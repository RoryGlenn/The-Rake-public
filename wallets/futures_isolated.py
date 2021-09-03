import datetime
import math
import time

from threading           import Event
from binance             import Client

from util.enums          import *
from util.log            import Log
from util.error_log      import ErrorLog
from util.binance_client import Binance_Client


class FuturesIsolated(Binance_Client):
    def __init__(self, parameter_dict, exit_event: Event, log_file: Log, error_file: ErrorLog):
        self.binance_client      = Client(api_key=parameter_dict['binance_api_key'], 
                                          api_secret=parameter_dict['binance_secret_key'],
                                          tld='com')
        self.log_file            = log_file
        self.error_file          = error_file
        self.thread_exit_event   = exit_event
        self.account_trades_list = list()


    def wait(self, message="", timeout=NAP):
        if self.thread_exit_event.wait(timeout):
            self.print_and_log(message=message, end=True)
            return True
        return False


    def take_nap(self):
        time.sleep(NAP)


    def round_decimals_down(self, number:float, decimals:int=2):
        """Returns a value rounded down to a specific number of decimal places."""
        if not isinstance(decimals, int):
            raise TypeError("decimal places must be an integer")
        elif decimals < 0:
            raise ValueError("decimal places has to be 0 or more")
        elif decimals == 0:
            return math.floor(number)
        factor = 10 ** decimals
        return math.floor(number * factor) / factor


    def futures_isolated_get_notional_value(self, mark_price, quantity_to_sell, min_quantity):
        """if the quantity of coin we want to trade is less than $5,
            then find and set the min amount to trade at $5.00 in terms of the quantity of coin"""
        i = min_quantity
        result = quantity_to_sell * mark_price
        if result < FUTURES_NOTIONAL_MIN:
            while result < FUTURES_NOTIONAL_MIN:
                i     += min_quantity
                result = i * mark_price
                quantity_to_sell = i
                if result == NOTHING:
                    break
        return quantity_to_sell


    def futures_isolated_get_realized_pnl(self):
        """Gets realized PnL (profit) made for the last hour in usdt"""
        realizedPnl = 0.0
        account_trades      = self.binance_client.futures_account_trades()
        account_trades_list = list(account_trades)
        one_hour_ago        = datetime.datetime.now() - datetime.timedelta(hours=1)
        account_trades_list.reverse()

        for trade in account_trades_list:
            time_of_trade    = datetime.datetime.fromtimestamp(int(trade['time']) / 1000)
            if time_of_trade < one_hour_ago:
                break
            realizedPnl += float(trade['realizedPnl'])
        return round(realizedPnl, 2)


    def futures_to_spot_transfer(self, realizedPnl, symbol=USDT):
        try:
            self.binance_client.futures_account_transfer(
                asset            = symbol,
                amount           = abs(realizedPnl),
                type             = 2,
                dualSidePosition = False,
                recvWindow       = RECV_WINDOW)

            self.print_and_log(message=f"{'${:,.3f}'.format(realizedPnl)} raked", money=True)
            self.write(f"{symbol} {abs(realizedPnl)}")
        except Exception as e:
            self.print_and_log(message=f"futures_to_spot_transfer failed", e=e)


    def futures_isolated_get_coin_min_trade_quantity(self, symbol):
        """This is the smallest quantity that we can trade in terms of the given coin"""
        min_trade_qty = float(FUTURES_MIN_TRADE_DICT[symbol])
        if min_trade_qty == 1:
            min_trade_qty = 0
        else:
            min_trade_qty = len( str(min_trade_qty) ) - 2
        return min_trade_qty


    def futures_isolated_get_dollar_max_precision(self, symbol):
        """Gets the maximum decimal places we can buy or sell the coin in terms of dollar"""
        max_prec = float(FUTURES_MAX_PRECISION_DICT[symbol])
        if max_prec == 1:
            max_prec = 0
        else:
            max_prec = len(str(max_prec)) - 2
        return max_prec


    def futures_isolated_check_open_stop_order(self, symbol, stop_price, quantity):
        """if there is already an open order on the symbol, return"""
        try:
            open_orders = self.binance_client.futures_get_open_orders(recvWindow=RECV_WINDOW)
            for dictionary in open_orders:
                if dictionary[SYMBOL]       == symbol      and \
                     dictionary['type']     == STOP_MARKET and \
                     dictionary['price']    == stop_price  and \
                     dictionary['quantity'] == quantity:
                    return True
                if dictionary[SYMBOL] == symbol and dictionary['type'] == STOP_MARKET and dictionary['price'] != stop_price:
                    self.binance_client.futures_cancel_order(symbol=symbol, orderId=int(dictionary['orderId']), recvWindow=RECV_WINDOW)
            return False
        except Exception as e:
            self.print_and_log(f"could not get open stop order for {symbol}", e=e)


    def futures_isolated_set_stop_in_profit(self, symbol, stop_price, quantity):
        """Sets a stop/limit for a symbol while the position is still in profit.
            In order for futures_isolated_set_stop_in_profit() to work,
                LONG:  stopPrice must be lower than markPrice
                SHORT: stopPrice must be higher than markPrice"""

        if abs(quantity) <= 0:
            return

        """if the position has been closed, return"""
        if self.futures_get_position_quantity(symbol) == NOTHING:
            return

        if self.futures_isolated_check_open_stop_order(symbol, stop_price, quantity):
            return

        stop_price = round(stop_price, self.futures_isolated_get_dollar_max_precision(symbol))
        mark_price = self.futures_get_mark_price(symbol)

        try:
            if self.futures_get_position_type(symbol) == LONG:
                if mark_price > stop_price: # and stop_price > entry_price:
                    self.binance_client.futures_create_order(
                        symbol      = symbol,
                        stopPrice   = stop_price,
                        quantity    = quantity,
                        side        = SELL,
                        type        = STOP_MARKET,
                        reduceOnly  = True,
                        recvWindow  = RECV_WINDOW)
            else:
                if mark_price < stop_price:
                    self.binance_client.futures_create_order(
                        symbol      = symbol,
                        stopPrice   = stop_price,
                        quantity    = quantity,
                        side        = BUY,
                        type        = STOP_MARKET,
                        reduceOnly  = True,
                        recvWindow  = RECV_WINDOW)
            self.print_and_log(f"{FUTURES_ISOLATED}: Set ${stop_price} stop for {symbol} {quantity}")
        except Exception as e:
            self.print_and_log(f"{FUTURES_ISOLATED}: could not set ${stop_price} stop or limit for {symbol} position", e=e)


    def futures_isolated_get_deleverage_ratio_threshold(self, dictionary):
        deleverage_ratio_threshold = 0
        if float(dictionary[QUANTITY]) > NOTHING:
            deleverage_ratio_threshold = float(dictionary[ENTRY_PRICE]) - ( (float(dictionary[ENTRY_PRICE]) - float(dictionary[LIQUIDATION_PRICE]) ) * FUTURES_ISOLATED_AUTO_DELEVERAGE_PERCENT)
        elif float(dictionary[QUANTITY]) < NOTHING:
            deleverage_ratio_threshold = float(dictionary[ENTRY_PRICE]) + ( (float(dictionary[ENTRY_PRICE]) - float(dictionary[LIQUIDATION_PRICE]) ) * FUTURES_ISOLATED_AUTO_DELEVERAGE_PERCENT)
        return deleverage_ratio_threshold


    def futures_isolated_get_open_positions(self):
        """check if position is still open before adding more margin to it"""
        open_positions_list = list()
        positions = self.binance_client.futures_position_information(recvWindow=RECV_WINDOW)
        for dictionary in positions:
            if float(dictionary[QUANTITY]) != NOTHING and dictionary[MARGIN_TYPE] == ISOLATED:
                open_positions_list.append(dictionary[SYMBOL])        
        return open_positions_list


    def futures_isolated_get_quantity_to_sell(self, dictionary):
        quantity = self.futures_get_position_quantity(dictionary[SYMBOL])
        return (abs(quantity) * FUTURES_ISOLATED_RAKE_PERCENT)


    def futures_isolated_get_final_quantity_to_sell(self, dictionary):
        """
        Order must meet all of these requirements at the same time:
            if the coin quantity meets the min trade requirement
            if the price meets the precision requirement in terms of the coin
            if the amount to sell is worth at least FUTURES_NOTIONAL_MIN ($5)
        """
        mark_price   = float(dictionary[MARK_PRICE])
        sell_qty     = abs(float(self.futures_get_position_quantity(dictionary[SYMBOL]))) * FUTURES_ISOLATED_RAKE_PERCENT
        coin_min_qty = self.futures_isolated_get_coin_min_trade_quantity(dictionary[SYMBOL])

        if coin_min_qty == 0:
            coin_min_qty = 1

        if sell_qty < coin_min_qty:
            sell_qty = coin_min_qty

        """qty_to_sell_value = sell_qty * mark_price"""
        if sell_qty * mark_price < FUTURES_NOTIONAL_MIN:
            sell_qty = self.futures_isolated_get_notional_value(mark_price, sell_qty, coin_min_qty)
        return sell_qty



    def futures_isolated_get_amount_to_transfer(self, dictionary):
        quantity_to_sell = self.futures_isolated_get_quantity_to_sell(dictionary)
        mark_price       = float(dictionary[MARK_PRICE])
        entry_price      = float(dictionary[ENTRY_PRICE])
        amount_to_transfer = quantity_to_sell * (mark_price - entry_price)
        return round(amount_to_transfer, 4)


    def futures_isolated_deleverage(self, dictionary):
        """
        1. Get deleverage ratio threshold for all futures isolated open positions
        2. if markPrice < deleverage_price, sell off FUTURES_ISOLATED_DELEVERAGE_QUANTITY_PERCENT of the quantity
        3. add the margin that was sold off in the previous step, back into the position
        """

        if float(dictionary[UNREALIZED_PROFIT]) > NOTHING:
            return

        deleverage_price = self.futures_isolated_get_deleverage_ratio_threshold(dictionary)

        if float(dictionary[MARK_PRICE]) < deleverage_price:
            self.print_and_log(message=f"FUTURES ISOLATED: Deleverage price for {dictionary[SYMBOL]}: {round(deleverage_price, 4)}")
            
            position_type = self.futures_get_position_type(dictionary[SYMBOL])
            qty_max_prec  = self.futures_isolated_get_coin_min_trade_quantity(dictionary[SYMBOL])

            quantity_to_close = abs(float(dictionary[QUANTITY])) * FUTURES_ISOLATED_DELEVERAGE_QUANTITY_PERCENT
            quantity_to_close = round(quantity_to_close, int(qty_max_prec))
            
            if quantity_to_close <= NOTHING:
                """if the quantity we want to trade gets rounded to zero, change it back to the minimum (smallest) amount to trade"""
                quantity_to_close = self.futures_isolated_get_coin_min_trade_quantity(dictionary[SYMBOL])

            if position_type == LONG:
                self.futures_close_long_position(dictionary[SYMBOL], quantity_to_close)
            else:
                self.futures_close_short_position(dictionary[SYMBOL], quantity_to_close)

            open_positions_list = self.futures_isolated_get_open_positions()

            if dictionary[SYMBOL] in open_positions_list:
                margin_to_add = (float(dictionary[ISOLATED_MARGIN]) + float(dictionary[UNREALIZED_PROFIT])) * FUTURES_ISOLATED_DELEVERAGE_QUANTITY_PERCENT
                self.binance_client.futures_change_position_margin(symbol=dictionary[SYMBOL], amount=margin_to_add, type=1, recvWindow=RECV_WINDOW)
                self.print_and_log(message=f"{FUTURES_ISOLATED}: Added ${round(margin_to_add, 4)} margin to {dictionary[SYMBOL]} position")


    def rake_it(self, dictionary):
        entry_price      = float(dictionary[ENTRY_PRICE])
        position_type    = self.futures_get_position_type(dictionary[SYMBOL])
        quantity_to_sell = self.futures_isolated_get_final_quantity_to_sell(dictionary)
        self.print_and_log(f"{FUTURES_ISOLATED}: {dictionary[SYMBOL]} {quantity_to_sell} to sell")

        if position_type == LONG:
            self.futures_close_long_position(dictionary[SYMBOL], quantity_to_sell)

            if FUTURES_ISOLATED_STOP_IN_PROFIT:
                stop_price = entry_price + (entry_price * FUTURES_ISOLATED_STOP_IN_PROFIT)
                self.futures_isolated_set_stop_in_profit(dictionary[SYMBOL], stop_price, abs(float(dictionary[QUANTITY])))
        else:
            self.futures_close_short_position(dictionary[SYMBOL], quantity_to_sell)

            if FUTURES_ISOLATED_STOP_IN_PROFIT:
                stop_price = entry_price - (entry_price * FUTURES_ISOLATED_STOP_IN_PROFIT)
                self.futures_isolated_set_stop_in_profit(dictionary[SYMBOL], stop_price, abs(float(dictionary[QUANTITY])))


    def futures_isolated_sell_remaining(self, dictionary):
        """If the current position value is between 5-10 dollars, sell the remaining instead of raking it 
            in order to avoid any type of min notional error in the future"""
        entry_price    = float(dictionary[ENTRY_PRICE])
        quantity       = abs(float(dictionary[QUANTITY]))
        position_value = entry_price * quantity

        if (position_value > FUTURES_NOTIONAL_MIN) and (position_value < FUTURES_NOTIONAL_MIN*2):
            position_type    = self.futures_get_position_type(dictionary[SYMBOL])
            quantity_to_sell = abs(float(self.futures_get_position_quantity(dictionary[SYMBOL])))

            if position_type == LONG:
                self.futures_close_long_position(dictionary[SYMBOL], quantity_to_sell)
            else:
                self.futures_close_short_position(dictionary[SYMBOL], quantity_to_sell)
            return True
        return False


    def futures_isolated_get_pnl(self, dictionary):
        """Returns the needed variables for the rest of the rake function"""
        unrealized_profit = float(dictionary[UNREALIZED_PROFIT])
        quantity          = abs(float(dictionary[QUANTITY]))
        mark_price        = float(self.futures_get_mark_price(dictionary[SYMBOL]))
        position_value    = mark_price * quantity
        pnl_percent       = unrealized_profit / position_value
        self.print_and_log(message=f"{FUTURES_ISOLATED}: {dictionary[SYMBOL]} pnl: {round(pnl_percent*100, 4)}%")
        return pnl_percent


    def rake_futures_isolated(self):
        while True:
            positions = None

            try:
                future = (datetime.timedelta(minutes=FUTURES_ISOLATED_RAKE_TIME/60) + datetime.datetime.now()).strftime("%H:%M:%S")
                self.print_and_log(f"{FUTURES_ISOLATED}: Waiting till {future} to rake...")

                if self.wait(message=f"{FUTURES_ISOLATED}: exiting rake_futures_isolated thread", timeout=FUTURES_ISOLATED_RAKE_TIME): break
                positions = self.binance_client.futures_position_information(recvWindow=RECV_WINDOW)
            except Exception as e:
                self.print_and_log(f"{FUTURES_ISOLATED}: could not get futures position info", e=e)
                if self.wait(timeout=LONG_NAP): break
                continue


            for dictionary in positions:
                if (dictionary[SYMBOL] not in FUTURES_ISOLATED_RAKE_BLACKLIST) and (dictionary[SYMBOL] not in STABLE_COINS_LIST):
                    if (dictionary[MARGIN_TYPE] == CROSS) or (float(dictionary[QUANTITY]) == NOTHING):
                        continue

                    self.print_and_log(message=f"{FUTURES_ISOLATED}: Checking asset {dictionary[SYMBOL]}")

                    if FUTURES_ISOLATED_AUTO_DELEVERAGE:
                        self.futures_isolated_deleverage(dictionary)

                    if float(dictionary[UNREALIZED_PROFIT]) > NOTHING:
                        if self.wait(timeout=LONG_NAP): break

                        try:
                            if self.futures_isolated_get_pnl(dictionary) < FUTURES_ISOLATED_RAKE_THRESHOLD_PERCENT:
                                continue

                            if self.futures_isolated_sell_remaining(dictionary):
                                continue

                            self.rake_it(dictionary)
                            amount_to_transfer = self.futures_isolated_get_amount_to_transfer(dictionary)

                            if amount_to_transfer < USDT_TRANSFER_MIN:
                                self.print_and_log(message=f"{FUTURES_ISOLATED}: {'${:,.4f}'.format(amount_to_transfer)} is too low to rake", money=True)
                                continue

                            if amount_to_transfer < FLEXIBLE_SAVINGS_USDT_MIN:
                                self.print_and_log(message=f"{FUTURES_ISOLATED}: Leaving {'${:,.4}'.format(amount_to_transfer)} in futures wallet", money=True)
                                continue
                            
                            self.take_nap()
                            self.futures_to_spot_transfer(amount_to_transfer, symbol=USDT)

                            self.take_nap()
                            self.spot_to_flexible_savings(FUTURES_ISOLATED, USDT, amount_to_transfer)
                        except Exception as e:
                            self.print_and_log(F"{FUTURES_ISOLATED}: rake_futures_isolated", e=e)
                            continue

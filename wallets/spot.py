import datetime
import os

from threading           import Event
from binance             import Client

from util.enums          import *
from util.log            import Log
from util.binance_client import Binance_Client


class Spot(Binance_Client):
    def __init__(self, parameter_dict, exit_event: Event, log_file: Log):
        self.binance_client      = Client(api_key=parameter_dict['binance_api_key'], api_secret=parameter_dict['binance_secret_key'], tld='com')
        self.log_file            = log_file
        self.thread_exit_event   = exit_event
        self.account_trades_list = list()        


    def wait(self, message="", timeout=NAP):
        if self.thread_exit_event.wait(timeout):
            self.print_and_log(message=message, end=True)
            return True
        return False


    def spot_get_assets(self):
        asset_dict = dict()
        try:
            account = self.binance_client.get_account(recvWindow=RECV_WINDOW)
            if account['accountType'] == 'SPOT':
                balances = account['balances']
                for dictionary in balances:
                    if float(dictionary['free']) > 0:
                        asset_dict[dictionary['asset']] = float(dictionary['free'])
        except Exception as e:
            self.print_and_log("could not get spot assets", e=e)
        return asset_dict


    def spot_get_notional_value(self, mark_price, quantity_to_sell, min_quantity):
        i = min_quantity
        result = quantity_to_sell * mark_price
        if result < SPOT_NOTIONAL_MIN:
            while result < SPOT_NOTIONAL_MIN:
                i += min_quantity
                result = i * mark_price
                quantity_to_sell = i
        return quantity_to_sell


    def spot_get_usdt(self):
        account = self.binance_client.get_account()
        quantity_usdt = 0
        balances = account['balances']
        for dictionary in balances:
            if dictionary['asset'] == USDT:
                quantity_usdt = float(dictionary['free']) - 0.01
                break
        return round(quantity_usdt, 2)


    def spot_get_decimal_precision(self, symbol):
        max_prec = float(SPOT_MAX_PRECISION_DICT[symbol])
        if max_prec == 1:
            max_prec = 0
        else:
            max_prec = len(str(max_prec)) - 2
        return max_prec


    def spot_get_min_trade_qty(self, symbol):
        quantity = float(SPOT_MIN_TRADE_AMOUNTS_DICT[symbol])
        return quantity


    def spot_get_symbol_entry_price(self, symbol):
        entry_price = 0

        if not os.path.exists(SPOT_ENTRY_PRICES):
            return entry_price

        with open(SPOT_ENTRY_PRICES, 'r') as file:
            lines = file.readlines()
            for line in lines:
                symbol_ = line.split()
                if symbol_[0].upper() == symbol:
                    entry_price = float(symbol_[1])
                    break
        return entry_price



    def rake_spot(self):
        while True:
            try:
                future = (datetime.timedelta(minutes=SPOT_RAKE_TIME/60) + datetime.datetime.now()).strftime("%H:%M:%S")
                self.print_and_log(f"SPOT: Waiting till {future} to rake...")
                
                if self.wait(message="SPOT: exiting rake_spot thread", timeout=SPOT_RAKE_TIME): break

                # assume that if no list is given, that we bought the coin at $0.0
                asset_dict = self.spot_get_assets()

                for symbol, quantity in asset_dict.items():
                    if symbol not in SPOT_RAKE_BLACKLIST and symbol not in STABLE_COINS_LIST and USDT not in symbol:
                        
                        self.print_and_log(message=f"SPOT: Checking asset {symbol}")

                        if self.thread_exit_event.wait(timeout=LONG_NAP):
                            break

                        try:
                            mark_price  = float(self.binance_client.get_symbol_ticker(symbol=symbol+USDT)['price'])
                            entry_price = self.spot_get_symbol_entry_price(symbol)
                            
                            owned_qty     = quantity
                            entry_value   = entry_price * quantity
                            current_value = mark_price * quantity

                            if entry_value == 0:
                                entry_value = 1

                            roi_percent = ((current_value / entry_value) - 1) * 100

                            if roi_percent < SPOT_RAKE_THRESHOLD_PERCENT:
                                continue

                            if current_value > SPOT_NOTIONAL_MIN and current_value < 20:
                                # sell it all to avoid MIN_NOMINAL error
                                max_prec = self.spot_get_decimal_precision(symbol+"/USDT")
                                quantity = round(owned_qty, max_prec)
                                
                                if quantity > owned_qty:
                                    quantity = self.round_decimals_down(owned_qty, max_prec)
                                

                                min_qty = self.spot_get_min_trade_qty(symbol+"/USDT")
                                min_qty_len = len(str(min_qty)) - 2

                                if len(str(quantity)) - 2 > min_qty_len:
                                    quantity = self.round_decimals_down(quantity, min_qty_len)

                                
                                self.print_and_log(message=f"SPOT: {symbol+USDT} {quantity} to sell")

                                self.binance_client.create_order(
                                        symbol     = symbol + USDT,
                                        quantity   = quantity,
                                        side       = "SELL",
                                        type       = "MARKET",
                                        recvWindow = RECV_WINDOW)

                                self.print_and_log(message=f"SPOT: Sold {symbol+USDT} {quantity}", money=True)
                                continue
                        except Exception as e:
                            self.print_and_log(message=f"SPOT: rake_spot {symbol}", e=e)
                            continue


                        if current_value < SPOT_NOTIONAL_MIN:
                            continue

                        self.print_and_log(message=f"SPOT: {symbol} roi: {round(roi_percent, 2)}%")

                        quantity_to_sell = quantity * SPOT_RAKE_PERCENT
                        amount_to_rake   = quantity_to_sell * (mark_price - entry_price)

                        min_trade_quantity = self.spot_get_min_trade_qty(symbol+"/USDT")
                        max_prec           = self.spot_get_decimal_precision(symbol+"/USDT")
                        
                        if quantity_to_sell < min_trade_quantity:
                            quantity_to_sell = min_trade_quantity

                        quantity_to_sell = self.round_decimals_down(quantity_to_sell, max_prec)

                        # if the value we are trying to sell is less than the $10 min, up the amount to sell to $10
                        if quantity_to_sell * mark_price < SPOT_NOTIONAL_MIN:
                            quantity_to_sell = self.spot_get_notional_value(mark_price, quantity_to_sell, min_trade_quantity)
                            
                        # if the quantity to sell if over the precision limit, round it to the maximum precision limit
                        if len(str(quantity_to_sell)) > max_prec:
                            quantity_to_sell = round(quantity_to_sell, max_prec)


                        self.binance_client.create_order(
                                symbol     = symbol + USDT, 
                                quantity   = quantity_to_sell,
                                side       = SELL,
                                type       = MARKET,
                                recvWindow = RECV_WINDOW)

                        self.print_and_log(message=f"SPOT: Sold {symbol+USDT} {quantity_to_sell}", money=True)

                        # minimum USDT transfer amount
                        if amount_to_rake < USDT_TRANSFER_MIN:
                            self.print_and_log(message=f"SPOT: {'${:,.4f}'.format(amount_to_rake)} is too low to rake")
                            continue

                        if amount_to_rake < FLEXIBLE_SAVINGS_USDT_MIN:
                            self.print_and_log(message=f"SPOT: Leaving {'${:,.4f}'.format(amount_to_rake)} in spot account", money=True)
                            continue
                        
                        if self.wait(timeout=NAP): break
                        self.spot_to_flexible_savings(SPOT, USDT, amount_to_rake)
            except Exception as e:
                self.print_and_log(message=f"SPOT: rake_spot", e=e)
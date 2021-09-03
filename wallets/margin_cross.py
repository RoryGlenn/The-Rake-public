import datetime
import os

from threading           import Event
from binance             import Client

from util.enums          import *
from util.log            import Log
from util.binance_client import Binance_Client
from util.error_log      import ErrorLog

from wallets.spot        import Spot


class MarginCross(Spot, Binance_Client):
    def __init__(self, parameter_dict, exit_event: Event, log_file: Log, error_file: ErrorLog):
        self.binance_client          = Client(api_key=parameter_dict['binance_api_key'], 
                                              api_secret=parameter_dict['binance_secret_key'],
                                              tld='com')
        self.log_file                = log_file
        self.error_file              = error_file
        self.thread_exit_event       = exit_event
        self.account_trades_list     = list()      


    def wait(self, message="", timeout=NAP):
        if self.thread_exit_event.wait(timeout):
            self.print_and_log(message=message, end=True)
            return True
        return False


    def margin_cross_get_symbol_entry_price(self, symbol):
        entry_price = 0

        if not os.path.exists(MARGIN_CROSS_ENTRY_PRICES):
            return entry_price

        with open(MARGIN_CROSS_ENTRY_PRICES, 'r') as file:
            lines = file.readlines()
            for line in lines:
                symbol_ = line.split()
                if symbol_[0].upper() == symbol:
                    entry_price = float(symbol_[1])
                    break
        return entry_price


    def margin_to_spot(self, symbol, quantity):
        try:
            self.binance_client.transfer_margin_to_spot(asset=symbol, amount=quantity, type=2, recvWindow=RECV_WINDOW)
        except Exception as e:
            self.print_and_log(f"could not transfer {symbol} {quantity} from cross margin to spot wallet", e=e)



    def rake_margin_cross(self):
        while True:
            try:
                future = (datetime.timedelta(minutes=CROSS_RAKE_TIME/60) + datetime.datetime.now()).strftime("%H:%M:%S")
                self.print_and_log(f"{MARGIN_CROSS}: Waiting till {future} to rake...")

                if self.wait(message=f"{MARGIN_CROSS}: exiting rake_margin_cross thread", timeout=CROSS_RAKE_TIME): break
            except Exception as e:
                self.print_and_log(f"{MARGIN_CROSS}: rake_margin_cross", money=False, e=e)
                if self.wait(timeout=LONG_NAP): break
                continue

            asset_dict           = dict()
            borrowed_dict        = dict()
            usdt_available       = 0
            cross_margin_account = self.binance_client.get_margin_account()
            user_assets          = cross_margin_account['userAssets']
            
            for dictionary in user_assets:
                if float(dictionary['free']) > 0:
                    asset_dict[dictionary['asset']] = float(dictionary['free'])
            
            for dictionary in user_assets:
                if float(dictionary['borrowed']) > 0:
                    borrowed_dict[dictionary['asset']] = float(dictionary['borrowed'])


            # if there is any USDT available, pay off loans
            if USDT in borrowed_dict.keys() and USDT in asset_dict.keys():
                if asset_dict[USDT] > 0 and borrowed_dict[USDT] > 0:
                    response = self.binance_client.repay_margin_loan(asset=USDT, amount=asset_dict[USDT], recvWindow=RECV_WINDOW)
                    self.print_and_log(f"{MARGIN_CROSS}: repaid margin loan USDT {round(asset_dict[USDT], 4)} {response}", money=True)
                    

            # if there is any usdt available, move it to earn wallet
            cross_margin_account = self.binance_client.get_margin_account()
            user_assets          = cross_margin_account['userAssets']
            for dictionary in user_assets:
                if dictionary['asset'] == USDT:
                    usdt_available = float(dictionary['free'])
                    break

            if usdt_available > 0:
                self.margin_to_spot(USDT, usdt_available)
                if self.wait(timeout=NAP): 
                    break
                self.spot_to_flexible_savings(MARGIN_CROSS, USDT, usdt_available)


            for asset, quantity in asset_dict.items():
                if asset not in CROSS_RAKE_BLACKLIST and asset not in STABLE_COINS_LIST and USDT not in asset:
                    self.print_and_log(message=f"{MARGIN_CROSS}: Checking asset {asset}")
                    
                    if self.wait(timeout=LONG_NAP): break

                    try:
                        owned_qty   = quantity
                        mark_price  = float(self.binance_client.get_symbol_ticker(symbol=asset+USDT)['price'])
                        entry_price = self.margin_cross_get_symbol_entry_price(asset)

                        entry_value   = entry_price * quantity
                        current_value = mark_price * quantity

                        if entry_value == 0:
                            entry_value = 1

                        roi_percent = ((current_value / entry_value) - 1) * 100

                        if roi_percent < MARGIN_CROSS_RAKE_THRESHOLD_PERCENT:
                            continue
                        
                        if current_value > MARGIN_CROSS_NOTIONAL_MIN and current_value < 20:
                            # sell it all to avoid MIN_NOMINAL error
                            max_prec = self.spot_get_decimal_precision(asset+"/USDT")
                            quantity = round(owned_qty, max_prec)
                            
                            if quantity > owned_qty:
                                quantity = self.round_decimals_down(owned_qty, max_prec)

                            self.binance_client.create_margin_order(symbol=asset+USDT, quantity=quantity, type="MARKET", side="SELL", recvWindow=RECV_WINDOW)
                            self.print_and_log(message=f"{MARGIN_CROSS}: Sold {asset}USDT {quantity}", money=True)

                            response = self.binance_client.repay_margin_loan(asset=USDT, amount=amount_to_rake, recvWindow=RECV_WINDOW)
                            self.print_and_log(f"{MARGIN_CROSS}: repaid margin loan {asset} {round(amount_to_rake, 4)} {response}", money=True)
                            continue

                        if current_value < MARGIN_CROSS_NOTIONAL_MIN:
                            continue


                        self.print_and_log(message=f"{MARGIN_CROSS}: {asset} roi: {round(roi_percent, 2)}%")

                        quantity_to_sell = quantity * MARGIN_CROSS_RAKE_PERCENT
                        amount_to_rake   = quantity_to_sell * (mark_price - entry_price)

                        min_trade_quantity = self.spot_get_min_trade_qty(asset+"/USDT")
                        max_prec           = self.spot_get_decimal_precision(asset+"/USDT")
                        

                        if quantity_to_sell < min_trade_quantity:
                            quantity_to_sell = min_trade_quantity

                        quantity_to_sell = self.round_decimals_down(quantity_to_sell, max_prec)

                        # if the value we are trying to sell is less than the $10 min, up the amount to sell to $10
                        if quantity_to_sell * mark_price < MARGIN_CROSS_NOTIONAL_MIN:
                            quantity_to_sell = self.spot_get_notional_value(mark_price, quantity_to_sell, min_trade_quantity)
                            
                        # if the quantity to sell if over the precision limit, round it to the maximum precision limit
                        if len(str(quantity_to_sell)) > max_prec:
                            quantity_to_sell = round(quantity_to_sell, max_prec)

                        if quantity_to_sell <= 0:
                            self.print_and_log(f"{MARGIN_CROSS}: {asset+USDT} {quantity_to_sell} is too low to sell!")
                            continue

                        self.print_and_log(f"{MARGIN_CROSS}: {asset+USDT} {quantity_to_sell} to sell")

                        if len(str(quantity_to_sell)) > max_prec:
                            quantity = round(quantity_to_sell, max_prec)

                        self.binance_client.create_margin_order(symbol=asset+USDT, quantity=quantity_to_sell, type=MARKET, side=SELL, recvWindow=RECV_WINDOW)
                        self.print_and_log(message=f"{MARGIN_CROSS}: Sold {asset+USDT} {quantity_to_sell}", money=True)

                        response = self.binance_client.repay_margin_loan(asset=USDT, amount=amount_to_rake, recvWindow=RECV_WINDOW)
                        self.print_and_log(f"{MARGIN_CROSS}: repaid margin loan {asset} {round(amount_to_rake, 4)} {response}", money=True)

                        # minimum USDT transfer amount
                        if amount_to_rake < USDT_TRANSFER_MIN:
                            self.print_and_log(message=f"{MARGIN_CROSS}: {'${:,.4f}'.format(amount_to_rake)} is too low to rake")
                            continue

                        if amount_to_rake < FLEXIBLE_SAVINGS_USDT_MIN:
                            self.print_and_log(message=f"{MARGIN_CROSS}: Leaving {'${:,.4f}'.format(amount_to_rake)} in {MARGIN_CROSS} wallet", money=True)
                            continue

                    except Exception as e:
                        self.print_and_log(message=f"{MARGIN_CROSS}: rake_margin_cross", e=e)
                        continue

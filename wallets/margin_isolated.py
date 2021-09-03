import math
import datetime
import os

from threading           import Event
from binance             import Client

from util.enums          import *
from util.log            import Log
from util.binance_client import Binance_Client
from util.error_log      import ErrorLog

from wallets.spot        import Spot


class MarginIsolated(Spot, Binance_Client):
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


    def margin_isolated_to_spot(self, asset, symbol, quantity):
        try:
            if asset in symbol:
                self.binance_client.transfer_isolated_margin_to_spot(asset=asset, symbol=symbol, amount=quantity, transFrom=ISOLATED_MARGIN, transTo=SPOT, recvWindow=RECV_WINDOW)
                self.print_and_log(f"{MARGIN_ISOLATED}: transferred {quantity} {asset} from {symbol} isolated margin wallet to spot wallet")
                return True
        except Exception as e:
            self.print_and_log(f"{MARGIN_ISOLATED}: could not transfer {symbol} {quantity} from isolated margin to spot wallet", e=e)
            return False


    def margin_isolated_get_symbol_entry_price(self, symbol):
        entry_price = 0

        if not os.path.exists(MARGIN_ISOLATED_ENTRY_PRICES):
            return entry_price

        with open(MARGIN_ISOLATED_ENTRY_PRICES, 'r') as file:
            lines = file.readlines()
            for line in lines:
                symbol_ = line.split()
                if symbol_[0].upper() == symbol:
                    entry_price = float(symbol_[1])
                    break
        return entry_price


    def margin_isolated_get_assets(self, assets):
        assets_dict = dict()
        for dictionary in assets:
            if float(dictionary['baseAsset']['free']) > 0:
                assets_dict[dictionary['baseAsset']['asset']] = float(dictionary['baseAsset']['free'])        
        return assets_dict


    def margin_isolated_get_all_symbols(self):
        """get all isolated symbols"""
        try:
            isolated_symbols = list()
            iso_symbols = self.binance_client.get_all_isolated_margin_symbols()
            for dictionary in iso_symbols:
                isolated_symbols.append(dictionary['symbol'])
        except Exception as e:
            self.print_and_log(message=f"{MARGIN_ISOLATED}: Can't get all margin isolated symbols", e=e)
        return isolated_symbols


    def margin_isolated_get_borrowed(self, assets):
        borrowed_dict = dict()
        for dictionary in assets:
            if float(dictionary['quoteAsset']['borrowed']) > 0:
                borrowed_dict[dictionary['baseAsset']['asset']] = float(dictionary['quoteAsset']['borrowed'])
        return borrowed_dict


    def margin_isolated_repay_loan(self, borrowed_dict):
        for symbol, value in borrowed_dict.items():
            usdt_available = self.margin_isolated_get_available_usdt(symbol+USDT)
            if usdt_available > NOTHING:
                response = self.binance_client.repay_margin_loan(asset=USDT, amount=usdt_available, symbol=symbol+USDT, isIsolated=True, recvWindow=RECV_WINDOW)
                self.print_and_log(f"{MARGIN_ISOLATED}: Repaid ${round(usdt_available, 4)} isolated margin loan on {symbol+USDT} {response}", money=True)


    def margin_isolated_get_available_usdt(self, symbol):
        usdt_available  = 0.0
        isolated_assets = self.binance_client.get_isolated_margin_account()['assets']
        for dictionary in isolated_assets:
            if dictionary['symbol'] == symbol:
                usdt_available = float(dictionary['quoteAsset']['free'])
                break
        return usdt_available


    def margin_isolated_to_flex(self):
        """Transfer USDT to flexible_savings wallet"""
        isolated_assets = self.binance_client.get_isolated_margin_account()['assets']
        for dictionary in isolated_assets:
            usdt_available = self.margin_isolated_get_available_usdt(dictionary['symbol'])

            if usdt_available > NOTHING:
                result = self.margin_isolated_to_spot(asset=USDT, symbol=dictionary['symbol'], quantity=usdt_available)
                if result:
                    self.spot_to_flexible_savings(MARGIN_ISOLATED, USDT, usdt_available)


    def margin_isolated_move_asset_on_repay(self, isolated_assets_dict, borrowed_dict):
        # if the borrowed money on an asset is 0, move the asset into spot
        if MARGIN_ISOLATED_MOVE_ASSET_ON_REPAY:
            for key, value in isolated_assets_dict.items():
                if key not in borrowed_dict.keys():
                    self.margin_isolated_to_spot(asset=key, symbol=key+USDT, quantity=value)


    def margin_isolated_get_quote_asset(self, asset_to_find):
        quote_asset = None
        isolated_assets = self.binance_client.get_isolated_margin_account()['assets']
        for dictionary in isolated_assets:
            if dictionary['baseAsset']['asset'] == asset_to_find:
                quote_asset = dictionary['quoteAsset']['asset']
                break
        return quote_asset


    def rake_margin_isolated(self):
        isolated_symbols = self.margin_isolated_get_all_symbols()


        while True:
            isolated_assets_dict = dict()
            borrowed_dict        = dict()

            try:
                future = (datetime.timedelta(minutes=ISOLATED_RAKE_TIME/60) + datetime.datetime.now()).strftime("%H:%M:%S")
                self.print_and_log(f"{MARGIN_ISOLATED}: Waiting till {future} to rake...")

                if self.wait(message=f"{MARGIN_ISOLATED}: exiting rake_margin_isolated thread", timeout=ISOLATED_RAKE_TIME): break

                isolated_assets      = self.binance_client.get_isolated_margin_account()['assets']
                isolated_assets_dict = self.margin_isolated_get_assets(isolated_assets)
                borrowed_dict        = self.margin_isolated_get_borrowed(isolated_assets)

                self.margin_isolated_repay_loan(borrowed_dict)
                self.margin_isolated_to_flex()
                self.margin_isolated_move_asset_on_repay(isolated_assets_dict, borrowed_dict)

            except Exception as e:
                self.print_and_log(f"{MARGIN_ISOLATED}: rake_margin_isolated", e=e)
                continue

            for asset, quantity in isolated_assets_dict.items():
                if asset not in ISOLATED_RAKE_BLACKLIST and asset not in STABLE_COINS_LIST and USDT not in asset:
                    self.print_and_log(message=f"{MARGIN_ISOLATED}: Checking asset {asset}")
                    
                    if self.wait(message=f"{MARGIN_ISOLATED}: exiting rake_margin_isolated thread", timeout=LONG_NAP): break
                    
                    quote_asset = self.margin_isolated_get_quote_asset(asset)

                    if quote_asset != USDT:
                        continue

                    try:
                        owned_qty   = quantity
                        mark_price  = float(self.binance_client.get_symbol_ticker(symbol=asset+USDT)['price'])
                        entry_price = self.margin_isolated_get_symbol_entry_price(asset)

                        entry_value   = entry_price * quantity
                        current_value = mark_price * quantity

                        if entry_value == 0:
                            entry_value = 1

                        # if the current value of the asset is less than ISOLATED_NOTIONAL_MIN, move it to spot
                        if current_value < MARGIN_ISOLATED_NOTIONAL_MIN:
                            self.margin_isolated_to_spot(asset=asset, symbol=asset+USDT, quantity=quantity)
                            continue


                        roi_percent = ((current_value / entry_value) - 1) * 100

                        if roi_percent < MARGIN_ISOLATED_RAKE_THRESHOLD_PERCENT:
                            continue

                        if current_value > MARGIN_ISOLATED_NOTIONAL_MIN and current_value < 20:
                            """sell it all to avoid MIN_NOMINAL error"""
                            max_prec = self.spot_get_decimal_precision(asset+"/USDT")
                            quantity = round(owned_qty, max_prec)
                            
                            if quantity > owned_qty:
                                quantity = self.round_decimals_down(owned_qty, max_prec)

                            if asset+USDT in isolated_symbols:
                                self.binance_client.create_margin_order(symbol=asset+USDT, quantity=quantity, isIsolated=True, type="MARKET", side="SELL", recvWindow=RECV_WINDOW)
                                self.print_and_log(message=f"{MARGIN_ISOLATED}: Sold {asset} {quantity}", money=True)
                            else:
                                self.print_and_log(message=f"{MARGIN_ISOLATED}: {asset} is not a valid margin pair")
                            continue

                        if current_value < MARGIN_ISOLATED_NOTIONAL_MIN:
                            continue

                        self.print_and_log(message=f"{MARGIN_ISOLATED}: {asset+USDT} roi: {round(roi_percent, 2)}%")

                        quantity_to_sell = quantity * MARGIN_ISOLATED_RAKE_PERCENT

                        min_trade_quantity = self.spot_get_min_trade_qty(asset+"/USDT")
                        max_prec           = self.spot_get_decimal_precision(asset+"/USDT")
                        
                        if quantity_to_sell < min_trade_quantity:
                            quantity_to_sell = min_trade_quantity

                        quantity_to_sell = self.round_decimals_down(quantity_to_sell, max_prec)

                        # if the value we are trying to sell is less than the $10 min, up the amount to sell to $10
                        if quantity_to_sell * mark_price < MARGIN_ISOLATED_NOTIONAL_MIN:
                            quantity_to_sell = self.spot_get_notional_value(mark_price, quantity_to_sell, min_trade_quantity)
                            
                        # if the quantity to sell if over the precision limit, round it to the maximum precision limit
                        if len(str(quantity_to_sell)) > max_prec:
                            quantity_to_sell = round(quantity_to_sell, max_prec)

                        if quantity_to_sell <= 0:
                            self.print_and_log(f"{MARGIN_ISOLATED}: {asset+USDT} {quantity_to_sell} is too low to sell!")
                            continue

                        self.print_and_log(f"{MARGIN_ISOLATED}: {asset+USDT} {quantity_to_sell} to sell")

                        if len(str(quantity_to_sell)) > max_prec:
                            quantity_to_sell = round(quantity_to_sell, max_prec)

                        if asset+USDT in isolated_symbols:
                            self.binance_client.create_margin_order(symbol=asset+USDT, quantity=quantity_to_sell, isIsolated=True, type="MARKET", side="SELL", recvWindow=RECV_WINDOW)
                            self.print_and_log(message=f"{MARGIN_ISOLATED}: Sold {asset+USDT} {quantity_to_sell}", money=True)
                        else:
                            self.print_and_log(message=f"{MARGIN_ISOLATED}: {asset+USDT} is not a valid margin pair")
                            continue

                    except Exception as e:
                        self.print_and_log(message=f"{MARGIN_ISOLATED}: rake_margin_isolated", e=e)
                        continue

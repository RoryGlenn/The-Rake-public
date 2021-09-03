from util.enums          import *
from util.log            import Log
from util.error_log      import ErrorLog
from util.order_type     import OrderType, SideType


from binance    import Client
from threading  import Event

import datetime
import os
import math

class Binance_Client():
    def __init__(self, parameter_dict: dict, exit_event: Event, log_file: Log, error_file: ErrorLog):
        self.binance_client = Client(api_key=parameter_dict['binance_api_key'], 
                                     api_secret=parameter_dict['binance_secret_key'],
                                     tld='com')
        self.exit_event     = exit_event
        self.log_file       = log_file
        self.error_file     = error_file
        self.open_orders    = list()


    def get_current_time(self):
        return datetime.datetime.now().strftime("%H:%M:%S")



###################################################################################################
### PRINT/LOG ###
###################################################################################################
    def print_and_log(self, message, money=False, e=False, end=False):
        if money:
            print(              f"[$] {self.get_current_time()} {message}")
            self.log_file.write(f"[$] {self.get_current_time()} {message}")
            return
        if e:
            print(f"{e}, {type(e).__name__}, {__file__}, {e.__traceback__.tb_lineno}")
            print(                f"[!] {self.get_current_time()} ERROR: {message}")
            self.log_file.write(  f"[!] {self.get_current_time()} ERROR: {message}")
            self.log_file.write(  f"[!] {self.get_current_time()} {e}, {type(e).__name__}, {__file__}, {e.__traceback__.tb_lineno}")
            self.error_file.write(f"{self.get_current_time()} {e}, {type(e).__name__}, {__file__}, {e.__traceback__.tb_lineno}")
            return
        if end:
            print(              f"[-] {self.get_current_time()} {message}")
            self.log_file.write(f"[-] {self.get_current_time()} {message}")
            return
        print(              f"[*] {self.get_current_time()} {message}")
        self.log_file.write(f"[*] {self.get_current_time()} {message}")




###################################################################################################
### LONG ###
###################################################################################################
    def futures_close_long_position(self, symbol, quantity):
        if quantity <= 0:
            return

        try:
            self.binance_client.futures_create_order(
                symbol     = symbol,
                side       = SideType.SIDE_SELL,
                type       = OrderType.FUTURE_ORDER_TYPE_MARKET,
                quantity   = quantity,
                reduceOnly = True,
                recvWindow = RECV_WINDOW)

            self.print_and_log(f"FUTURES ISOLATED: closed {symbol} {quantity} long position")
        except Exception as e:
            self.print_and_log(f"FUTURES ISOLATED: Could not close long {symbol} {quantity} position", e=e)



###################################################################################################
### SHORT ###
###################################################################################################
    def futures_close_short_position(self, symbol, quantity):
        quantity = abs(quantity)
        
        if quantity <= 0:
            return
        
        try:
            self.binance_client.futures_create_order(
                symbol     = symbol, 
                side       = SideType.SIDE_BUY, 
                type       = OrderType.FUTURE_ORDER_TYPE_MARKET, 
                quantity   = quantity,
                reduceOnly = True,
                recvWindow = RECV_WINDOW)
            self.print_and_log(f"FUTURES ISOLATED: closed {symbol} {quantity} short position")
        except Exception as e:
            self.print_and_log(f"Could not close short {symbol} {quantity} position", e=e)


###################################################################################################
### POSITION TYPE ###
###################################################################################################
    def futures_get_position_type(self, symbol):
        """Figure out if our position is a long or short"""
        position_type = "Short"
        try:
            for dictionary in self.binance_client.futures_account(recvWindow=RECV_WINDOW)['positions']:
                if dictionary["symbol"] == symbol:
                    if float(dictionary['positionAmt']) > 0.0:
                        position_type = "Long"
        except Exception as e:
            self.print_and_log(f"Could not get position type for {symbol}", e=e)
        return position_type




###################################################################################################
### UTILITY/ETC... ###
###################################################################################################
    def futures_get_position_quantity(self, symbol):
        quantity = 0
        try:
            positions = self.binance_client.futures_position_information(recvWindow=RECV_WINDOW)
            for dictionary in positions:
                if dictionary['symbol'] == symbol:
                    quantity = float(dictionary['positionAmt'])
        except Exception as e:
            self.print_and_log(f"Could not get position quantity for {symbol}", e=e)
        return quantity


    def futures_get_mark_price(self, symbol):
        mark_price = 0
        
        if symbol in STABLE_COINS_LIST:
            return 1.0
        try:
            mark_price = self.binance_client.futures_mark_price(symbol=symbol, recvWindow=RECV_WINDOW)['markPrice']
            mark_price = round(float(mark_price), 4)
        except Exception as e:
            self.print_and_log(f"Could not get position type for {symbol}", e=e)
        return mark_price


    def futures_change_margin_type(self, symbol, marginType):
        try:
            self.binance_client.futures_change_margin_type(symbol=symbol, marginType=marginType, recvWindow=RECV_WINDOW)
        except Exception as e:
            self.print_and_log(f"Could not change margin type for {symbol} to {marginType}", e=e)



###################################################################################################
### TRANSFERS ###
###################################################################################################

    def margin_to_spot(self, symbol, quantity):
        try:
            self.binance_client.transfer_margin_to_spot(asset=symbol, amount=quantity, type=2, recvWindow=RECV_WINDOW)
        except Exception as e:
            self.print_and_log(f"could not transfer {symbol} {quantity} from cross margin to spot wallet", e=e)



    def spot_to_flexible_savings(self, wallet, productId, amount):
        if amount < 0.0:
            self.print_and_log(message=f"{wallet}: can't move negative values {productId} {'${:,.4f}'.format(amount)}")          
            return

        try:
            self.binance_client.purchase_lending_product(productId=productId+"001", amount=amount, recvWindow=RECV_WINDOW) 
            self.print_and_log(message=f"{wallet}: Moved to flexible savings: {productId} {'${:,.4f}'.format(amount)}", money=True)
        except Exception as e:
            self.print_and_log(message=f"{wallet}: Could not move to flexible savings {productId} {'${:,.4f}'.format(amount)}", e=e)
        print()




###################################################################################################
### ROUND ###
###################################################################################################

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

from util.log       import Log
from util.error_log import ErrorLog
from datetime       import datetime

CONFIG_FILE = 'config.txt'

"""
Parses CONFIG_FILE for all keys used in Anti-Liquidation bot
    CONFIG_FILE should be in this format:

        binance_api_key                = "ENTER BINANCE API KEY HERE"
        binance_secret_key             = "ENTER BINANCE SECRET KEY HERE"
        twilio_account_sid             = "ENTER TWILIO SID HERE"
        twilio_auth_token              = "ENTER TWILIO AUTH TOKEN HERE"
        twilio_bot_phonenumber         = "ENTER TWILIO BOT PHONE NUMBER HERE (+15823262015)"
        my_cell_number                 = "ENTER YOUR CELL PHONE NUMBER HERE (+12523459832)"

        spot_rake             		            = True
        spot_rake_percent    		            = 0.05
        spot_rake_threshold_percent             = 0.5
        spot_rake_time        		            = 0.3
        spot_rake_blacklist    		            = "HNT"

        margin_cross_rake     	     	        = True
        margin_cross_move_asset_on_repay        = True
        margin_cross_rake_percent   	        = 0.1
        margin_cross_rake_threshold_percent     = 0.5
        margin_cross_rake_time        		    = 58
        margin_cross_rake_blacklist    	        = ""

        margin_isolated_rake   		            = True
        margin_isolated_move_asset_on_repay     = True
        margin_isolated_rake_percent		    = 0.1
        margin_isolated_rake_threshold_percent  = 0.5
        margin_isolated_rake_time     		    = 56
        margin_isolated_rake_blacklist 	        = ""

        futures_isolated_rake           		= True
        futures_isolated_rake_percent  		    = 0.3
        futures_isolated_rake_threshold_percent = 0.75
        futures_isolated_rake_time      	    = 1
        futures_isolated_rake_blacklist  	    = ""
        futures_isolated_stop_in_profit_percent = 0.25

        futures_isolated_auto_deleverage_percent     = 50
        futures_isolated_deleverage_quantity_percent = 25

        rake_tip_percent = 1

"""


class ConfigParser():
    def __init__(self, log_file: Log, error_file: ErrorLog):
        self.log_file   = log_file
        self.error_file = error_file
        
        self.binance_api_key                              = "binance_api_key"
        self.binance_secret_key                           = "binance_secret_key"
        self.threecommas_api_key                          = "threecommas_api_key"
        self.threecommas_secret_key                       = "threecommas_secret_key"
        self.twilio_account_sid                           = "twilio_account_sid"
        self.twilio_auth_token                            = "twilio_auth_token"
        self.twilio_bot_phonenumber                       = "twilio_bot_phonenumber"
        self.my_cell_number                               = "my_cell_number"
             
        self.rake_tip_percent                             = "rake_tip_percent"
             
        self.spot_rake                                    = "spot_rake"
        self.margin_cross_rake                            = "margin_cross_rake"
        self.margin_isolated_rake                         = "margin_isolated_rake"
        self.futures_isolated_rake                        = "futures_isolated_rake"
             
        self.spot_rake_percent                            = "spot_rake_percent"
        self.margin_cross_rake_percent                    = "margin_cross_rake_percent"
        self.margin_isolated_rake_percent                 = "margin_isolated_rake_percent"
        self.futures_isolated_rake_percent                = "futures_isolated_rake_percent"
     
        self.spot_rake_time                               = "spot_rake_time"
        self.margin_cross_rake_time                       = "margin_cross_rake_time"
        self.margin_isolated_rake_time                    = "margin_isolated_rake_time"
        self.futures_isolated_rake_time                   = "futures_isolated_rake_time"
     
        self.futures_isolated_stop_in_profit_percent      = "futures_isolated_stop_in_profit_percent"
     
        self.spot_rake_threshold_percent                  = "spot_rake_threshold_percent"
        self.margin_cross_rake_threshold_percent          = "margin_cross_rake_threshold_percent"
        self.margin_isolated_rake_threshold_percent       = "margin_isolated_rake_threshold_percent"
        self.futures_isolated_rake_threshold_percent      = "futures_isolated_rake_threshold_percent"
             
        self.spot_rake_blacklist                          = "spot_rake_blacklist"
        self.margin_cross_rake_blacklist                  = "margin_cross_rake_blacklist"
        self.margin_isolated_rake_blacklist               = "margin_isolated_rake_blacklist"
        self.futures_isolated_rake_blacklist              = "futures_isolated_rake_blacklist"
             
        self.margin_isolated_move_asset_on_repay          = "margin_isolated_move_asset_on_repay"
        self.margin_cross_move_asset_on_repay             = "margin_cross_move_asset_on_repay"

        self.futures_isolated_stop_in_profit              = "futures_isolated_stop_in_profit"
        self.futures_isolated_auto_deleverage             = "futures_isolated_auto_deleverage"
        self.futures_isolated_auto_deleverage_percent     = "futures_isolated_auto_deleverage_percent"
        self.futures_isolated_deleverage_quantity_percent = "futures_isolated_deleverage_quantity_percent"


    def get_current_time(self):
        return datetime.now().strftime("%H:%M:%S")


    def parse_config_file(self):
        """Read from CONFIG_FILE. Strips out an unnecessary characters and store key/value pairs in dictionary.
             Args can be rearranged to the users desire"""
        
        parameter_dict = dict()
        
        parameter_list = [ self.binance_api_key, 
                           self.binance_secret_key, 
                           self.threecommas_api_key, 
                           self.threecommas_secret_key, 
                           self.twilio_account_sid, 
                           self.twilio_auth_token, 
                           self.twilio_bot_phonenumber, 
                           self.my_cell_number, 

                           self.spot_rake,
                           self.margin_cross_rake,
                           self.margin_isolated_rake,
                           self.futures_isolated_rake, 

                           self.rake_tip_percent,
                           
                           self.spot_rake_time,
                           self.margin_cross_rake_time,
                           self.margin_isolated_rake_time,
                           self.futures_isolated_rake_time,
                           
                           self.spot_rake_percent,
                           self.margin_cross_rake_percent,
                           self.margin_isolated_rake_percent,
                           self.futures_isolated_rake_percent,

                           self.spot_rake_threshold_percent,
                           self.margin_cross_rake_threshold_percent,
                           self.margin_isolated_rake_threshold_percent,
                           self.futures_isolated_rake_threshold_percent,

                           self.futures_isolated_stop_in_profit_percent,
                           
                           self.spot_rake_blacklist,
                           self.margin_cross_rake_blacklist,
                           self.margin_isolated_rake_blacklist,
                           self.futures_isolated_rake_blacklist,
                           
                           self.margin_isolated_move_asset_on_repay,
                           self.margin_cross_move_asset_on_repay,
                           
                           self.futures_isolated_stop_in_profit,
                           self.futures_isolated_auto_deleverage,
                           self.futures_isolated_auto_deleverage_percent,
                           self.futures_isolated_deleverage_quantity_percent]
                           

        try:
            with open(CONFIG_FILE, mode='r') as file:
                lines       = file.readlines()
                removed_set = set()
                
                for line in lines:
                    edited_line = line.replace("\n", "").replace("\t", "").replace(" ", "").replace('"', "").replace("=", "")
                    for param in parameter_list:
                        if param in edited_line and param not in removed_set:
                            edited_line = edited_line.replace(param, "")
                            parameter_dict[param] = edited_line
                            removed_set.add(param)
                            break
            return parameter_dict

        except Exception as e:
            self.log_file.write(f"[!] {self.get_current_time()} {e}, {type(e).__name__}, {__file__}, {e.__traceback__.tb_lineno}")
            self.error_file.write(f"{self.get_current_time()} {e}, {type(e).__name__}, {__file__}, {e.__traceback__.tb_lineno}")
            exit()
    
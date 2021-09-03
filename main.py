import signal
import os
import sys

from threading          import Thread, Event
from datetime           import datetime

from util.log           import Log
from util.error_log     import ErrorLog
from util.config_parser import ConfigParser
from util.enums         import *

from wallets.spot             import Spot
from wallets.margin_isolated  import MarginIsolated
from wallets.margin_cross     import MarginCross
from wallets.futures_isolated import FuturesIsolated

g_thread_dict       = dict()
g_thread_exit_event = Event()
g_log_file          = Log()
g_error_file        = ErrorLog()



def get_current_time():
    return datetime.now().strftime("%H:%M:%S")


def signal_handler(signum, frame):
    global g_thread_exit_event
    global g_log_file

    print(           f"[+] {get_current_time()} in signal_handler")
    g_log_file.write(f"[*] {get_current_time()} in signal handler")
    signal.signal(signum, signal.SIG_IGN) # ignore additional signals
    g_thread_exit_event.set()


def print_and_log(message, money=False, e=False, end=False):
    global g_log_file
    global g_error_file

    if money:
        print(           f"[$] {get_current_time()} {message}")
        g_log_file.write(f"[$] {get_current_time()} {message}")
        return
    if e:
        print(           f"[!] {get_current_time()} ERROR: {message}")
        g_log_file.write(f"[!] {get_current_time()} ERROR: {message}")
        g_log_file.write(f"[!] {get_current_time()} {type(e).__name__}, {__file__}, {e.__traceback__.tb_lineno}")

        g_error_file.write(f"{get_current_time()} {e}, {type(e).__name__}, {__file__}, {e.__traceback__.tb_lineno}")
        return
    if end:
        print(           f"[-] {get_current_time()} {message}")
        g_log_file.write(f"[-] {get_current_time()} {message}")
        return

    print(           f"[*] {get_current_time()} {message}")
    g_log_file.write(f"[*] {get_current_time()} {message}")


def windows_sync_time():
    """Sync windows time in case we get disconnected from Binance API"""
    global g_log_file

    if sys.platform == "linux" or sys.platform == "linux2":
        # linux
        print_and_log("Futures Manual Assistant is not build for linux. Please run on a Windows machine")
        exit()
    elif sys.platform == "darwin":
        # OS X
        print_and_log("Futures Manual Assistant is not build for OS X. Please run on a Windows machine")
        exit()
    elif sys.platform == "win32":
        # Windows...
        try:
            # https://docs.microsoft.com/en-us/troubleshoot/windows-server/identity/error-message-run-w32tm-resync-no-time-data-available
            # https://bwit.blog/tutorial-sync-server-time-ntp/
            print_and_log("w32tm /resync")

            if os.system("w32tm /resync") != 0:
                print_and_log("windows time sync failed")
                print_and_log("configuring windows time sync")
                os.system("w32tm /config /manualpeerlist:time.nist.gov /syncfromflags:manual /reliable:yes /update")
                os.system("Net stop w32time")
                os.system("Net start w32time")
            else:
                print_and_log("windows time sync successful")
        except Exception as e:
            print_and_log(message="failed to sync windows time", e=e)
    else:
        print_and_log(f"Futures Manual Assistant is not build for {str(sys.platform)}. Please run on a Windows machine")
        exit()


def init_rake_threads():
    global g_thread_dict
    global g_thread_exit_event
    global g_log_file
    global g_error_file

    cfg_dict = ConfigParser(g_log_file, g_error_file).parse_config_file()

    if RAKE_SPOT:
        spot_wallet = Spot(parameter_dict=cfg_dict, exit_event=g_thread_exit_event, log_file=g_log_file, error_file=g_error_file)
        g_thread_dict["spot"] = Thread(target=spot_wallet.rake_spot)

    if RAKE_MARGIN_ISOLATED:
        margin_isolated_wallet = MarginIsolated(parameter_dict=cfg_dict, exit_event=g_thread_exit_event, log_file=g_log_file, error_file=g_error_file)
        g_thread_dict["margin_isolated"] = Thread(target=margin_isolated_wallet.rake_margin_isolated)

    if RAKE_MARGIN_CROSS:
        margin_cross_wallet = MarginCross(parameter_dict=cfg_dict, exit_event=g_thread_exit_event, log_file=g_log_file, error_file=g_error_file)
        g_thread_dict["margin_cross"] = Thread(target=margin_cross_wallet.rake_margin_cross)

    if RAKE_FUTURES_ISOLATED:
        futures_isolated_wallet = FuturesIsolated(parameter_dict=cfg_dict, exit_event=g_thread_exit_event, log_file=g_log_file, error_file=g_error_file)
        g_thread_dict["futures_isolated"] = Thread(target=futures_isolated_wallet.rake_futures_isolated)


    for thread in g_thread_dict.values():
        thread.start()

    for thread in g_thread_dict.values(): 
        thread.join()



#######################################################################################
### MAIN ###
#######################################################################################

if __name__ == "__main__":
    os.system("cls")

    print("""
#######################################################################
                            Starting Rake!
#######################################################################""")

    g_log_file.directory_create()
    g_log_file.file_create()

    g_error_file.directory_create()
    g_error_file.file_create()

    print_and_log("Sync windows time on startup")
    windows_sync_time()
    
    signal.signal(signal.SIGINT, signal_handler)
    
    init_rake_threads()

    print_and_log(message="Exiting main thread")
    
from util.log           import Log
from util.error_log     import ErrorLog
from util.config_parser import ConfigParser

g_cfg_dict = ConfigParser(Log(), ErrorLog()).parse_config_file()


RECV_WINDOW                   = 10000
FLEXIBLE_SAVINGS_USDT_MIN     = 0.10
USDT_TRANSFER_MIN             = 0.0000001

SPOT_NOTIONAL_MIN             = 10.1
MARGIN_CROSS_NOTIONAL_MIN     = 10.1
MARGIN_ISOLATED_NOTIONAL_MIN  = 10.1
FUTURES_NOTIONAL_MIN          = 5.1

NOTHING                       = 0.0
NAP                           = 1     # Jesus took naps, be like Jesus...
LONG_NAP                      = 2     # Jesus took naps, be like Jesus...

# misc terms
USDT                          = "USDT"
ISOLATED_MARGIN               = "ISOLATED_MARGIN"
SPOT                          = "SPOT"
CROSS                         = "cross"
ISOLATED                      = "isolated"
STOP_MARKET                   = "STOP_MARKET"
SELL                          = "SELL"
BUY                           = "BUY"
MARKET                        = "MARKET"
LIMIT                         = "LIMIT"
GTC                           = "GTC"

# wallets
SPOT                          = "SPOT"
MARGIN_ISOLATED               = "MARGIN ISOLATED"
MARGIN_CROSS                  = "MARGIN CROSS"
FUTURES_ISOLATED              = "FUTURES ISOLATED"

# mainly for futures
MARK_PRICE                    = "markPrice"
ENTRY_PRICE                   = "entryPrice"
QUANTITY                      = "positionAmt"
SYMBOL                        = "symbol"
UNREALIZED_PROFIT             = "unRealizedProfit"
MARGIN_TYPE                   = "marginType"
ISOLATED_MARGIN               = "isolatedMargin"
LIQUIDATION_PRICE             = "liquidationPrice"
LONG                          = "Long"
SHORT                         = "Short"

CONFIG_FILE                   = "config.txt"
RAKED_TRADES_FILE             = "logs\\raked_trades.txt"

# stables coins that are 1:1 with the US dollar
STABLE_COINS_LIST             = ['USDT', 'BUSD', 'PAX', 'USDC', 'USD', 'TUSD', 'DAI', 'UST', 'HUSD', 'USDN', 'GUSD', 'FEI',  'LUSD', 'FRAX','SUSD', 'USDX','MUSD', 'USDK','USDS','USDP', 'RSV',  'USDQ', 'USDEX']

# entry prices files
SPOT_ENTRY_PRICES             = "entry_prices/spot_entry_prices.txt"
MARGIN_CROSS_ENTRY_PRICES     = "entry_prices/margin_cross_entry_prices.txt"
MARGIN_ISOLATED_ENTRY_PRICES  = "entry_prices/margin_isolated_entry_prices.txt"

# Min trade/Max prec dictionaries
SPOT_MIN_TRADE_AMOUNTS_DICT   = {'BTC/USDT': '0.000001', 'ETH/USDT': '0.00001', 'BNB/USDT': '0.0001', 'NEO/USDT': '0.001', 'LTC/USDT': '0.00001', 'QTUM/USDT': '0.001', 'ADA/USDT': '0.01', 'XRP/USDT': '0.01', 'EOS/USDT': '0.01', 'TUSD/USDT': '0.01', 'IOTA/USDT': '0.01', 'XLM/USDT': '0.1', 'ONT/USDT': '0.01', 'TRX/USDT': '0.1', 'ETC/USDT': '0.001', 'ICX/USDT': '0.01', 'NULS/USDT': '0.01', 'VET/USDT': '0.1', 'PAX/USDT': '0.01', 'USDC/USDT': '0.01', 'LINK/USDT': '0.001', 'WAVES/USDT': '0.001', 'BTT/USDT': '1', 'ONG/USDT': '0.01', 'HOT/USDT': '1', 'ZIL/USDT': '0.1', 'ZRX/USDT': '0.01', 'FET/USDT': '0.1', 'BAT/USDT': '0.01', 'XMR/USDT': '0.00001', 'ZEC/USDT': '0.00001', 'IOST/USDT': '1', 'CELR/USDT': '0.1', 'DASH/USDT': '0.00001', 'NANO/USDT': '0.01', 'OMG/USDT': '0.01', 'THETA/USDT': '0.001', 'ENJ/USDT': '0.01', 'MITH/USDT': '0.1', 'MATIC/USDT': '0.1', 'ATOM/USDT': '0.001', 'TFUEL/USDT': '0.1', 'ONE/USDT': '0.1', 'FTM/USDT': '0.1', 'ALGO/USDT': '0.01', 'GTO/USDT': '0.1', 'DOGE/USDT': '0.1', 'DUSK/USDT': '0.01', 'ANKR/USDT': '0.1', 'WIN/USDT': '1', 'COS/USDT': '0.1', 'COCOS/USDT': '0.01', 'MTL/USDT': '0.01', 'TOMO/USDT': '0.01', 'PERL/USDT': '0.1', 'DENT/USDT': '1', 'MFT/USDT': '1', 'KEY/USDT': '1', 'DOCK/USDT': '1', 'WAN/USDT': '0.01', 'FUN/USDT': '1', 'CVC/USDT': '0.1', 'CHZ/USDT': '0.1', 'BAND/USDT': '0.001', 'BUSD/USDT': '0.01', 'BEAM/USDT': '0.01', 'XTZ/USDT': '0.01', 'REN/USDT': '0.1', 'RVN/USDT': '0.1', 'HBAR/USDT': '0.1', 'NKN/USDT': '0.1', 'STX/USDT': '0.01', 'KAVA/USDT': '0.01', 'ARPA/USDT': '0.1', 'IOTX/USDT': '1', 'RLC/USDT': '0.01', 'CTXC/USDT': '0.01', 'BCH/USDT': '0.00001', 'TROY/USDT': '1', 'VITE/USDT': '0.1', 'FTT/USDT': '0.001', 'EUR/USDT': '0.01', 'OGN/USDT': '0.01', 'DREP/USDT': '0.001', 'TCT/USDT': '1', 'WRX/USDT': '0.01', 'BTS/USDT': '0.1', 'LSK/USDT': '0.01', 'BNT/USDT': '0.01', 'LTO/USDT': '0.1', 'AION/USDT': '0.01', 'MBL/USDT': '1', 'COTI/USDT': '0.1', 'STPT/USDT': '0.1', 'WTC/USDT': '0.01', 'DATA/USDT': '0.1', 'SOL/USDT': '0.001', 'CTSI/USDT': '0.1', 'HIVE/USDT': '0.01', 'CHR/USDT': '0.1', 'BTCUP/USDT': '0.01', 'BTCDOWN/USDT': '0.01', 'GXS/USDT': '0.01', 'ARDR/USDT': '0.1', 'MDT/USDT': '0.1', 'STMX/USDT': '1', 'KNC/USDT': '0.001', 'REP/USDT': '0.001', 'LRC/USDT': '0.1', 'PNT/USDT': '0.01', 'COMP/USDT': '0.00001', 'SC/USDT': '1', 'ZEN/USDT': '0.0001', 'SNX/USDT': '0.001', 'ETHUP/USDT': '0.01', 'ETHDOWN/USDT': '0.01', 'ADAUP/USDT': '0.01', 'ADADOWN/USDT': '0.01', 'LINKUP/USDT': '0.01', 'LINKDOWN/USDT': '0.01', 'VTHO/USDT': '1', 'DGB/USDT': '0.1', 'GBP/USDT': '0.01', 'SXP/USDT': '0.001', 'MKR/USDT': '0.00001', 'DCR/USDT': '0.0001', 'STORJ/USDT': '0.01', 'BNBUP/USDT': '0.01', 'BNBDOWN/USDT': '0.01', 'XTZUP/USDT': '0.01', 'XTZDOWN/USDT': '0.01', 'MANA/USDT': '0.01', 'AUD/USDT': '0.1', 'YFI/USDT': '0.000001', 'BAL/USDT': '0.001', 'BLZ/USDT': '0.1', 'IRIS/USDT': '0.1', 'KMD/USDT': '0.01', 'JST/USDT': '0.1', 'SRM/USDT': '0.01', 'ANT/USDT': '0.01', 'CRV/USDT': '0.001', 'SAND/USDT': '0.1', 'OCEAN/USDT': '0.01', 'NMR/USDT': '0.001', 'DOT/USDT': '0.001', 'LUNA/USDT': '0.001', 'RSR/USDT': '0.1', 'PAXG/USDT': '0.000001', 'WNXM/USDT': '0.001', 'TRB/USDT': '0.001', 'BZRX/USDT': '0.01', 'SUSHI/USDT': '0.001', 'YFII/USDT': '0.000001', 'KSM/USDT': '0.0001', 'EGLD/USDT': '0.0001', 'DIA/USDT': '0.001', 'RUNE/USDT': '0.001', 'FIO/USDT': '0.01', 'UMA/USDT': '0.001', 'EOSUP/USDT': '0.01', 'EOSDOWN/USDT': '0.01', 'TRXUP/USDT': '0.01', 'TRXDOWN/USDT': '0.01', 'XRPUP/USDT': '0.01', 'XRPDOWN/USDT': '0.01', 'DOTUP/USDT': '0.01', 'DOTDOWN/USDT': '0.01', 'BEL/USDT': '0.01', 'WING/USDT': '0.001', 'LTCUP/USDT': '0.01', 'LTCDOWN/USDT': '0.01', 'UNI/USDT': '0.001', 'NBS/USDT': '0.1', 'OXT/USDT': '0.01', 'SUN/USDT': '1', 'AVAX/USDT': '0.001', 'HNT/USDT': '0.001', 'FLM/USDT': '0.01', 'UNIUP/USDT': '0.01', 'UNIDOWN/USDT': '0.01', 'ORN/USDT': '0.001', 'UTK/USDT': '0.01', 'XVS/USDT': '0.001', 'ALPHA/USDT': '0.01', 'AAVE/USDT': '0.0001', 'NEAR/USDT': '0.01', 'SXPUP/USDT': '0.01', 'SXPDOWN/USDT': '0.01', 'FIL/USDT': '0.0001', 'FILUP/USDT': '0.01', 'FILDOWN/USDT': '0.01', 'YFIUP/USDT': '0.01', 'YFIDOWN/USDT': '0.01', 'INJ/USDT': '0.001', 'AUDIO/USDT': '0.01', 'CTK/USDT': '0.01', 'BCHUP/USDT': '0.01', 'BCHDOWN/USDT': '0.01', 'AKRO/USDT': '1', 'AXS/USDT': '0.01', 'HARD/USDT': '0.01', 'DNT/USDT': '0.1', 'STRAX/USDT': '0.01', 'UNFI/USDT': '0.001', 'ROSE/USDT': '0.1', 'AVA/USDT': '0.01', 'XEM/USDT': '0.01', 'AAVEUP/USDT': '0.01', 'AAVEDOWN/USDT': '0.01', 'SKL/USDT': '0.1', 'SUSD/USDT': '0.01', 'SUSHIUP/USDT': '0.01', 'SUSHIDOWN/USDT': '0.01', 'XLMUP/USDT': '0.01', 'XLMDOWN/USDT': '0.01', 'GRT/USDT': '0.01', 'JUV/USDT': '0.001', 'PSG/USDT': '0.001', '1INCH/USDT': '0.01', 'REEF/USDT': '1', 'OG/USDT': '0.001', 'ATM/USDT': '0.001', 'ASR/USDT': '0.001', 'CELO/USDT': '0.01', 'RIF/USDT': '0.01', 'BTCST/USDT': '0.001', 'TRU/USDT': '0.01', 'CKB/USDT': '1', 'TWT/USDT': '0.01', 'FIRO/USDT': '0.001', 'LIT/USDT': '0.01', 'SFP/USDT': '0.01', 'DODO/USDT': '0.001', 'CAKE/USDT': '0.001', 'ACM/USDT': '0.001', 'BADGER/USDT': '0.001', 'FIS/USDT': '0.001', 'OM/USDT': '0.01', 'POND/USDT': '0.01', 'DEGO/USDT': '0.001', 'ALICE/USDT': '0.01', 'LINA/USDT': '0.01', 'PERP/USDT': '0.001', 'RAMP/USDT': '0.01', 'SUPER/USDT': '0.001', 'CFX/USDT': '0.001', 'EPS/USDT': '0.001', 'AUTO/USDT': '0.000001', 'TKO/USDT': '0.01', 'PUNDIX/USDT': '0.001', 'TLM/USDT': '0.01', '1INCHUP/USDT': '0.01', '1INCHDOWN/USDT': '0.01', 'BTG/USDT': '0.001', 'MIR/USDT': '0.001', 'BAR/USDT': '0.001', 'FORTH/USDT': '0.001', 'BAKE/USDT': '0.1', 'BURGER/USDT': '0.1', 'SLP/USDT': '1', 'SHIB/USDT': '1', 'ICP/USDT': '0.01', 'AR/USDT': '0.01', 'POLS/USDT': '0.01', 'MDX/USDT': '0.01', 'MASK/USDT': '0.01', 'LPT/USDT': '0.01', 'NU/USDT': '1', 'XVG/USDT': '1', 'ATA/USDT': '1', 'GTC/USDT': '0.01', 'TORN/USDT': '0.01', 'KEEP/USDT': '1', 'ERN/USDT': '0.1', 'KLAY/USDT': '1', 'PHA/USDT': '1'}
SPOT_MAX_PRECISION_DICT       = {'BTC/USDT': '0.01', 'ETH/USDT': '0.01', 'BNB/USDT': '0.01', 'NEO/USDT': '0.001', 'LTC/USDT': '0.01', 'QTUM/USDT': '0.001', 'ADA/USDT': '0.0001', 'XRP/USDT': '0.0001', 'EOS/USDT': '0.0001', 'TUSD/USDT': '0.0001', 'IOTA/USDT': '0.0001', 'XLM/USDT': '0.00001', 'ONT/USDT': '0.0001', 'TRX/USDT': '0.00001', 'ETC/USDT': '0.001', 'ICX/USDT': '0.0001', 'NULS/USDT': '0.0001', 'VET/USDT': '0.00001', 'PAX/USDT': '0.0001', 'USDC/USDT': '0.0001', 'LINK/USDT': '0.001', 'WAVES/USDT': '0.001', 'BTT/USDT': '0.0000001', 'ONG/USDT': '0.0001', 'HOT/USDT': '0.000001', 'ZIL/USDT': '0.00001', 'ZRX/USDT': '0.0001', 'FET/USDT': '0.00001', 'BAT/USDT': '0.0001', 'XMR/USDT': '0.01', 'ZEC/USDT': '0.01', 'IOST/USDT': '0.000001', 'CELR/USDT': '0.00001', 'DASH/USDT': '0.01', 'NANO/USDT': '0.0001', 'OMG/USDT': '0.0001', 'THETA/USDT': '0.001', 'ENJ/USDT': '0.0001', 'MITH/USDT': '0.00001', 'MATIC/USDT': '0.00001', 'ATOM/USDT': '0.001', 'TFUEL/USDT': '0.00001', 'ONE/USDT': '0.00001', 'FTM/USDT': '0.00001', 'ALGO/USDT': '0.0001', 'GTO/USDT': '0.00001', 'DOGE/USDT': '0.00001', 'DUSK/USDT': '0.0001', 'ANKR/USDT': '0.00001', 'WIN/USDT': '0.0000001', 'COS/USDT': '0.00001', 'COCOS/USDT': '0.0001', 'MTL/USDT': '0.0001', 'TOMO/USDT': '0.0001', 'PERL/USDT': '0.00001', 'DENT/USDT': '0.0000001', 'MFT/USDT': '0.000001', 'KEY/USDT': '0.000001', 'DOCK/USDT': '0.000001', 'WAN/USDT': '0.0001', 'FUN/USDT': '0.000001', 'CVC/USDT': '0.00001', 'CHZ/USDT': '0.00001', 'BAND/USDT': '0.001', 'BUSD/USDT': '0.0001', 'BEAM/USDT': '0.0001', 'XTZ/USDT': '0.0001', 'REN/USDT': '0.00001', 'RVN/USDT': '0.00001', 'HBAR/USDT': '0.00001', 'NKN/USDT': '0.00001', 'STX/USDT': '0.0001', 'KAVA/USDT': '0.0001', 'ARPA/USDT': '0.00001', 'IOTX/USDT': '0.000001', 'RLC/USDT': '0.0001', 'CTXC/USDT': '0.0001', 'BCH/USDT': '0.01', 'TROY/USDT': '0.000001', 'VITE/USDT': '0.00001', 'FTT/USDT': '0.001', 'EUR/USDT': '0.0001', 'OGN/USDT': '0.0001', 'DREP/USDT': '0.001', 'TCT/USDT': '0.000001', 'WRX/USDT': '0.0001', 'BTS/USDT': '0.00001', 'LSK/USDT': '0.0001', 'BNT/USDT': '0.0001', 'LTO/USDT': '0.00001', 'AION/USDT': '0.0001', 'MBL/USDT': '0.000001', 'COTI/USDT': '0.00001', 'STPT/USDT': '0.00001', 'WTC/USDT': '0.0001', 'DATA/USDT': '0.00001', 'SOL/USDT': '0.001', 'CTSI/USDT': '0.00001', 'HIVE/USDT': '0.0001', 'CHR/USDT': '0.00001', 'BTCUP/USDT': '0.001', 'BTCDOWN/USDT': '0.00001', 'GXS/USDT': '0.0001', 'ARDR/USDT': '0.00001', 'MDT/USDT': '0.00001', 'STMX/USDT': '0.000001', 'KNC/USDT': '0.001', 'REP/USDT': '0.001', 'LRC/USDT': '0.00001', 'PNT/USDT': '0.0001', 'COMP/USDT': '0.01', 'SC/USDT': '0.000001', 'ZEN/USDT': '0.01', 'SNX/USDT': '0.001', 'ETHUP/USDT': '0.001', 'ETHDOWN/USDT': '0.000001', 'ADAUP/USDT': '0.001', 'ADADOWN/USDT': '0.0001', 'LINKUP/USDT': '0.001', 'LINKDOWN/USDT': '0.0001', 'VTHO/USDT': '0.000001', 'DGB/USDT': '0.00001', 'GBP/USDT': '0.0001', 'SXP/USDT': '0.001', 'MKR/USDT': '0.01', 'DCR/USDT': '0.01', 'STORJ/USDT': '0.0001', 'BNBUP/USDT': '0.001', 'BNBDOWN/USDT': '0.001', 'XTZUP/USDT': '0.001', 'XTZDOWN/USDT': '0.00001', 'MANA/USDT': '0.0001', 'AUD/USDT': '0.00001', 'YFI/USDT': '0.01', 'BAL/USDT': '0.001', 'BLZ/USDT': '0.00001', 'IRIS/USDT': '0.00001', 'KMD/USDT': '0.0001', 'JST/USDT': '0.00001', 'SRM/USDT': '0.0001', 'ANT/USDT': '0.0001', 'CRV/USDT': '0.001', 'SAND/USDT': '0.00001', 'OCEAN/USDT': '0.0001', 'NMR/USDT': '0.001', 'DOT/USDT': '0.001', 'LUNA/USDT': '0.001', 'RSR/USDT': '0.00001', 'PAXG/USDT': '0.01', 'WNXM/USDT': '0.001', 'TRB/USDT': '0.001', 'BZRX/USDT': '0.0001', 'SUSHI/USDT': '0.001', 'YFII/USDT': '0.01', 'KSM/USDT': '0.01', 'EGLD/USDT': '0.01', 'DIA/USDT': '0.001', 'RUNE/USDT': '0.001', 'FIO/USDT': '0.0001', 'UMA/USDT': '0.001', 'EOSUP/USDT': '0.001', 'EOSDOWN/USDT': '0.00001', 'TRXUP/USDT': '0.001', 'TRXDOWN/USDT': '0.000001', 'XRPUP/USDT': '0.001', 'XRPDOWN/USDT': '0.000001', 'DOTUP/USDT': '0.001', 'DOTDOWN/USDT': '0.0001', 'BEL/USDT': '0.0001', 'WING/USDT': '0.001', 'LTCUP/USDT': '0.001', 'LTCDOWN/USDT': '0.000001', 'UNI/USDT': '0.001', 'NBS/USDT': '0.00001', 'OXT/USDT': '0.0001', 'SUN/USDT': '0.00001', 'AVAX/USDT': '0.001', 'HNT/USDT': '0.001', 'FLM/USDT': '0.0001', 'UNIUP/USDT': '0.001', 'UNIDOWN/USDT': '0.000001', 'ORN/USDT': '0.001', 'UTK/USDT': '0.0001', 'XVS/USDT': '0.001', 'ALPHA/USDT': '0.0001', 'AAVE/USDT': '0.01', 'NEAR/USDT': '0.0001', 'SXPUP/USDT': '0.0001', 'SXPDOWN/USDT': '0.001', 'FIL/USDT': '0.01', 'FILUP/USDT': '0.001', 'FILDOWN/USDT': '0.000001', 'YFIUP/USDT': '0.001', 'YFIDOWN/USDT': '0.0001', 'INJ/USDT': '0.001', 'AUDIO/USDT': '0.0001', 'CTK/USDT': '0.0001', 'BCHUP/USDT': '0.001', 'BCHDOWN/USDT': '0.001', 'AKRO/USDT': '0.000001', 'AXS/USDT': '0.0001', 'HARD/USDT': '0.0001', 'DNT/USDT': '0.00001', 'STRAX/USDT': '0.0001', 'UNFI/USDT': '0.001', 'ROSE/USDT': '0.00001', 'AVA/USDT': '0.0001', 'XEM/USDT': '0.0001', 'AAVEUP/USDT': '0.001', 'AAVEDOWN/USDT': '0.0001', 'SKL/USDT': '0.00001', 'SUSD/USDT': '0.0001', 'SUSHIUP/USDT': '0.001', 'SUSHIDOWN/USDT': '0.0000001', 'XLMUP/USDT': '0.001', 'XLMDOWN/USDT': '0.000001', 'GRT/USDT': '0.0001', 'JUV/USDT': '0.001', 'PSG/USDT': '0.001', '1INCH/USDT': '0.0001', 'REEF/USDT': '0.000001', 'OG/USDT': '0.001', 'ATM/USDT': '0.001', 'ASR/USDT': '0.001', 'CELO/USDT': '0.0001', 'RIF/USDT': '0.0001', 'BTCST/USDT': '0.001', 'TRU/USDT': '0.0001', 'CKB/USDT': '0.000001', 'TWT/USDT': '0.0001', 'FIRO/USDT': '0.001', 'LIT/USDT': '0.0001', 'SFP/USDT': '0.0001', 'DODO/USDT': '0.001', 'CAKE/USDT': '0.001', 'ACM/USDT': '0.001', 'BADGER/USDT': '0.001', 'FIS/USDT': '0.001', 'OM/USDT': '0.0001', 'POND/USDT': '0.0001', 'DEGO/USDT': '0.001', 'ALICE/USDT': '0.0001', 'LINA/USDT': '0.0001', 'PERP/USDT': '0.001', 'RAMP/USDT': '0.0001', 'SUPER/USDT': '0.001', 'CFX/USDT': '0.001', 'EPS/USDT': '0.001', 'AUTO/USDT': '0.01', 'TKO/USDT': '0.0001', 'PUNDIX/USDT': '0.001', 'TLM/USDT': '0.0001', '1INCHUP/USDT': '0.000001', '1INCHDOWN/USDT': '0.001', 'BTG/USDT': '0.001', 'MIR/USDT': '0.001', 'BAR/USDT': '0.001', 'FORTH/USDT': '0.001', 'BAKE/USDT': '0.0001', 'BURGER/USDT': '0.01', 'SLP/USDT': '0.0001', 'SHIB/USDT': '0.00000001', 'ICP/USDT': '0.01', 'AR/USDT': '0.001', 'POLS/USDT': '0.001', 'MDX/USDT': '0.0001', 'MASK/USDT': '0.001', 'LPT/USDT': '0.01', 'NU/USDT': '0.0001', 'XVG/USDT': '0.00001', 'ATA/USDT': '0.00001', 'GTC/USDT': '0.01', 'TORN/USDT': '0.01', 'KEEP/USDT': '0.0001', 'ERN/USDT': '0.001', 'KLAY/USDT': '0.0001', 'PHA/USDT': '0.0001'}

# this is the smallest quantity that we can trade in terms of the given coin
FUTURES_MIN_TRADE_DICT        = {'BTCUSDT': '0.001', 'ETHUSDT': '0.001', 'BCHUSDT': '0.001', 'XRPUSDT': '0.1', 'EOSUSDT': '0.1', 'LTCUSDT': '0.001', 'TRXUSDT': '1', 'ETCUSDT': '0.01', 'LINKUSDT': '0.01', 'XLMUSDT': '1', 'ADAUSDT': '1', 'XMRUSDT': '0.001', 'DASHUSDT': '0.001', 'ZECUSDT': '0.001', 'XTZUSDT': '0.1', 'BNBUSDT': '0.01', 'ATOMUSDT': '0.01', 'ONTUSDT': '0.1', 'IOTAUSDT': '0.1', 'BATUSDT': '0.1', 'VETUSDT': '1', 'NEOUSDT': '0.01', 'QTUMUSDT': '0.1', 'IOSTUSDT': '1', 'THETAUSDT': '0.1', 'ALGOUSDT': '0.1', 'ZILUSDT': '1', 'KNCUSDT': '1', 'ZRXUSDT': '0.1', 'COMPUSDT': '0.001', 'OMGUSDT': '0.1', 'DOGEUSDT': '1', 'SXPUSDT': '0.1', 'KAVAUSDT': '0.1', 'BANDUSDT': '0.1', 'RLCUSDT': '0.1', 'WAVESUSDT': '0.1', 'MKRUSDT': '0.001', 'SNXUSDT': '0.1', 'DOTUSDT': '0.1', 'DEFIUSDT': '0.001', 'YFIUSDT': '0.001', 'BALUSDT': '0.1', 'CRVUSDT': '0.1', 'TRBUSDT': '0.1', 'YFIIUSDT': '0.001', 'RUNEUSDT': '1', 'SUSHIUSDT': '1', 'SRMUSDT': '1', 'BZRXUSDT': '1', 'EGLDUSDT': '0.1', 'SOLUSDT': '1', 'ICXUSDT': '1', 'STORJUSDT': '1', 'BLZUSDT': '1', 'UNIUSDT': '1', 'AVAXUSDT': '1', 'FTMUSDT': '1', 'HNTUSDT': '1', 'ENJUSDT': '1', 'FLMUSDT': '1', 'TOMOUSDT': '1', 'RENUSDT': '1', 'KSMUSDT': '0.1', 'NEARUSDT': '1', 'AAVEUSDT': '0.1', 'FILUSDT': '0.1', 'RSRUSDT': '1', 'LRCUSDT': '1', 'MATICUSDT': '1', 'OCEANUSDT': '1', 'CVCUSDT': '1', 'BELUSDT': '1', 'CTKUSDT': '1', 'AXSUSDT': '1', 'ALPHAUSDT': '1', 'ZENUSDT': '0.1', 'SKLUSDT': '1', 'GRTUSDT': '1', '1INCHUSDT': '1', 'AKROUSDT': '1', 'CHZUSDT': '1', 'SANDUSDT': '1', 'ANKRUSDT': '1', 'LUNAUSDT': '1', 'BTSUSDT': '1', 'LITUSDT': '0.1', 'UNFIUSDT': '0.1', 'DODOUSDT': '0.1', 'REEFUSDT': '1', 'RVNUSDT': '1', 'SFPUSDT': '1', 'XEMUSDT': '1', 'COTIUSDT': '1', 'CHRUSDT': '1', 'MANAUSDT': '1', 'ALICEUSDT': '0.1', 'HBARUSDT': '1', 'ONEUSDT': '1', 'LINAUSDT': '1', 'STMXUSDT': '1', 'DENTUSDT': '1', 'CELRUSDT': '1', 'HOTUSDT': '1', 'MTLUSDT': '1', 'OGNUSDT': '1', 'BTTUSDT': '1', 'NKNUSDT': '1', 'SCUSDT': '1', 'DGBUSDT': '1', '1000SHIBUSDT': '1', 'ICPUSDT': '0.01', 'BAKEUSDT': '1', 'GTCUSDT': '0.1'}

# Gets the maximum decimal places we can buy or sell the coin in terms of dollar
FUTURES_MAX_PRECISION_DICT    = {'BTCUSDT': '0.01', 'ETHUSDT': '0.01', 'BCHUSDT': '0.01', 'XRPUSDT': '0.0001', 'EOSUSDT': '0.001', 'LTCUSDT': '0.01', 'TRXUSDT': '0.00001', 'ETCUSDT': '0.001', 'LINKUSDT': '0.001', 'XLMUSDT': '0.00001', 'ADAUSDT': '0.00010', 'XMRUSDT': '0.01', 'DASHUSDT': '0.01', 'ZECUSDT': '0.01', 'XTZUSDT': '0.001', 'BNBUSDT': '0.010', 'ATOMUSDT': '0.001', 'ONTUSDT': '0.0001', 'IOTAUSDT': '0.0001', 'BATUSDT': '0.0001', 'VETUSDT': '0.000010', 'NEOUSDT': '0.001', 'QTUMUSDT': '0.001', 'IOSTUSDT': '0.000001', 'THETAUSDT': '0.0010', 'ALGOUSDT': '0.0001', 'ZILUSDT': '0.00001', 'KNCUSDT': '0.00100', 'ZRXUSDT': '0.0001', 'COMPUSDT': '0.01', 'OMGUSDT': '0.0001', 'DOGEUSDT': '0.000010', 'SXPUSDT': '0.0001', 'KAVAUSDT': '0.0001', 'BANDUSDT': '0.0001', 'RLCUSDT': '0.0001', 'WAVESUSDT': '0.0010', 'MKRUSDT': '0.10', 'SNXUSDT': '0.001', 'DOTUSDT': '0.001', 'DEFIUSDT': '0.1', 'YFIUSDT': '1', 'BALUSDT': '0.001', 'CRVUSDT': '0.001', 'TRBUSDT': '0.010', 'YFIIUSDT': '0.1', 'RUNEUSDT': '0.0010', 'SUSHIUSDT': '0.0010', 'SRMUSDT': '0.0010', 'BZRXUSDT': '0.0001', 'EGLDUSDT': '0.010', 'SOLUSDT': '0.0010', 'ICXUSDT': '0.0001', 'STORJUSDT': '0.0001', 'BLZUSDT': '0.00001', 'UNIUSDT': '0.0010', 'AVAXUSDT': '0.0010', 'FTMUSDT': '0.000010', 'HNTUSDT': '0.0010', 'ENJUSDT': '0.00010', 'FLMUSDT': '0.0001', 'TOMOUSDT': '0.0001', 'RENUSDT': '0.00001', 'KSMUSDT': '0.010', 'NEARUSDT': '0.0001', 'AAVEUSDT': '0.010', 'FILUSDT': '0.001', 'RSRUSDT': '0.000001', 'LRCUSDT': '0.00001', 'MATICUSDT': '0.00010', 'OCEANUSDT': '0.00001', 'CVCUSDT': '0.00001', 'BELUSDT': '0.00010', 'CTKUSDT': '0.00100', 'AXSUSDT': '0.00100', 'ALPHAUSDT': '0.00010', 'ZENUSDT': '0.001', 'SKLUSDT': '0.00001', 'GRTUSDT': '0.00001', '1INCHUSDT': '0.0001', 'AKROUSDT': '0.00001', 'CHZUSDT': '0.00001', 'SANDUSDT': '0.00001', 'ANKRUSDT': '0.000010', 'LUNAUSDT': '0.001', 'BTSUSDT': '0.00001', 'LITUSDT': '0.001', 'UNFIUSDT': '0.001', 'DODOUSDT': '0.001', 'REEFUSDT': '0.000001', 'RVNUSDT': '0.00001', 'SFPUSDT': '0.0001', 'XEMUSDT': '0.0001', 'COTIUSDT': '0.00001', 'CHRUSDT': '0.0001', 'MANAUSDT': '0.0001', 'ALICEUSDT': '0.001', 'HBARUSDT': '0.00001', 'ONEUSDT': '0.00001', 'LINAUSDT': '0.00001', 'STMXUSDT': '0.00001', 'DENTUSDT': '0.000001', 'CELRUSDT': '0.00001', 'HOTUSDT': '0.000001', 'MTLUSDT': '0.0001', 'OGNUSDT': '0.0001', 'BTTUSDT': '0.000001', 'NKNUSDT': '0.00001', 'SCUSDT': '0.000001', 'DGBUSDT': '0.00001', '1000SHIBUSDT': '0.000001', 'ICPUSDT': '0.01', 'BAKEUSDT': '0.0001', 'GTCUSDT': '0.001', 'ETHBUSD': '0.01', 'BTCUSDT0924': '0.1', 'ETHUSDT0924': '0.01', 'BTCDOMUSDT': '0.1', 'KEEPUSDT': '0.0001'}


# time for each thread to rake
SPOT_RAKE_TIME                = float(g_cfg_dict['spot_rake_time'])             * 60
CROSS_RAKE_TIME               = float(g_cfg_dict['margin_cross_rake_time'])     * 60
ISOLATED_RAKE_TIME            = float(g_cfg_dict['margin_isolated_rake_time'])  * 60 
FUTURES_ISOLATED_RAKE_TIME    = float(g_cfg_dict['futures_isolated_rake_time']) * 60

# rake percent for each thread
SPOT_RAKE_PERCENT             = float(g_cfg_dict['spot_rake_percent'])             / 100
MARGIN_CROSS_RAKE_PERCENT     = float(g_cfg_dict['margin_cross_rake_percent'])     / 100
MARGIN_ISOLATED_RAKE_PERCENT  = float(g_cfg_dict['margin_isolated_rake_percent'])  / 100
FUTURES_ISOLATED_RAKE_PERCENT = float(g_cfg_dict['futures_isolated_rake_percent']) / 100

# rake threshold
SPOT_RAKE_THRESHOLD_PERCENT              = float(g_cfg_dict['spot_rake_threshold_percent'])             / 100  # (We convert to decimal by dividing by 100)
MARGIN_CROSS_RAKE_THRESHOLD_PERCENT      = float(g_cfg_dict['margin_cross_rake_threshold_percent'])     / 100  # (We convert to decimal by dividing by 100) 
MARGIN_ISOLATED_RAKE_THRESHOLD_PERCENT   = float(g_cfg_dict['margin_isolated_rake_threshold_percent'])  / 100  # (We convert to decimal by dividing by 100)
FUTURES_ISOLATED_RAKE_THRESHOLD_PERCENT  = float(g_cfg_dict['futures_isolated_rake_threshold_percent']) / 100  # (We convert to decimal by dividing by 100)

FUTURES_ISOLATED_STOP_IN_PROFIT              = float(g_cfg_dict['futures_isolated_stop_in_profit_percent'])      / 100 #
FUTURES_ISOLATED_AUTO_DELEVERAGE_PERCENT     = float(g_cfg_dict['futures_isolated_auto_deleverage_percent'])     / 100 # used for calculating the deleverage threshold.
FUTURES_ISOLATED_DELEVERAGE_QUANTITY_PERCENT = float(g_cfg_dict['futures_isolated_deleverage_quantity_percent']) / 100 # amount to sell when deleveraging a position

# blacklist
SPOT_RAKE_BLACKLIST             = g_cfg_dict['spot_rake_blacklist'].split(",")
CROSS_RAKE_BLACKLIST            = g_cfg_dict['margin_cross_rake_blacklist'].split(",")
ISOLATED_RAKE_BLACKLIST         = g_cfg_dict['margin_isolated_rake_blacklist'].split(",")
FUTURES_ISOLATED_RAKE_BLACKLIST = g_cfg_dict['futures_isolated_rake_blacklist'].split(",")


# booleans
RAKE_SPOT                           = False
RAKE_MARGIN_CROSS                   = False
RAKE_MARGIN_ISOLATED                = False
RAKE_FUTURES_ISOLATED               = False
   
FUTURES_ISOLATED_STOP_IN_PROFIT     = False
FUTURES_ISOLATED_AUTO_DELEVERAGE    = False

MARGIN_ISOLATED_MOVE_ASSET_ON_REPAY = False
MARGIN_CROSS_MOVE_ASSET_ON_REPAY    = False



if g_cfg_dict['spot_rake'] == "True":
    RAKE_SPOT = True

if g_cfg_dict['margin_cross_rake'] == "True":
    RAKE_MARGIN_CROSS = True

if g_cfg_dict['margin_isolated_rake'] == "True":
    RAKE_MARGIN_ISOLATED = True

if g_cfg_dict['futures_isolated_rake'] == "True":
    RAKE_FUTURES_ISOLATED = True

if g_cfg_dict['futures_isolated_stop_in_profit'] == "True":
    FUTURES_ISOLATED_STOP_IN_PROFIT = True

if g_cfg_dict['futures_isolated_auto_deleverage'] == "True":
    FUTURES_ISOLATED_AUTO_DELEVERAGE = True

if g_cfg_dict['margin_isolated_move_asset_on_repay'] == "True":
    MARGIN_ISOLATED_MOVE_ASSET_ON_REPAY = True

if g_cfg_dict['margin_cross_move_asset_on_repay'] == "True":
    MARGIN_CROSS_MOVE_ASSET_ON_REPAY = True
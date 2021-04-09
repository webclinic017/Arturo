import os
import logging

ExceptionLog = os.getcwd()+"\\Exception.txt" 
tickerBasket = os.getcwd()+"\\TickerBasket.csv"
historyDataPath = os.getcwd()+"\HistoryData\\"
calculationDataPath = os.getcwd()+"\Data\\"
Report = os.getcwd()+"\Report\\"
ticker_collection = {}
ticker_id_collection = {}
DateTime_collection = {}
DateTime_collection_1min = {}
order_collections = {}
trade_qty = 100000
stochasticPeriod1=5
stochasticPeriod2=5
stochasticPeriod3=3
ema_LongPeriod=5
ema_ShortPeriod=3
selectedTimeFrame = ""
selectedTimeFrame_collection = {'1 min':60,'3 mins':180,'5 mins':300,'15 mins':900,'1 hour':3600}
TF = 0
slippage = 0
longExitStoch = 0
ShortExitStoch = 0
startTradeHr = None
startTradeMin = None
endTradeHr = None
endTradeMin = None
EODExitHr = None
EODExitMin = None
stochasticPeriod = stochasticPeriod1 + stochasticPeriod3
#objGeneric = Generic()
#objOrder = Orders()
BUY = "BUY"
SELL = "SELL"
OPEN = "OPEN"
segment = None
STK = "STK"
CASH = "CASH"
commPer = 0
ORDER_TYPE_MKT = "MKT"
ORDER_TYPE_LMT = "LMT"
ORDER_TYPE_STP = "STP"
ORDER_TYPE_TGT = "TGT"
ORDER_NAME_EntryOrder = "EntryOrder"
ORDER_NAME_StopLossOrder = "StopLossOrder"
ORDER_NAME_TargetOrder = "TargetOrder"
ORDER_STATUS_FILLED = "FILLED"
ORDER_STATUS_FILLED = "SUBMITTED"


historyDataEnd_Count = 0

ib_host = None
ib_port = None
IB_DateTime = None
OrderId = 0
# # logging
# logging.basicConfig(filename = "logs.txt",
#                     level = logging.DEBUG,
#                     format=format='%(levelname)s: %(asctime)s %(message)s',
#                     datefmt= '%m/%d/%Y %I:%M:%S')
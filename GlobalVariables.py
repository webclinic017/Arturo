import os
from Orders import Orders
from Generic import Generic
ExceptionLog = os.getcwd()+"\\Exception.txt" 
tickerBasket = os.getcwd()+"\TickerBasket.csv"
historyDataPath = os.getcwd()+"\HistoryData\\"
calculationDataPath = os.getcwd()+"\Data\\"
Report = os.getcwd()+"\Report\\"
ticker_collection = {}
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
objGeneric = Generic()
objOrder = Orders()
BUY = "BUY"
SELL = "SELL"
OPEN = "OPEN"
segment = None
STK = "STK"
CASH = "CASH"
commPer = 0

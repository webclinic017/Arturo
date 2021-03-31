import Log
import traceback
from Bar import Bar
class Ticker():
    def __init__(self,id):
       try:
            #Ticker basic detials
            self.tickerID = id
            self.symbol=None
            self.secType = None
            self.exchange = None
            self.currency = None
            self.expiry = None
            # as per req        
            self.qty=0 # global
            self.pip=0 # used aspip for currency and tickSize for stock
            self.spread=0
            self.target=0
            self.stopLoss =0
            # collection to store data
            self.ohlc = {}
            self.ohlc_1min = {}
            # used for indicators
            self.ema_Long = 0
            self.ema_Short = 0
            self.handyData_close = {}
            self.handyData_high = {}
            self.handyData_low = {}
            self.handyData_volume = {}
            #Orders
            self.orderId=0
            self.isExit = False
            self.weekDays = []
            self.startTradeHr = None
            self.startTradeMin = None
            self.endTradeHr = None
            self.endTradeMin = None
            self.EODExitHr = None
            self.EODExitMin = None
            self.isEMAExit = False
            self.isStochExit = False
            self.construct_ohlc = Bar()
            self.startConstruction = False
            # IB 
            self.ltp = 0
            self.objIBContract = None
       except Exception as ex:
           Log.WriteLog("__init__",traceback.format_exc())
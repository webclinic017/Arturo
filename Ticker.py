from Bars import Bars
class Ticker:
    def __init__(self,id):
        #Ticker basic detials
        self.tickerID = id
        self.symbol=""
        self.secType=""
        self.exchange=""
        self.currency=""
        self.expiry =""
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
        self.handy_close_longema = {}
        self.handy_close_shortema = {}
        # Indicators period and timeframe
        self.TF = 0
        self.stochasticPeriod1=5
        self.stochasticPeriod2=5
        self.stochasticPeriod3=3
        self.ema_LongPeriod=5
        self.ema_ShortPeriod=3
        self.longExitStoch = 0
        self.ShortExitStoch = 0
        self.stochasticPeriod = 0        
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
    
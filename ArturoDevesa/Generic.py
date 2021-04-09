import GlobalVariables
from Ticker import Ticker
import Log
import os
import csv
import traceback
from Bars import Bars
from datetime import datetime ,timedelta
class Generic:
    
    def loadData(self):
        try:
            for obj in GlobalVariables.ticker_collection.values():
                self.loadHistoryData(obj)
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"loadData")

    def loadHistoryData(self,objTicker):
        try:
            #timeFrame = ["1min",GlobalVariables.selectedTimeFrame]
            timeFrame = [GlobalVariables.selectedTimeFrame]
            for TF in timeFrame:
                filePath = os.getcwd()+"\\HistoryData\\"+objTicker.symbol+"_"+TF+".csv"
                flag = self.isFileExists(filePath)
                if(flag):
                    with open(filePath) as file:
                        reader = csv.DictReader(file)
                        prev_dt = None
                        for ohlc in reader:
                            objBar = Bars()
                            objBar.dt = ohlc["DateTime"]
                            objBar.dt =  (datetime.strptime(objBar.dt,'%m/%d/%Y %H:%M:%S %p'))
                            objBar.open_ = float(ohlc["Open"])
                            objBar.high = float(ohlc["High"])
                            objBar.low = float(ohlc["Low"])
                            objBar.close = float(ohlc["Close"])
                            objBar.volume = float(ohlc["Volume"])
                            if(not prev_dt == None):
                                objBar.prev_dt = prev_dt
                            prev_dt = objBar.dt
                            if(TF == GlobalVariables.selectedTimeFrame):
                                if(not objBar.dt in objTicker.ohlc):
                                    objTicker.ohlc[objBar.dt] = objBar
                                if(not objBar.dt in GlobalVariables.DateTime_collection):
                                    GlobalVariables.DateTime_collection[objBar.dt] = len(GlobalVariables.DateTime_collection)+1
                            elif(TF == "1min"):
                                if(not objBar.dt in objTicker.ohlc_1min):
                                    objTicker.ohlc_1min[objBar.dt] = objBar
                                if(not objBar.dt in GlobalVariables.DateTime_collection_1min):
                                    GlobalVariables.DateTime_collection_1min[objBar.dt] = len(GlobalVariables.DateTime_collection_1min)+1

        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"loadHistoryData")

    def isFileExists(self,fileName):
        try:
            if(os.path.exists(fileName)):
                return True
            return False 
        except Exception as identifier:
            Log.WriteLog(traceback.format_exc(),"isFileExists")

    def  loadTickerCollection(self,fileName):
        try:
            flag = self.isFileExists(fileName)
            if(flag == False):
                print(fileName+"  Not Found")      
            with open(fileName) as file:
                reader = csv.DictReader(file)
                for ticker in reader:
                    if(not ticker["Status"] == "A"):
                        continue
                    objTicker = Ticker(len(GlobalVariables.ticker_collection)+1)
                    objTicker.symbol = ticker['Symbol']
                    objTicker.secType = ticker['SecType']
                    objTicker.exchange = ticker['Exchange']
                    objTicker.currency = ticker['Currency']
                    #objTicker.expiry = ticker['Expiry']
                    #objTicker.expiry = GlobalVariables.trade_qty
                    objTicker.qty = int(ticker['Quantity'])
                    objTicker.spread = float(ticker['Spread'])
                    objTicker.pip = float(ticker['TickSize'])
                    #objTicker.target = float(ticker['Target'])
                    objTicker.stopLoss = float(ticker['StopLoss'])#007
                    objTicker.target = float(ticker['Target'])
                    objTicker.isEMAExit = ticker['isEmaExit'].upper()
                    objTicker.isStochExit = ticker['isStochExit'].upper()
                    objTicker.weekDays = [x.upper() for x in ticker['weekDays'].split(",")]
                    objTicker.startTradeHr = int(ticker['Start_Time_Hr'])
                    objTicker.startTradeMin = int(ticker['Start_Time_Min'])
                    objTicker.endTradeHr = int(ticker['Stop_Time_Hr'])
                    objTicker.endTradeMin = int(ticker['Stop_Time_Min'])
                    objTicker.EODExitHr = int(ticker['EOD_Hr'])
                    objTicker.EODExitMin = int(ticker['EOD_Min'])
                    if(GlobalVariables.segment == None and objTicker.secType == GlobalVariables.STK):
                         GlobalVariables.segment = GlobalVariables.STK
                    elif(GlobalVariables.segment == None and objTicker.secType == GlobalVariables.CASH):
                        GlobalVariables.segment = GlobalVariables.CASH
                    if(not objTicker.tickerID in GlobalVariables.ticker_collection):
                        GlobalVariables.ticker_collection[objTicker.tickerID] = objTicker
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"loadTickerCollection")

    def roundToTickSize(self,price,tickSize):

        div = 0
        try:
            div = int(round(1/tickSize))
            return round(price * div)/div
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"roundToTickSize")

    def createNewBar(self,TF,objTicker,dt,open_ ,high,low,close,volume):
            bars = None
            try:
                objTicker.construct_ohlc.count +=1
                if(objTicker.construct_ohlc .count == 1):
                    #print(hex(id(objTicker.construct_ohlc.count)),objTicker.construct_ohlc.count,objTicker.symbol)
                    objTicker.construct_ohlc.open_ = open_
                    objTicker.construct_ohlc.high = high
                    objTicker.construct_ohlc.low =  low
                    objTicker.construct_ohlc.close = close
                    objTicker.construct_ohlc.volume = volume
                    objTicker.construct_ohlc.dt = dt
                    if(len(objTicker.ohlc) > 0):
                        objTicker.construct_ohlc.dt_prev = sorted(objTicker.ohlc.keys())[-1]# get last value from dictionary
                else:
                    #print(hex(id(objTicker.construct_ohlc.count)),objTicker.construct_ohlc.count,objTicker.symbol)
                    if(high > objTicker.construct_ohlc.high):
                        objTicker.construct_ohlc.high = high
                    if(low < objTicker.construct_ohlc.low):
                        objTicker.construct_ohlc.low = low
                    objTicker.construct_ohlc.close = close
                    objTicker.construct_ohlc.volume += volume
                if(objTicker.construct_ohlc.count == TF):
                    #print(objTicker.construct_ohlc.count,TF,objTicker.symbol)
                    objTicker.construct_ohlc.close = close
                    objTicker.construct_ohlc.count = 0

                    bars = Bars()
                    bars.dt = objTicker.construct_ohlc.dt
                    bars.open_ = self.roundToTickSize(objTicker.construct_ohlc.open_,GlobalVariables.tickSize)
                    bars.high = self.roundToTickSize(objTicker.construct_ohlc.high,GlobalVariables.tickSize)
                    bars.low = self.roundToTickSize(objTicker.construct_ohlc.low,GlobalVariables.tickSize)
                    bars.close = self.roundToTickSize(objTicker.construct_ohlc.close,GlobalVariables.tickSize)
                    bars.volume = objTicker.construct_ohlc.volume
                    if(len(objTicker.ohlc) > 0):
                        bars.prev_dt = sorted(objTicker.ohlc.keys())[-1]# get last vlaue from dictionary 
                    
                    if(bars.prev_dt == None):# if prev_dt equals to None
                        bars.prev_dt  = bars.dt + timedelta(seconds=-GlobalVariables.TF.get(int(objTicker.timeFrame))) # subtract seconds
                    if(not bars.prev_dt in objTicker.ohlc):
                        objTicker.ohlc[bars.dt] = bars # add new value to ditionary 
                    objTicker.construct_ohlc.open_ = objTicker.construct_ohlc.high = objTicker.construct_ohlc.low = objTicker.construct_ohlc.close = objTicker.construct_ohlc.volume = 0
                return bars
            except Exception as ex:
                Log.WriteLog(traceback.format_exc(),"createNewBar")
                
    def calculateRsi(self,closeprice , close , prevClose , prevAvgGain , prevAvgLoss , prevRsi , period):
        try:
            closeprice = closeprice[len(closeprice)-period-1:len(closeprice)]
            avg_gain = 0
            avg_loss = 0
            rsi = 0
            i = -1
            gain = [0]
            loss = [0]
            change = 0
            if(len(closeprice) >= period+1 and prevRsi == 0):
                prev_price = 0
                for items in closeprice:
                    i = i + 1
                    if(prev_price == 0):
                        prev_price = items
                    else:
                        change = items - prev_price
                        prev_price = items
                        if(change >= 0):
                            gain.insert(i,change)
                            avg_gain = avg_gain + change
                        else:
                            change = change * -1
                            loss.insert(i,change)
                            avg_loss = avg_loss + change
                avg_gain = (avg_gain / period)
                avg_loss = (avg_loss / period)
            elif(prevRsi != 0):
                change = close - prevClose
                if(change > 0):
                    gain.insert(0,change)
                elif(change < 0):
                    change = (change * -1)
                    loss.insert(0,change)
                avg_gain = ((prevAvgGain * (period - 1)) + gain[0]) / period
                avg_loss = ((prevAvgLoss * (period - 1)) + loss[0]) / period
            if(avg_loss == 0):
                rsi = 100
            else:
                RS = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + RS))
            return round(rsi,2) , round(avg_gain,2) , round(avg_loss,2)
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"calculatRsi()")
    
    def caculateMfi(self,High,Low,Close,Volume,period):
        try:
            High = High[len(High)-period-1:len(High)]
            Low = Low[len(Low)-period-1:len(Low)]
            Close = Close[len(Close)-period-1:len(Close)]
            Volume = Volume[len(Volume)-period-1:len(Volume)]

            pos_MF = []
            neg_MF = []
            if(len(High) >= period+1):
                prev_TypicalPrice = 0
                for i in range(len(High)):
                    typicalPrice = self.get_TypicalPrice(High[i],Low[i],Close[i])
                    RMF = self.get_rawMoneyFlow(typicalPrice,Volume[i])
                    if(prev_TypicalPrice > 0 ):
                        if(typicalPrice > prev_TypicalPrice):
                            pos_MF.append(RMF)
                        else:
                            neg_MF.append(RMF)
                    prev_TypicalPrice = typicalPrice
                mfi =  round(sum(pos_MF)/sum(neg_MF),2)
                mfi = 100-(100/(1+mfi))
                return round(mfi,2)           
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"calculateMfi")

    def get_TypicalPrice(self,high,low,close_):
        try:
            value = (high+low+close_)/3
            return value
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"calculateTypicalPrice")

    def get_rawMoneyFlow(self,typicalPrice , volume):
        try:
            return typicalPrice * volume
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"get_rawMoneyFlow")

    def calculate_Stochastic(self , high  , low , close,tickSize, stochasticPeriod1,stochasticPeriod2,stochasticPeriod3):
        try:
            Kfast = []
            KPercentage = []
            stochastic = []
            signal = []
            startIndex = 0
            a= []
            b = []
            p= 0 
            q= 0
            endIndex = stochasticPeriod1
            for i in range(stochasticPeriod3+1):
                HighestHigh = max(high[startIndex:endIndex])
                lowestLow = min(low[startIndex:endIndex])
                p = close[endIndex-1] - lowestLow
                q = HighestHigh - lowestLow
                if(q == 0):
                    q = 1
                stochastic.append(round(p/q*100,2))
                endIndex+=1
                startIndex +=1
                if(len(stochastic) == stochasticPeriod3):
                    signal.append(round(sum(stochastic)/len(stochastic),2))
            return stochastic[-1],signal[-1]
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"calculate_Stochastic()")

    def ema(self,price,prev_ema,period ,tickSize):
        try:
            value = 0
            value = (2.0 / (period + 1)) * (price - prev_ema) + prev_ema
            return self.roundToTickSize(value,tickSize)
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"EMA")

    def sma(self,price,period , tickSize):
        try:
            values = []
            cal_sma = 0
            for i in price:
                values.append(i)
                if(len(values) == period):
                    cal_sma = self.roundToTickSize(sum(values)/len(values),tickSize)
                    values.pop(0)
            return cal_sma
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"SMA")


    def crossOver(self,prev_emaLong,prev_emashort,emaLong,emaShort):
        try:
            if(prev_emashort >= prev_emaLong and emaLong > emaShort):
                return GlobalVariables.SELL
            elif(prev_emaLong >= prev_emashort and emaShort > emaLong):
                return GlobalVariables.BUY
            return ""
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"crossOver()")

    def checkForExit(self,flag,stochastic,value):
        try:
            if(flag > 0):
                if(stochastic > value):
                    return True
            else:
                if(stochastic < value):
                    return True
            return False
        except Exception as ex:
            Log.WriteLog(ex,"checkForExit")

    def calculate_SL(self,action,price,per,tickSize):

        try:
            temp = 0
            if(action == GlobalVariables.BUY):
                temp = price -  (price * per / 100)
            else:
                temp = price +  (price * per / 100)
            return self.roundToTickSize(temp,tickSize)
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"calculate_SL")

    def calculate_tgt(self,action,price,per,tickSize):

        try:
            temp = 0
            if(action == GlobalVariables.BUY):
                temp = price +  (price * per / 100)
            else:
                temp = price -  (price * per / 100)
            return self.roundToTickSize(temp,tickSize)
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"calculate_tgt")            

    def checkfor_sl_exit(self,action,objBar , sl_price):
        try:
            if(action == GlobalVariables.BUY):
                if(objBar.low < sl_price):
                    return True
            else:
                if(objBar.high > sl_price):
                    return True
            return False
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"checkfor_sl_exit")

    def checkfor_tgt_exit(self,action,objBar , tgt_price):
        try:
            if(action == GlobalVariables.BUY):
                if(objBar.high >= tgt_price):
                    return True
            else:
                if(objBar.low <= tgt_price):
                    return True
            return False
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"checkfor_tgt_exit")            

    def calculate_sl_pip(self,action ,price,sl_pip,tickSize,):
        try:
            temp = 0
            if(action == GlobalVariables.BUY):
                temp = price - (sl_pip * tickSize)
            else:
                temp = price + (sl_pip * tickSize)
            return self.roundToTickSize(temp,tickSize)
        except Exception as ex:
            Log.WriteLog(ex,"checkfor_sl_exit_pip")

    def calculate_tgt_pip(self,action ,price,tgt_pip,tickSize,):
        try:
            temp = 0
            if(action == GlobalVariables.BUY):
                temp = price + (tgt_pip * tickSize)
            else:
                temp = price - (tgt_pip * tickSize)
            return self.roundToTickSize(temp,tickSize)
        except Exception as ex:
            Log.WriteLog(ex,"checkfor_sl_exit_pip")            

    def calculate_comm(self,value,per):
        return round(value * per / 100,2)
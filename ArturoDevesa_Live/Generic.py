import Log
import traceback
import GlobalVariables
from Ticker import Ticker
import csv
import os
import json
from ibapi.contract import Contract
from Bar import Bar
from datetime import datetime , timedelta

def load_config():
    try:
        f = open('config.json')
        data = json.load(f)
        GlobalVariables.ib_host = data["ib_host"]
        GlobalVariables.ib_port = int(data["ib_port"])
    except Exception as ex:
        Log.WriteLog("load_config",traceback.format_exc())

def isFileExists(fileName):
    try:
        if(os.path.exists(fileName)):
            return True
        return False 
    except Exception as identifier:
        Log.WriteLog(traceback.format_exc(),"isFileExists")

def loadTickerBasket(fileName):
    
    try:
        flag = isFileExists(fileName)
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
                objTicker.qty = int(ticker['Quantity'])
                #objTicker.expiry = ticker['Expiry']
                #objTicker.expiry = GlobalVariables.trade_qty
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
                # if(GlobalVariables.segment == None and objTicker.secType == GlobalVariables.STK):
                #     GlobalVariables.segment = GlobalVariables.STK
                # elif(GlobalVariables.segment == None and objTicker.secType == GlobalVariables.CASH):
                #     GlobalVariables.segment = GlobalVariables.CASH
                objTicker.objIBContract = Contract()
                objTicker.objIBContract.symbol = objTicker.symbol
                objTicker.objIBContract.secType = objTicker.secType 
                objTicker.objIBContract.exchange = objTicker.exchange
                objTicker.objIBContract.currency = objTicker.currency                
                if(not objTicker.tickerID in GlobalVariables.ticker_collection):
                    GlobalVariables.ticker_collection[objTicker.tickerID] = objTicker
                    GlobalVariables.ticker_id_collection[objTicker.symbol] = objTicker.tickerID
    except Exception as ex:
        Log.WriteLog("loadTickerBasket",traceback.format_exc())        

def calculate_Stochastic(high  , low , close,tickSize, stochasticPeriod1,stochasticPeriod2,stochasticPeriod3):
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
 
def createNewBar(TF,objTicker,dt,open_ ,high,low,close,volume,tickSize):
    bars = None
    try:
        objTicker.construct_ohlc.count +=1
        #print(TF,objTicker.construct_ohlc.count)
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
            bars = Bar()
            bars.dt = objTicker.construct_ohlc.dt
            bars.open_ = roundToTickSize(objTicker.construct_ohlc.open_,tickSize)
            bars.high = roundToTickSize(objTicker.construct_ohlc.high,tickSize)
            bars.low = roundToTickSize(objTicker.construct_ohlc.low,tickSize)
            bars.close = roundToTickSize(objTicker.construct_ohlc.close,tickSize)
            bars.volume = objTicker.construct_ohlc.volume
            if(len(objTicker.ohlc) > 0):
                bars.dt_prev = sorted(objTicker.ohlc.keys())[-1]# get last vlaue from dictionary 
        
            if(bars.dt_prev == None):# if prev_dt equals to None
                bars.dt_prev  = bars.dt + timedelta(seconds=-GlobalVariables.TF.get(int(objTicker.timeFrame))) # subtract seconds
            if(not bars.dt_prev in objTicker.ohlc):
                objTicker.ohlc[bars.dt] = bars # add new value to ditionary 
            objTicker.construct_ohlc.open_ = objTicker.construct_ohlc.high = objTicker.construct_ohlc.low = objTicker.construct_ohlc.close = objTicker.construct_ohlc.volume = 0
        return bars
    except Exception as ex:
        Log.WriteLog(traceback.format_exc(),"createNewBar")

def sma(price,period , tickSize):
    try:
        values = []
        cal_sma = 0
        for i in price:
            values.append(i)
            if(len(values) == period):
                cal_sma = roundToTickSize(sum(values)/len(values),tickSize)
                values.pop(0)
        return cal_sma
    except Exception as ex:
        Log.WriteLog(traceback.format_exc(),"SMA")

def ema(price,prev_ema,period ,tickSize):
    try:
        value = 0
        value = (2.0 / (period + 1)) * (price - prev_ema) + prev_ema
        return roundToTickSize(value,tickSize)
    except Exception as ex:
        Log.WriteLog(traceback.format_exc(),"EMA")

def roundToTickSize(price,tickSize):
    div = 0
    try:
        div = int(round(1/tickSize))
        return round(price * div)/div
    except Exception as ex:
        Log.WriteLog(traceback.format_exc(),"roundToTickSize")

def crossOver(prev_emaLong,prev_emashort,emaLong,emaShort):
    try:
        if(True or prev_emashort >= prev_emaLong and emaLong > emaShort):
            return GlobalVariables.SELL
        elif(prev_emaLong >= prev_emashort and emaShort > emaLong):
            return GlobalVariables.BUY
        return ""
    except Exception as ex:
        Log.WriteLog(traceback.format_exc(),"crossOver()")

def checkForExit(flag,stochastic,value):
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

def calculate_sl_pip(action ,price,sl_pip,tickSize,):
    try:
        temp = 0
        if(action == GlobalVariables.BUY):
            temp = price - (sl_pip * tickSize)
        else:
            temp = price + (sl_pip * tickSize)
        return roundToTickSize(temp,tickSize)
    except Exception as ex:
        Log.WriteLog(ex,"checkfor_sl_exit_pip")

def calculate_tgt_pip(action ,price,tgt_pip,tickSize,):
    try:
        temp = 0
        if(action == GlobalVariables.BUY):
            temp = price + (tgt_pip * tickSize)
        else:
            temp = price - (tgt_pip * tickSize)
        return roundToTickSize(temp,tickSize)
    except Exception as ex:
        Log.WriteLog(ex,"checkfor_sl_exit_pip")

def calculate_SL(action,price,per,tickSize):

    try:
        temp = 0
        if(action == GlobalVariables.BUY):
            temp = price -  (price * per / 100)
        else:
            temp = price +  (price * per / 100)
        return roundToTickSize(temp,tickSize)
    except Exception as ex:
        Log.WriteLog(traceback.format_exc(),"calculate_SL")

def calculate_tgt(action,price,per,tickSize):

    try:
        temp = 0
        if(action == GlobalVariables.BUY):
            temp = price +  (price * per / 100)
        else:
            temp = price -  (price * per / 100)
        return roundToTickSize(temp,tickSize)
    except Exception as ex:
        Log.WriteLog(traceback.format_exc(),"calculate_tgt")
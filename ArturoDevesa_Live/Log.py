# -*- coding: utf-8 -*-
"""
@author: smit
"""
from os import path
import GlobalVariables
from datetime import datetime 
def WriteLog(method,error):
    try:
        print("Exception logged ")
        if(path.exists(GlobalVariables.ExceptionLog) == False):      
            file = open(GlobalVariables.ExceptionLog,"w+")
            file.write("Date : "+str(datetime.now())+"\n")
            file.write("Method : "+method +"\n")
            file.write("Errror : "+str(error) +"\n")
            file.write("-------------------------------------------------------------------------\n")      
            file.close()
        if(path.exists(GlobalVariables.ExceptionLog) == True):
            file = open(GlobalVariables.ExceptionLog,"a+")
            file.write("Date : "+str(datetime.now())+"\n")
            file.write("Method : "+method +"\n")
            file.write("Errror : "+str(error) +"\n")
            file.write("-------------------------------------------------------------------------\n")      
            file.close()
    except Exception as ex:
        print("Error Log.patternLog : ",ex)
    # def createNewBar(self,objTicker,dt,open_ ,high,low,close,volume):
    #         bars = None
    #         TF = GlobalVariables.TF.get(int(objTicker.timeFrame)) / 5
    #         try:
    #             objTicker.construct_ohlc.count +=1
    #             if(objTicker.construct_ohlc .count == 1):
    #                 #print(hex(id(objTicker.construct_ohlc.count)),objTicker.construct_ohlc.count,objTicker.symbol)
    #                 objTicker.construct_ohlc.open_ = open_
    #                 objTicker.construct_ohlc.high = high
    #                 objTicker.construct_ohlc.low =  low
    #                 objTicker.construct_ohlc.close = close
    #                 objTicker.construct_ohlc.volume = volume
    #                 objTicker.construct_ohlc.dt = dt
    #                 if(len(objTicker.ohlc) > 0):
    #                     objTicker.construct_ohlc.dt_prev = sorted(objTicker.ohlc.keys())[-1]# get last value from dictionary
    #             else:
    #                 #print(hex(id(objTicker.construct_ohlc.count)),objTicker.construct_ohlc.count,objTicker.symbol)
    #                 if(high > objTicker.construct_ohlc.high):
    #                     objTicker.construct_ohlc.high = high
    #                 if(low < objTicker.construct_ohlc.low):
    #                     objTicker.construct_ohlc.low = low
    #                 objTicker.construct_ohlc.close = close
    #                 objTicker.construct_ohlc.volume = objTicker.construct_ohlc.volume + volume
    #             if(objTicker.construct_ohlc.count == TF):
    #                 #print(objTicker.construct_ohlc.count,TF,objTicker.symbol)
    #                 objTicker.construct_ohlc.close = close
    #                 objTicker.construct_ohlc.count = 0

    #                 bars = Bars()
    #                 bars.dt = objTicker.construct_ohlc.dt
    #                 bars.open_ = self.roundToTickSize(objTicker.construct_ohlc.open_,GlobalVariables.tickSize)
    #                 bars.high = self.roundToTickSize(objTicker.construct_ohlc.high,GlobalVariables.tickSize)
    #                 bars.low = self.roundToTickSize(objTicker.construct_ohlc.low,GlobalVariables.tickSize)
    #                 bars.close = self.roundToTickSize(objTicker.construct_ohlc.close,GlobalVariables.tickSize)
    #                 if(len(objTicker.ohlc) > 0):
    #                     bars.prev_dt = sorted(objTicker.ohlc.keys())[-1]# get last vlaue from dictionary 
                    
    #                 if(bars.prev_dt == None):# if prev_dt equals to None
    #                     bars.prev_dt  = bars.dt + timedelta(seconds=-GlobalVariables.TF.get(int(objTicker.timeFrame))) # subtract seconds
    #                 if(not bars.prev_dt in objTicker.ohlc):
    #                     objTicker.ohlc[bars.dt] = bars # add new value to ditionary 
    #                 objTicker.construct_ohlc.open_ = objTicker.construct_ohlc.high = objTicker.construct_ohlc.low = objTicker.construct_ohlc.close = objTicker.construct_ohlc.volume = 0
    #             return bars
    #         except Exception as ex:
    #             Logs.WriteLog("createNewBar",traceback.format_exc())        
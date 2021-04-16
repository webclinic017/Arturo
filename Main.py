from GUI import GUI
import Log
import traceback
import tkinter as Tkinter
from tkinter import *
from Ticker import Ticker
import os
import csv
from datetime import datetime
import calendar
import Generic
import Orders
import GlobalVariables
class Main(GUI):
    
    def __init__(self):
        try:
            self.load_requirements()
            super().__init__(1000,1600)
            self.mainForm.mainloop()
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"Main.__init__()")

    def btn_start_clickEvent(self):
        try:
            self.setParam()
            GlobalVariables.objGeneric.loadData()
            self.Init_calculation()
        except Exception as ex:
            print(traceback.format_exc(),"btn_start_clickEvent")

    def load_requirements(self):
        try:
            GlobalVariables.objGeneric.loadTickerCollection(GlobalVariables.tickerBasket)
            #self.messageToGUI("Load_requirements Done!")
        except Exception as ex:
            Log.WriteLog(ex,"load_requirements")

    def Simulate(self):
        try:
            for dt in GlobalVariables.DateTime_collection.keys():
                print(dt)
                for objTicker in GlobalVariables.ticker_collection.values():
                    weekDay_name = (calendar.day_name[dt.weekday()][:3]).upper()
                    if(not weekDay_name in  objTicker.weekDays):
                        continue
                    self.set_trading_param(objTicker)
                    if(dt in objTicker.ohlc):
                        objBar = objTicker.ohlc[dt]
                        if(objBar.stochastic == 0):
                            continue
                        if(objBar.prev_dt in objTicker.ohlc):
                            objBarPrev = objTicker.ohlc[objBar.prev_dt]
                            if(objTicker.orderId == 0 and objBar.dt >= datetime(objBar.dt.year,objBar.dt.month,objBar.dt.day,GlobalVariables.startTradeHr,GlobalVariables.startTradeMin,0)
                            and objBar.dt < datetime(objBar.dt.year,objBar.dt.month,objBar.dt.day,GlobalVariables.endTradeHr,GlobalVariables.endTradeMin,0) ):
                                
                                action = GlobalVariables.objGeneric.crossOver(objBarPrev.ema_Long,objBarPrev.ema_Short,objBar.ema_Long,objBar.ema_Short)
                                if(len(action) > 0):
                                    GlobalVariables.objOrder.createEntryOrder(objTicker,objBar,action)
                            elif(objTicker.orderId > 0):
                                objEntryOrder = GlobalVariables.order_collections[objTicker.orderId]
                                action = GlobalVariables.objGeneric.crossOver(objBarPrev.ema_Long,objBarPrev.ema_Short,objBar.ema_Long,objBar.ema_Short)
                                
                                if(GlobalVariables.objGeneric.checkfor_sl_exit(objEntryOrder.action,objBar,objEntryOrder.sl)):
                                    GlobalVariables.objOrder.createExitOrder(objBar,objTicker,objEntryOrder,"SL")
                                    continue

                                if(GlobalVariables.objGeneric.checkfor_tgt_exit(objEntryOrder.action,objBar,objEntryOrder.target)):
                                    GlobalVariables.objOrder.createExitOrder(objBar,objTicker,objEntryOrder,"TGT")
                                    continue

                                if(objTicker.isEMAExit == "TRUE" and objEntryOrder.action == GlobalVariables.BUY and action == GlobalVariables.SELL):
                                    GlobalVariables.objOrder.createExitOrder(objBar,objTicker,objEntryOrder,"EMA_EXIT")
                                elif(objTicker.isEMAExit == "TRUE" and objEntryOrder.action == GlobalVariables.SELL and action == GlobalVariables.BUY):
                                    GlobalVariables.objOrder.createExitOrder(objBar,objTicker,objEntryOrder,"EMA_EXIT")

                                    
                                if(objTicker.isStochExit == "TRUE" and objEntryOrder.action == GlobalVariables.BUY):
                                    if(objTicker.isExit == False):
                                        objTicker.isExit =  GlobalVariables.objGeneric.checkForExit(1,objBar.stochastic,GlobalVariables.longExitStoch)
                                    else:
                                        p =  GlobalVariables.objGeneric.checkForExit(-1,objBar.stochastic,GlobalVariables.longExitStoch)
                                        if(p == True):
                                            GlobalVariables.objOrder.createExitOrder(objBar,objTicker,objEntryOrder,"STOCH_EXIT")
                                elif(objEntryOrder.action == GlobalVariables.SELL):
                                    if(objTicker.isExit == False):
                                        objTicker.isExit =  GlobalVariables.objGeneric.checkForExit(-1,objBar.stochastic,GlobalVariables.ShortExitStoch)
                                    else:
                                        p =  GlobalVariables.objGeneric.checkForExit(1,objBar.stochastic,GlobalVariables.ShortExitStoch)
                                        if(p == True):
                                            GlobalVariables.objOrder.createExitOrder(objBar,objTicker,objEntryOrder,"STOCH_EXIT")
                            elif(objBar.dt > datetime(objBar.dt.year,objBar.dt.month,objBar.dt.day,GlobalVariables.EODExitHr,GlobalVariables.EODExitMin,0)):
                                for ticker in GlobalVariables.ticker_collection.values():
                                    if(ticker.orderId > 0):
                                        objEntryOrder = GlobalVariables.order_collections[ticker.orderId]
                                        GlobalVariables.objOrder.createExitOrder(objBar,objTicker,objEntryOrder,"EOD")
            self.LogOrder()
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"Main.Simulate")

    def Init_calculation(self):
        try:
            for dt in GlobalVariables.DateTime_collection.keys():
                for objTicker in GlobalVariables.ticker_collection.values():
                    if(dt in objTicker.ohlc):
                        objBar = objTicker.ohlc[dt]
                        objTicker.handyData_close.update({objBar.dt : objBar.close})
                        objTicker.handyData_high.update({objBar.dt : objBar.high})
                        objTicker.handyData_low.update({objBar.dt : objBar.low})
                        if(len(objTicker.handyData_close) >= GlobalVariables.stochasticPeriod):
                            objBar.stochastic , objBar.stochastic_signal =  GlobalVariables.objGeneric.calculate_Stochastic([x for x in objTicker.handyData_high.values()],[x for x in objTicker.handyData_low.values()],[x for x in objTicker.handyData_close.values()],objTicker.pip,GlobalVariables.stochasticPeriod1,GlobalVariables.stochasticPeriod2,GlobalVariables.stochasticPeriod3) 
                            for key in sorted(objTicker.handyData_close.keys()):
                                objTicker.handyData_close.pop(key)
                                objTicker.handyData_high.pop(key)
                                objTicker.handyData_low.pop(key)
                                #print(key)
                                break
                        if(len(objTicker.handyData_close) >= GlobalVariables.ema_LongPeriod):
                            if(objBar.prev_dt in objTicker.ohlc):
                                objBarPrev = objTicker.ohlc[objBar.prev_dt]
                                if(objBarPrev.ema_Long == 0):
                                    objBar.ema_Long = GlobalVariables.objGeneric.sma([x for x in objTicker.handyData_close.values()],GlobalVariables.ema_LongPeriod,objTicker.pip)
                                else:
                                    objBar.ema_Long = GlobalVariables.objGeneric.ema(objBar.close,objBarPrev.ema_Long,GlobalVariables.ema_LongPeriod,objTicker.pip)
                        if(len(objTicker.handyData_close) >= GlobalVariables.ema_ShortPeriod):
                            if(objBar.prev_dt in objTicker.ohlc):
                                objBarPrev = objTicker.ohlc[objBar.prev_dt]
                                if(objBarPrev.ema_Short == 0):
                                    objBar.ema_Short = GlobalVariables.objGeneric.sma([x for x in objTicker.handyData_close.values()],GlobalVariables.ema_ShortPeriod,objTicker.pip)
                                else:
                                    objBar.ema_Short = GlobalVariables.objGeneric.ema(objBar.close,objBarPrev.ema_Short,GlobalVariables.ema_ShortPeriod,objTicker.pip)
            self.messageToGUI("Init_Calculation Done !")
            self.dataToCSV()
            self.Simulate()
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"Init_calculation")

    def dataToCSV(self):
        try:
            List_file = os.listdir(GlobalVariables.calculationDataPath)
            if(len(List_file) > 0):
                i = [os.remove(GlobalVariables.calculationDataPath + x) for x in List_file]
            data = []
            for objTicker in GlobalVariables.ticker_collection.values():
                for obj in objTicker.ohlc.values():
                    data.append([obj.dt,obj.open_,obj.high,obj.low,obj.close,obj.ema_Long,obj.ema_Short,obj.stochastic,obj.stochastic_signal])
                file = open(GlobalVariables.calculationDataPath+objTicker.symbol+".csv",'a', newline ='') 
                header = ["DateTime","Open","High","Low","Close","EMA_Period_"+str(GlobalVariables.ema_LongPeriod),"EMA_Period_"+str(GlobalVariables.ema_ShortPeriod),"Stochastic","Stochastic_Signal"]
                with file:
                    write = csv.writer(file)
                    write.writerow(header)
                    write.writerows(data)
                    data.clear()
            self.messageToGUI("DataToCSV Done !")               
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"dataToCSV")

    def messageToGUI(self,message):
        try:
            self.txtBox_message.insert(END,"\n ->"+message)
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"messageToGUI()")

    def LogOrder(self):
        try:
            List_file = os.listdir(GlobalVariables.Report)
            if(len(List_file) > 0):
                i = [os.remove(GlobalVariables.Report + x) for x in List_file]
            data = []
            for obj in GlobalVariables.order_collections.values():
                if(GlobalVariables.segment == GlobalVariables.CASH):
                    data.append([obj.orderId,obj.parentOrderId,obj.symbol,obj.action,(calendar.day_name[obj.p_dt.weekday()])[:3],obj.p_dt,obj.p_price,obj.p_qty,obj.totalPip,obj.NET,obj.comm,obj.status,obj.sl,obj.target])
                else:
                    data.append([obj.orderId,obj.parentOrderId,obj.symbol,obj.action,(calendar.day_name[obj.p_dt.weekday()])[:3],obj.p_dt,obj.p_price,obj.p_qty,obj.Points,obj.NET,obj.comm,obj.status,obj.sl,obj.target])
            file = open(GlobalVariables.Report+"Trades.csv",'a', newline ='')
            header = ["OrderID","Parent_OrderID","Symbol","Action","WeekDay","p_dt","p_price","p_qty","Pip/Points","NET","Comm","Status","StopLoss","Target"]
            with file:
                write = csv.writer(file)
                write.writerow(header)
                write.writerows(data)
                data.clear()
            self.messageToGUI("TradesToCSV Done !")
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"LogOrder()")

    def setParam(self):
        try:
            GlobalVariables.ema_LongPeriod  = int(self.txtBox_emaPeriodLong_text.get())
            GlobalVariables.ema_ShortPeriod  = int(self.txtBox_emaPeriodShort_text.get())
            GlobalVariables.stochasticPeriod1  = int(self.txtBox_stochasticPeriod1_text.get())
            GlobalVariables.stochasticPeriod2  = int(self.txtBox_stochasticPeriod2_text.get())
            GlobalVariables.stochasticPeriod3  = int(self.txtBox_stochasticPeriod3_text.get())
            GlobalVariables.stochasticPeriod = GlobalVariables.stochasticPeriod1 + GlobalVariables.stochasticPeriod3
            GlobalVariables.selectedTimeFrame =  self.selectedEntryTF.get()
            GlobalVariables.commPer = float(self.txtBox_slippage_text.get()) # name is slippage but used for comm
            GlobalVariables.trade_qty = int(self.txtBox_tradeQty_text.get())
            GlobalVariables.longExitStoch = int(self.txtBox_longExitstoch_text.get())
            GlobalVariables.ShortExitStoch = int(self.txtBox_shortExitstoch_text.get())
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"setParam()")

    def set_trading_param(self,objTicker):
        try:
            GlobalVariables.startTradeHr = objTicker.startTradeHr
            GlobalVariables.startTradeMin = objTicker.startTradeMin
            GlobalVariables.endTradeHr = objTicker.endTradeHr
            GlobalVariables.endTradeMin = objTicker.endTradeMin
            GlobalVariables.EODExitHr = objTicker.EODExitHr
            GlobalVariables.EODExitMin = objTicker.EODExitMin
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"")

main = Main()

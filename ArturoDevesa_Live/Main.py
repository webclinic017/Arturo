from GUI import GUI
import Log
import traceback
import Generic as objGeneric
import GlobalVariables
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.common import *
from ibapi.contract import *
from threading import Thread
import random
from ibapi.utils import iswrapper
from tkinter import END
import time
from datetime import datetime , timedelta
from Bar import Bar
from collections import OrderedDict
class Main(EWrapper,EClient,GUI):
    
    def __init__(self):
        try:
            objGeneric.load_config()
            objGeneric.loadTickerBasket(GlobalVariables.tickerBasket)
            EClient.__init__(self,wrapper=self)
            GUI.__init__(self,1000,1600)
            self.IBConnect(GlobalVariables.ib_host,GlobalVariables.ib_port,random.randint(10,1000))
            self.display_ticker()
            self.mainForm.mainloop()
        except Exception as ex:
            Log.WriteLog("__init__",traceback.format_exc())

    def display_ticker(self):
        try:
            for item_ticker in GlobalVariables.ticker_collection.values():
                data =[[item_ticker.tickerID,item_ticker.symbol,item_ticker.secType,item_ticker.exchange,item_ticker.currency,0]]
                self.dgv_tickers.addRows(data)
        except Exception as ex:
            Log.WriteLog("loadTickers_to_table",traceback.format_exc())

    def IBConnect(self, ipaddress, portid, clientid):
        try:
            self.connect(ipaddress, portid, clientid)
            thread = Thread(target = self.run)
            thread.start()
        except Exception as ex:
            Log.WriteLog("IBConnect",traceback.format_exc())

    def messageToGUI(self,message):
        try:
            self.txtBox_message.insert(END,"\n ->"+message)
        except Exception as ex:
            Log.WriteLog("messageToGUI()",traceback.format_exc())            

    def reqMkData(self):
        try:
            for item_ticker in GlobalVariables.ticker_collection.values():
                self.reqMktData(item_ticker.tickerID,item_ticker.objIBContract,"",False,False,[])
        except Exception as ex:
            Log.WriteLog("reqMkData()",traceback.format_exc())

    def update_ltp_to_table(self):
        try:
            for row in self.dgv_tickers.treeview.get_children():
                tickerId = int(self.dgv_tickers.treeview.set(row, '#1'))
                if(tickerId in GlobalVariables.ticker_collection):
                    objTicker = GlobalVariables.ticker_collection[tickerId]
                    self.dgv_tickers.set_column_value(row,"#6",objTicker.ltp)
        except Exception as ex:
            Log.WriteLog("update_ltp_to_table",traceback.format_exc())
    
    def update_ltp_to_table_Thread(self):
        try:
            update_ltp_thread = Thread(target=self.update_ltp_to_table())
            #$update_ltp_thread.daemon = True
            update_ltp_thread.start()        
        except Exception as ex:
            Log.WriteLog("update_ltp_to_table_Thread",traceback.format_exc())
            
    def reqHistoryData(self):
        try:
            for item_ticker in GlobalVariables.ticker_collection.values():
                self.reqHistoricalData(item_ticker.tickerID,item_ticker.objIBContract,datetime.now().strftime("%Y%m%d %H:%M:%S"),"1 D",GlobalVariables.selectedTimeFrame, "MIDPOINT", 1, 1, False, [])
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"reqHistoryData")
            
    def setParam(self):
        try:
            GlobalVariables.ema_LongPeriod  = int(self.txtBox_emaPeriodLong_text.get())
            GlobalVariables.ema_ShortPeriod  = int(self.txtBox_emaPeriodShort_text.get())
            GlobalVariables.stochasticPeriod1  = int(self.txtBox_stochasticPeriod1_text.get())
            GlobalVariables.stochasticPeriod2  = int(self.txtBox_stochasticPeriod2_text.get())
            GlobalVariables.stochasticPeriod3  = int(self.txtBox_stochasticPeriod3_text.get())
            GlobalVariables.stochasticPeriod = GlobalVariables.stochasticPeriod1 + GlobalVariables.stochasticPeriod3
            GlobalVariables.selectedTimeFrame =  self.selectedEntryTF.get()
            GlobalVariables.TF = GlobalVariables.selectedTimeFrame_collection[GlobalVariables.selectedTimeFrame]
            GlobalVariables.commPer = float(self.txtBox_slippage_text.get()) # name is slippage but used for comm
            GlobalVariables.trade_qty = int(self.txtBox_tradeQty_text.get())
            GlobalVariables.longExitStoch = int(self.txtBox_longExitstoch_text.get())
            GlobalVariables.ShortExitStoch = int(self.txtBox_shortExitstoch_text.get())
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"setParam()")            

    def initCalculation(self,objTicker):
        try:
            if(True):
                if(len(objTicker.ohlc) > 0):
                    for objBar in objTicker.ohlc.values():
                        objTicker.handyData_close.update({objBar.dt : objBar.close})
                        objTicker.handyData_high.update({objBar.dt : objBar.high})
                        objTicker.handyData_low.update({objBar.dt : objBar.low})
                        if(len(objTicker.handyData_close) >= GlobalVariables.stochasticPeriod):
                            objBar.stochastic , objBar.stochastic_signal =  objGeneric.calculate_Stochastic([x for x in objTicker.handyData_high.values()],[x for x in objTicker.handyData_low.values()],[x for x in objTicker.handyData_close.values()],objTicker.pip,GlobalVariables.stochasticPeriod1,GlobalVariables.stochasticPeriod2,GlobalVariables.stochasticPeriod3) 
                            for key in sorted(objTicker.handyData_close.keys()):
                                objTicker.handyData_close.pop(key)
                                objTicker.handyData_high.pop(key)
                                objTicker.handyData_low.pop(key)
                                #print(key)
                                break
                        if(len(objTicker.handyData_close) >= GlobalVariables.ema_LongPeriod):
                            if(objBar.dt_prev in objTicker.ohlc):
                                objBarPrev = objTicker.ohlc[objBar.dt_prev]
                                if(objBarPrev.ema_Long == 0):
                                    objBar.ema_Long = objGeneric.sma([x for x in objTicker.handyData_close.values()],GlobalVariables.ema_LongPeriod,objTicker.pip)
                                else:
                                    objBar.ema_Long = objGeneric.ema(objBar.close,objBarPrev.ema_Long,GlobalVariables.ema_LongPeriod,objTicker.pip)
                        if(len(objTicker.handyData_close) >= GlobalVariables.ema_ShortPeriod):
                            if(objBar.dt_prev in objTicker.ohlc):
                                objBarPrev = objTicker.ohlc[objBar.dt_prev]
                                if(objBarPrev.ema_Short == 0):
                                    objBar.ema_Short = objGeneric.sma([x for x in objTicker.handyData_close.values()],GlobalVariables.ema_ShortPeriod,objTicker.pip)
                                else:
                                    objBar.ema_Short = objGeneric.ema(objBar.close,objBarPrev.ema_Short,GlobalVariables.ema_ShortPeriod,objTicker.pip)
            self.messageToGUI(objTicker.symbol+"  initial calculatio done !")
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"initCalculation")
    
    def set_dt_prev_next(self,objTicker):
        try:
            dt_prev = None
            for objBar in objTicker.ohlc.values():
                if(dt_prev in objTicker.ohlc):
                    objBar.dt_prev = objTicker.ohlc[dt_prev]
                    objBar.dt_next = objBar.dt
                objBar.dt_prev = dt_prev
                dt_prev = objBar.dt
                
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"set_dt_prev_next")

    def Simulate(self,objTicker,objBar):
        try:
            if(True):
                if(objBar.stochastic == 0):
                    return
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
                                return
                            if(GlobalVariables.objGeneric.checkfor_tgt_exit(objEntryOrder.action,objBar,objEntryOrder.target)):
                                GlobalVariables.objOrder.createExitOrder(objBar,objTicker,objEntryOrder,"TGT")
                                return
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
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"Simulate")
    #IB call back
        
    @iswrapper
    def error(self,reqId: TickerId , errorCode : int , errorString : str):
        try:
            self.messageToGUI(errorString)
            
            print("@ => errorCode : "+str(errorCode)+" message : "+errorString)

            if(errorCode == 504):
                self.IBConnect(GlobalVariables.ib_host,GlobalVariables.ib_port,random.randint(10,1000))
        except Exception as ex:
            Logs.WriteLog("error",traceback.format_exc())    

    @iswrapper
    def connectAck(self):
        try:
            print("@ Okay connected")
            GlobalVariables.IB_DateTime = datetime.now()
        except Exception as ex:
            Logs.WriteLog("connectAck",traceback.format_exc())

    @iswrapper
    def tickPrice(self, reqId, tickType, price, attrib):
        try:
            if(tickType == 4): # LTP
                if(reqId in GlobalVariables.ticker_collection):
                    objTicker = GlobalVariables.ticker_collection[reqId]
                    objTicker.ltp = price
                if(datetime.now() > GlobalVariables.IB_DateTime):
                    GlobalVariables.IB_DateTime += timedelta(seconds=5)
                    #print(datetime.now(),"Test")
                    self.update_ltp_to_table_Thread()
        except Exception as ex:
            Log.WriteLog("tickPrice",traceback.format_exc())

    @iswrapper
    def historicalData (self,reqId,bar):
        try:
            if(reqId in GlobalVariables.ticker_collection):
                objTicker = GlobalVariables.ticker_collection[reqId]
                objBar = Bar()
                objBar.dt = datetime.strptime(bar.date,'%Y%m%d %H:%M:%S')
                objBar.open = bar.open
                objBar.high = bar.high
                objBar.low = bar.low
                objBar.close = bar.close
                if(not objBar.dt in objTicker.ohlc):
                    objTicker.ohlc[objBar.dt] = objBar
                if(not objBar.dt in GlobalVariables.DateTime_collection):
                    GlobalVariables.DateTime_collection[objBar.dt] = 1        
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"historicalData")

    @iswrapper
    def historicalDataEnd(self, reqId: int, start: str, end: str):
        try:
            if(reqId in GlobalVariables.ticker_collection):
                objTicker = GlobalVariables.ticker_collection[reqId]
                self.set_dt_prev_next(objTicker)
                self.initCalculation(objTicker)
                self.reqRealTimeBars(objTicker.tickerID,objTicker.objIBContract, 5, "MIDPOINT", True, [])
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"historicalDataEnd")

    @iswrapper
    def realtimeBar(self, reqId: TickerId, time:int, open_: float, high: float, low: float, close: float,volume: int, wap: float, count: int): 
        try:
            if(reqId in GlobalVariables.ticker_collection):
                objTicker = GlobalVariables.ticker_collection[reqId]
                dt = datetime.fromtimestamp(time)
                if (objTicker.startConstruction == False and dt.second == 0 and (dt.minute % int(GlobalVariables.TF/60) == 0)):
                    objTicker.startConstruction = True
                    print("Constraction start",dt)
                if(objTicker.startConstruction == True):
                    #print(dt)
                    objBar =  objGeneric.createNewBar(GlobalVariables.TF/5,objTicker,dt,open_ ,high,low,close,volume,objTicker.pip)
                    if(not objBar == None):
                        # check for new trade or exit trade
                        objTicker.ohlc[objBar.dt] = objBar
                        print(objTicker.ohlc.keys())
                        print("Bar constacted",objBar.dt)
                        self.Simulate(objTicker, objBar)
                    
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"realtimeBar")
    
    #Event
    
    def btn_start_clickEvent(self):
        try:
            self.setParam()
            self.reqHistoryData()
        except Exception as ex:
            Log.WriteLog("btn_start_clickEvent",traceback.format_exc())

    def btn_showCalculation_clickEvent(self):
        try:
            symbol = self.cBox_showCalculationSymbols.get()
            if(symbol in GlobalVariables.ticker_id_collection):
                objTicker = GlobalVariables.ticker_collection[GlobalVariables.ticker_id_collection[symbol]]
                temp_collection = OrderedDict(reversed(list(objTicker.ohlc.items())))
                for objBar in temp_collection.values():
                    data = [[objBar.dt,objBar.open,objBar.high,objBar.low,objBar.close,objBar.volume,objBar.ema_Long,objBar.ema_Short,objBar.stochastic,objBar.stochastic_signal]]
                    self.dgv_calculation.addRows(data)
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"btn_showCalculation_clickEvent()")


main = Main()



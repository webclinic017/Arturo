import Log
import traceback
import GlobalVariables
class Orders():

    def __init__(self):
        try:
            self.orderId= 0
            self.parentOrderId = 0
            self.symbol = 0
            self.action = None
            self.p_dt = 0
            self.p_qty = 0
            self.p_price=0
            self.e_price=0
            self.sl = 0
            self.target = 0
            self.Points =0
            self.NET = 0
            self.totalPip=0
            self.status =None
            self.comm = 0
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"Orders.__init__()")

    def createEntryOrder(self ,objTicker,objBar, action):
        try:
            objEntryOrder = Orders()
            objEntryOrder.orderId = len(GlobalVariables.order_collections)+1
            objTicker.orderId = objEntryOrder.orderId
            objEntryOrder.symbol = objTicker.symbol
            objEntryOrder.action = action
            objEntryOrder.p_dt = objBar.dt
            price = 0
            if(objTicker.secType == "CASH"):
                temp = objTicker.spread / 2
                if(action == GlobalVariables.BUY):
                    price = objBar.close + (temp * objTicker.pip)
                else:
                    price = objBar.close - (temp * objTicker.pip)
            else:
                temp = objTicker.spread / 2
                if(action == GlobalVariables.BUY):
                    price = objBar.close + temp
                else:
                    price = objBar.close - temp
            objEntryOrder.p_price = objBar.close 
            objEntryOrder.e_price = GlobalVariables.objGeneric.roundToTickSize(price,objTicker.pip)
            objEntryOrder.p_qty = GlobalVariables.trade_qty
            if(objTicker.secType == "CASH"):
                objEntryOrder.sl = GlobalVariables.objGeneric.calculate_sl_pip(action,objEntryOrder.p_price,objTicker.stopLoss,objTicker.pip)
                objEntryOrder.target = GlobalVariables.objGeneric.calculate_tgt_pip(action,objEntryOrder.p_price,objTicker.target,objTicker.pip)
            elif(objTicker.secType == "STK"):
                objEntryOrder.sl = GlobalVariables.objGeneric.calculate_SL(action,objEntryOrder.p_price,objTicker.stopLoss,objTicker.pip)
                objEntryOrder.target = GlobalVariables.objGeneric.calculate_tgt(action,objEntryOrder.p_price,objTicker.target,objTicker.pip)
            objEntryOrder.status = GlobalVariables.OPEN
            GlobalVariables.order_collections[objEntryOrder.orderId] = objEntryOrder
        except Exception as ex:
            Log.WriteLog(ex,"createEntryOrder")
    
    def createExitOrder(self,objBar,objTicker,objEntryOrder,status):
        try:
            objExitOrder = Orders()
            objTicker.orderId = 0
            objTicker.isExit = False
            objExitOrder.orderId = len(GlobalVariables.order_collections)+1
            objExitOrder.parentOrderId = objEntryOrder.orderId
            objExitOrder.symbol = objEntryOrder.symbol
            objExitOrder.p_dt = objBar.dt
            price = objBar.close
            if(status == "SL"):
                price = objEntryOrder.sl
            if(status == "TGT"):
                price = objEntryOrder.target
                
            if(objTicker.secType == "CASH"):
                temp = objTicker.spread / 2
                if(objEntryOrder.action == GlobalVariables.SELL):
                    price = price + (temp * objTicker.pip)
                else:
                    price = price - (temp * objTicker.pip)
            else:
                temp = objTicker.spread / 2
                if(objEntryOrder.action == GlobalVariables.SELL):
                    price = price + temp
                else:
                    price = price - temp
            price = GlobalVariables.objGeneric.roundToTickSize(price,objTicker.pip)
            objExitOrder.p_price = objBar.close
            objExitOrder.e_price = price
            objExitOrder.p_qty = GlobalVariables.trade_qty
            if(objEntryOrder.action == GlobalVariables.BUY):
                objEntryOrder.Points = GlobalVariables.objGeneric.roundToTickSize(objExitOrder.p_price - objEntryOrder.p_price,objTicker.pip)
                objExitOrder.action = GlobalVariables.SELL
            else:
                objEntryOrder.Points = GlobalVariables.objGeneric.roundToTickSize(objEntryOrder.p_price - objExitOrder.p_price,objTicker.pip)
                objExitOrder.action = GlobalVariables.BUY
            temp = objEntryOrder.p_price * objExitOrder.p_qty
            temp = temp + (objExitOrder.p_price * objExitOrder.p_qty)
            objEntryOrder.comm = GlobalVariables.objGeneric.calculate_comm(temp,GlobalVariables.commPer)
            objEntryOrder.NET = GlobalVariables.objGeneric.roundToTickSize(objEntryOrder.Points * objEntryOrder.p_qty,objTicker.pip) - objEntryOrder.comm
            objEntryOrder.totalPip = GlobalVariables.objGeneric.roundToTickSize(objEntryOrder.Points /objTicker.pip,objTicker.pip)
            objExitOrder.status = status
            GlobalVariables.order_collections[objExitOrder.orderId] = objExitOrder
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"createExitOrder")
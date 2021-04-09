import Log
import traceback
import GlobalVariables
import Generic as objGeneric
from ibapi.order import Order
class Orders():


    def __init__(self):
        try:
            self.orderId= 0
            self.parentOrderId = 0
            self.stoplossOrderId = 0
            self.targetOrderId = 0
            self.objIBOrder = None
            self.orderName = ""
            self.symbol = 0
            self.action = None
            self.orderType = None
            self.p_dt = ""
            self.e_dt = ""
            self.p_qty = 0
            self.e_qty = 0
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
            objEntryOrder.orderId = GlobalVariables.OrderId
            GlobalVariables.OrderId += 1
            objEntryOrder.stoplossOrderId = GlobalVariables.OrderId
            GlobalVariables.OrderId += 1
            objEntryOrder.targetOrderId = GlobalVariables.OrderId
            GlobalVariables.OrderId += 1

            objEntryOrder.orderName = "EntryOrder"
            objEntryOrder.symbol = objTicker.symbol
            objEntryOrder.action = action
            objEntryOrder.orderType = GlobalVariables.ORDER_TYPE_MKT
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

            objEntryOrder.p_price = objGeneric.roundToTickSize(price,objTicker.pip)
            objEntryOrder.p_qty = objTicker.qty

            if(objTicker.secType == "CASH"):
                objEntryOrder.sl = objGeneric.calculate_sl_pip(action,objEntryOrder.p_price,objTicker.stopLoss,objTicker.pip)
                objEntryOrder.target = objGeneric.calculate_tgt_pip(action,objEntryOrder.p_price,objTicker.target,objTicker.pip)
            
            elif(objTicker.secType == "STK"):
                objEntryOrder.sl = objGeneric.calculate_SL(action,objEntryOrder.p_price,objTicker.stopLoss,objTicker.pip)
                objEntryOrder.target = objGeneric.calculate_tgt(action,objEntryOrder.p_price,objTicker.target,objTicker.pip)
            
            objEntryOrder.status = GlobalVariables.OPEN
            GlobalVariables.order_collections[objEntryOrder.orderId] = objEntryOrder
            
            return objEntryOrder
        except Exception as ex:
            Log.WriteLog(ex,"createEntryOrder")

    def create_stopLossOrder(self,objTicker,objEntryOrder):
        try:
            objOrder = Orders()
            objOrder.orderId = objEntryOrder.stoplossOrderId
            objOrder.parentOrderId = objEntryOrder.orderId
            objOrder.orderName = "StopLossOrder"            
            objOrder.symbol = objTicker.symbol
            objOrder.action = GlobalVariables.SELL
            if(objEntryOrder.action == GlobalVariables.SELL):
                objOrder.action = GlobalVariables.BUY
            objOrder.orderType = GlobalVariables.ORDER_TYPE_STP
            objOrder.p_dt = objEntryOrder.p_dt
            objOrder.p_price = objGeneric.roundToTickSize(objEntryOrder.sl,objTicker.pip)
            objOrder.p_qty = objEntryOrder.p_qty
            objEntryOrder.status = GlobalVariables.OPEN
            GlobalVariables.order_collections[objOrder.orderId] = objOrder  
            return objOrder     
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"create_stopLossOrder")

    def create_targetOrder(self,objTicker,objEntryOrder):
        try:
            objOrder = Orders()
            objOrder.orderId = objEntryOrder.targetOrderId
            objOrder.parentOrderId = objEntryOrder.orderId
            objOrder.orderName = "TargetOrder"            
            objOrder.symbol = objTicker.symbol
            objOrder.action = GlobalVariables.SELL
            if(objEntryOrder.action == GlobalVariables.SELL):
                objOrder.action = GlobalVariables.BUY
            objOrder.orderType = GlobalVariables.ORDER_TYPE_LMT
            objOrder.p_dt = objEntryOrder.p_dt
            objOrder.p_price = objGeneric.roundToTickSize(objEntryOrder.target,objTicker.pip)
            objOrder.p_qty = objEntryOrder.p_qty
            objEntryOrder.status = GlobalVariables.OPEN
            GlobalVariables.order_collections[objOrder.orderId] = objOrder       
            return objOrder
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"create_stopLossOrder")

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
            price = objGeneric.roundToTickSize(price,objTicker.pip)
            objExitOrder.p_price = price
            objExitOrder.p_qty = GlobalVariables.trade_qty
            if(objEntryOrder.action == GlobalVariables.BUY):
                objEntryOrder.Points = objGeneric.roundToTickSize(objExitOrder.p_price - objEntryOrder.p_price,objTicker.pip)
                objExitOrder.action = GlobalVariables.SELL
            else:
                objEntryOrder.Points = objGeneric.roundToTickSize(objEntryOrder.p_price - objExitOrder.p_price,objTicker.pip)
                objExitOrder.action = GlobalVariables.BUY
            temp = objEntryOrder.p_price * objExitOrder.p_qty
            temp = temp + (objExitOrder.p_price * objExitOrder.p_qty)
            objEntryOrder.comm = objGeneric.calculate_comm(temp,GlobalVariables.commPer)
            objEntryOrder.NET = objGeneric.roundToTickSize(objEntryOrder.Points * objEntryOrder.p_qty,objTicker.pip) - objEntryOrder.comm
            objEntryOrder.totalPip = objGeneric.roundToTickSize(objEntryOrder.Points /objTicker.pip,objTicker.pip)
            objExitOrder.status = status
            GlobalVariables.order_collections[objExitOrder.orderId] = objExitOrder
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"createExitOrder")


    def shoot_parent_orders_to_IB(self,objOrder):
        try:
            objOrder.objIBOrder = Order()
            objOrder.objIBOrder.orderId = objOrder.orderId
            objOrder.objIBOrder.totalQuantity = objOrder.p_qty
            objOrder.objIBOrder.action = objOrder.action
            objOrder.objIBOrder.orderType = objOrder.orderType
            if(objOrder.objIBOrder.orderType == GlobalVariables.ORDER_TYPE_MKT):
                objOrder.objIBOrder.lmtPrice = 0
            else:
                objOrder.objIBOrder.lmtPrice = objOrder.p_price
            objOrder.objIBOrder.transmit = False
            objOrder.objIBOrder.orderRef = str(objOrder.orderId)
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"shoot_orders_to_IB")

    def shoot_stopLoss_order_to_IB(self,objOrder):
        try:
            objOrder.objIBOrder = Order()
            objOrder.objIBOrder.orderId = objOrder.orderId
            objOrder.objIBOrder.parentId = objOrder.parentOrderId
            objOrder.objIBOrder.totalQuantity = objOrder.p_qty
            objOrder.objIBOrder.action = objOrder.action
            objOrder.objIBOrder.orderType = objOrder.orderType
            objOrder.objIBOrder.auxPrice = objOrder.p_price
            objOrder.objIBOrder.transmit = False
            objOrder.objIBOrder.orderRef = str(objOrder.orderId)

        except Exception as ex :
            Log.WriteLog(traceback.format_exc(),"shoot_parent_orders_to_IB")

    def shooty_target_order_to_IB(self,objOrder):
        try:
            objOrder.objIBOrder = Order()
            objOrder.objIBOrder.orderId = objOrder.orderId
            objOrder.objIBOrder.parentId = objOrder.parentOrderId
            objOrder.objIBOrder.totalQuantity = objOrder.p_qty
            objOrder.objIBOrder.action = objOrder.action
            objOrder.objIBOrder.orderType = objOrder.orderType
            objOrder.objIBOrder.lmtPrice = objOrder.p_price
            objOrder.objIBOrder.transmit = True
            objOrder.objIBOrder.orderRef = str(objOrder.orderId)  
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"shooty_target_order_to_IB")

    def shoot_exit_order_to_IB(self,objEntryOrder):
        try:
            if(objEntryOrder.stoplossOrderId in GlobalVariables.order_collections):
                objOrder = GlobalVariables.order_collections[objEntryOrder.orderId]
                objOrder.objIBOrder.orderType = GlobalVariables.ORDER_TYPE_MKT
                objOrder.objIBOrder.lmtPrice = 0
                return objOrder
            return None
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"shoot_exit_order_to_IB")
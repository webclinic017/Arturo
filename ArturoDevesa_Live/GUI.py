import tkinter as Tkinter
import Log as Logs
import traceback
from tkinter import ttk,Text
import GlobalVariables
from GridView import GridView
from tkinter.ttk import * 
class GUI(): 
    def __init__(self,height:"Height of mainWindow",width:"Width of mainWindow"):
        try:
            self.width = width
            self.heigth = height
            self.btn_width=15
            self.btn_height=3
            # All widget variable
            self.mainForm = Tkinter.Tk()
            self.TabControl=None
            self.tradeTab = None
            self.messageTab = None
            self.scriptListTab= None
            self.calculationTab = None
            self.btn_showCalculation = None

            self.dgv_tickers = None
            self.dgv_calculation = None
            self.dgv_trades = None
            self.cBox_showCalculationSymbols = None 
            
            self.txtBox_message=None
            self.txtBox_message_text= Tkinter.StringVar()

            self.btn_start=None
            
            self.txtBox_emaPeriodLong=None
            self.txtBox_emaPeriodLong_text= Tkinter.StringVar()
            
            self.txtBox_emaPeriodShort=None
            self.txtBox_emaPeriodShort_text= Tkinter.StringVar()
            
            self.txtBox_stochasticPeriod1=None
            self.txtBox_stochasticPeriod1_text= Tkinter.StringVar()

            self.txtBox_stochasticPeriod2=None
            self.txtBox_stochasticPeriod2_text= Tkinter.StringVar()

            self.txtBox_stochasticPeriod3=None
            self.txtBox_stochasticPeriod3_text= Tkinter.StringVar()


            self.txtBox_longExitstoch=None
            self.txtBox_longExitstoch_text= Tkinter.StringVar()

            self.txtBox_shortExitstoch=None
            self.txtBox_shortExitstoch_text= Tkinter.StringVar()
            
            self.txtBox_slippage =None
            self.txtBox_slippage_text= Tkinter.StringVar()

            self.txtBox_startTradeHr=None
            self.txtBox_startTradeHr_text= Tkinter.StringVar()

            self.txtBox_startTradeMin=None
            self.txtBox_startTradeMin_text= Tkinter.StringVar()

            self.txtBox_stopTradeHr=None
            self.txtBox_stopTradeHr_text= Tkinter.StringVar()

            self.txtBox_stopTradeMin=None
            self.txtBox_stopTradeMin_text= Tkinter.StringVar()

            self.txtBox_EODHr=None
            self.txtBox_EODHr_text= Tkinter.StringVar()

            self.txtBox_EODMin=None
            self.txtBox_EODMin_text= Tkinter.StringVar()
            
            self.selectedEntryTF= Tkinter.StringVar()  #comboBox selectedvalues store init
            self.selectedExitTF= Tkinter.StringVar()   # comboBox selectedvalues store init

            self.txtBox_tradeQty =None
            self.txtBox_tradeQty_text = Tkinter.StringVar() 
            #Init
            self.mainForm.title = "Tvisi"
            self.mainForm.geometry(str(width)+"x"+str(height))
            self.TopFrame = Tkinter.Frame(self.mainForm,width=width,height=self.calculatePer(10,height))
            self.set_Top_Frame_GUI()
            self.TopFrame.pack(fill="both",expand=1)
            self.set_Bottom_Frame_GUI(50)
            #self.mainForm.resizable(0,0)    
        except Exception as ex:
            Logs.WriteLog(traceback.format_exc(),"__init__()")
        
    def calculatePer(self,per,total):
        try:
            return int(per * total / 100)
        except Exception as ex:
            Logs.WriteLog(traceback.format_exc(),"calculatePer()")

    def set_Bottom_Frame_GUI(self,per):
        try:
            #init tabControl
            self.TabControl = ttk.Notebook(self.mainForm,width=self.width,height=self.calculatePer(per,self.heigth))
            
            #init tabs
            self.tradeTab = ttk.Frame(self.TabControl,width=self.width,height=self.calculatePer(per,self.heigth))
            self.messageTab = ttk.Frame(self.TabControl,width=self.width,height=self.calculatePer(per,self.heigth))
            self.scriptListTab = ttk.Frame(self.TabControl,width=self.width,height=self.calculatePer(per,self.heigth))
            self.calculationTab = ttk.Frame(self.TabControl,width=self.width,height=self.calculatePer(per,self.heigth))
            #Adding tab to tabControl
            self.TabControl.add(self.tradeTab, text ='Trades')
            self.TabControl.add(self.scriptListTab,text='Script')
            self.TabControl.add(self.calculationTab,text = 'Calculation')
            self.TabControl.add(self.messageTab, text ='Message')
            #add widget to messageTab
            self.txtBox_message = Text(self.messageTab,width=self.width,height=self.calculatePer(per,self.heigth))
            self.txtBox_message.pack()
            #self.txtBox_message.insert(Tkinter.END,"Hello world")
            self.TabControl.pack(expand = 1, fill ="both")
            
            #add widget to scriptListTab
            self.createTable_tickersLTP(self.scriptListTab)
            
            #add widget to calculation tab
            temp_frame_calculation = ttk.Frame(self.calculationTab,width=self.width,height=self.calculatePer(5,self.heigth))
            temp_frame_calculation.pack(side = 'top')
            
            self.btn_showCalculation = Tkinter.Button(temp_frame_calculation, text ="Show",width=self.btn_width , command = self.btn_showCalculation_clickEvent) #,width=self.btn_width,height=self.btn_height)
            self.btn_showCalculation.place(x=150,y=20)
            
            
            self.cBox_showCalculationSymbols = ttk.Combobox(temp_frame_calculation, width = 12, textvariable = self.cBox_showCalculationSymbols) 
            self.cBox_showCalculationSymbols['values'] = tuple((x.symbol  for x in GlobalVariables.ticker_collection.values()))
            self.cBox_showCalculationSymbols.current(0)             
            self.cBox_showCalculationSymbols.place(x=50,y=20)            
            
            temp_frame_gridVew = ttk.Frame(self.calculationTab,width=self.width,height=self.calculatePer(70,self.heigth))
            temp_frame_gridVew.pack(expand = 1 ,fill = 'both')

            temp_frame_gridVew_1 = ttk.Frame(self.tradeTab,width=self.width,height=self.calculatePer(70,self.heigth))
            temp_frame_gridVew_1.pack(expand = 1 ,fill = 'both')

            # set grid view to calculation on calulation tab
            self.dgv_calculation = GridView(temp_frame_gridVew)
            temp_heading = ['DT','Open','high','low','close','volume','EMA_long','EMA_Short','Stochastic','Stochastic signals']
            self.dgv_calculation.set_columns(temp_heading)
            self.dgv_calculation.treeview.place(x=1,y=1)

            # set gridvew to trades table 

            self.dgv_trades = GridView(temp_frame_gridVew_1)
            temp_heading = ['OrderId','Parent_orderId','StopLoss_orderId','Target_orderId','Symbol','Action','P_dt','E_dt','P_qty','E_qty','P_price','E_price','Status']
            self.dgv_trades.set_columns(temp_heading)
            self.dgv_trades.treeview.place(x=1,y=1)


        except Exception as ex:
            Logs.WriteLog(traceback.format_exc(),"set_Tab_to_GUI()")

    def createTable_tickersLTP(self,frame):
        try:
            columns = ["Id","Symbol","SecType","Exchange","Curr","LTP"]
            self.dgv_tickers = GridView(frame)
            self.dgv_tickers.set_columns(columns = columns)
            #self.dgv_News.dataSource(data)
            self.dgv_tickers.treeview.place(x=1,y=1)
        except Exception as ex:
            Logs.WriteLog(traceback.format_exc(),"set_table_to_scriptTab")

    def set_table_to_scriptTab(self):
        try:
            i=0
            heading = ["Symbol","SecType","Exchange","Currency","Pip","Spread","Target","StopLoss"]
            for obj in GlobalVariables.ticker_collection.values():
                values = [obj.symbol,obj.secType,obj.exchange,obj.currency,obj.pip,obj.spread,obj.target,obj.stopLoss]
                if(i==0):
                    for j in range(len(heading)):                   
                        entry = Tkinter.Entry(self.scriptListTab,width=12,font=('Arial',10,'bold'))
                        entry.grid(row=0, column=j) 
                        entry.insert(Tkinter.END, heading[j])                    
                for j in range(len(values)):                   
                    entry = Tkinter.Entry(self.scriptListTab,width=12)
                    entry.grid(row=i+1, column=j) 
                    entry.insert(Tkinter.END, values[j])
                i+=1 
        except Exception as ex:
            Logs.WriteLog(traceback.format_exc(),"set_table_to_scriptTab")

        def edit_item():
            focused = self.treeview.focus()
            x = input('Enter a Value you want to change')
            self.treeview.insert("", str(focused)[1:], values=("", str(x)))
            self.treeview.delete(focused)

    def set_Top_Frame_GUI(self):
        try:
            #Button
            self.btn_start = Tkinter.Button(self.TopFrame, text ="Start", command = self.btn_start_clickEvent,width=self.btn_width) #,width=self.btn_width,height=self.btn_height)
            self.btn_start.place(x=50,y=20)
            #label 
            lable11 = Tkinter.Label(self.TopFrame,text="Entry TF")
            lable11.place(x=350,y=80)
            #comboBox
            entryTF = ttk.Combobox(self.TopFrame, width = 12, textvariable = self.selectedEntryTF) 
            entryTF['values'] = ('1 min','3 mins','5 mins','15 mins','1 hour')
            entryTF.current(0)             
            entryTF.place(x=350,y=100)

            #label
            lable12 = Tkinter.Label(self.TopFrame,text="EMA Period-Long")
            lable12.place(x=500,y=80)

            #textBox
            self.txtBox_emaPeriodLong_text.set("5")
            self.txtBox_emaPeriodLong = Tkinter.Entry(self.TopFrame,width=10,textvariable = self.txtBox_emaPeriodLong_text)
            self.txtBox_emaPeriodLong.place(x=500,y=100)

            #label
            label3 = Tkinter.Label(self.TopFrame,text="EMA Period-Short")
            label3.place(x=650,y=80)

            #textBox
            self.txtBox_emaPeriodShort_text.set("3")
            self.txtBox_emaPeriodShort = Tkinter.Entry(self.TopFrame,width=10,textvariable = self.txtBox_emaPeriodShort_text)
            self.txtBox_emaPeriodShort.place(x=650,y=100)            

            #label
            label4 = Tkinter.Label(self.TopFrame,text="Stochastic Period-1")
            label4.place(x=800,y=80)

            #textBox
            self.txtBox_stochasticPeriod1_text.set("7")
            self.txtBox_stochasticPeriod1 = Tkinter.Entry(self.TopFrame,width=10,textvariable = self.txtBox_stochasticPeriod1_text)
            self.txtBox_stochasticPeriod1.place(x=800,y=100)

            #label
            label5 = Tkinter.Label(self.TopFrame,text="Stochastic Period-2")
            label5.place(x=950,y=80)

            #textBox
            self.txtBox_stochasticPeriod2_text.set("7")
            self.txtBox_stochasticPeriod2 = Tkinter.Entry(self.TopFrame,width=10,textvariable = self.txtBox_stochasticPeriod2_text)
            self.txtBox_stochasticPeriod2.place(x=950,y=100)

            #label
            label6 = Tkinter.Label(self.TopFrame,text="Stochastic Period-3")
            label6.place(x=1100,y=80)

            #textBox
            self.txtBox_stochasticPeriod3_text.set("3")
            self.txtBox_stochasticPeriod3 = Tkinter.Entry(self.TopFrame,width=10,textvariable = self.txtBox_stochasticPeriod3_text)
            self.txtBox_stochasticPeriod3.place(x=1100,y=100)
            
            #label
            label7 = Tkinter.Label(self.TopFrame,text="Long Exit (stoch)")
            label7.place(x=350,y=160)

            #textBox
            self.txtBox_longExitstoch_text.set("20")
            self.txtBox_longExitstoch_text = Tkinter.Entry(self.TopFrame,width=10,textvariable = self.txtBox_longExitstoch_text)
            self.txtBox_longExitstoch_text.place(x=350,y=180)

            #label
            label8 = Tkinter.Label(self.TopFrame,text="Short Exit (stoch)")
            label8.place(x=500,y=160)

            #textBox
            self.txtBox_shortExitstoch_text.set("80")
            self.txtBox_shortExitstoch_text = Tkinter.Entry(self.TopFrame,width=10,textvariable = self.txtBox_shortExitstoch_text)
            self.txtBox_shortExitstoch_text.place(x=500,y=180)

            # #label
            # label9 = Tkinter.Label(self.TopFrame,text="Long Exit (stoch)")
            # label9.place(x=650,y=160)

            # #textBox
            
            # self.txtBox_longExitstoch_text.set("80")
            # self.txtBox_longExitstoch = Tkinter.Entry(self.TopFrame,width=10,textvariable = self.txtBox_longExitstoch_text)
            # self.txtBox_longExitstoch.place(x=650,y=180)

            # #label
            # label10 = Tkinter.Label(self.TopFrame,text="Short Exit (stoch)")
            # label10.place(x=800,y=160)

            # #TextBox
            # self.txtBox_shortExitstoch_text.set("20")
            # self.txtBox_shortExitstoch = Tkinter.Entry(self.TopFrame,width=10,textvariable = self.txtBox_shortExitstoch_text)
            # self.txtBox_shortExitstoch.place(x=800,y=180)

            # #label
            # label11 = Tkinter.Label(self.TopFrame,text="Start Trade (hr/Min)")
            # label11.place(x=350,y=240)

            # #textBox
            # self.txtBox_startTradeHr_text.set("2")
            # self.txtBox_startTradeMin_text.set("0")
            # self.txtBox_startTradeHr = Tkinter.Entry(self.TopFrame,width=5,textvariable = self.txtBox_startTradeHr_text)
            # self.txtBox_startTradeHr.place(x=350,y=260)            
            # self.txtBox_startTradeMin = Tkinter.Entry(self.TopFrame,width=5,textvariable = self.txtBox_startTradeMin_text)
            # self.txtBox_startTradeMin.place(x=400,y=260)    

            # #label
            # label12 = Tkinter.Label(self.TopFrame,text="Stop Trade (hr/Min)")
            # label12.place(x=500,y=240)

            # #textBox
            # self.txtBox_stopTradeHr_text.set("11")
            # self.txtBox_stopTradeMin_text.set("0")
            # self.txtBox_stopTradeHr = Tkinter.Entry(self.TopFrame,width=5,textvariable = self.txtBox_stopTradeHr_text)
            # self.txtBox_stopTradeHr.place(x=500,y=260)            
            # self.txtBox_stopTradeMin = Tkinter.Entry(self.TopFrame,width=5,textvariable = self.txtBox_stopTradeMin_text)
            # self.txtBox_stopTradeMin.place(x=550,y=260)    

            # #label
            # label13 = Tkinter.Label(self.TopFrame,text="EOD (hr/Min)")
            # label13.place(x=650,y=240)

            # #textBox
            # self.txtBox_EODHr_text.set("11")
            # self.txtBox_EODMin_text.set("55")

            # self.txtBox_EODHr = Tkinter.Entry(self.TopFrame,width=5,textvariable = self.txtBox_EODHr_text)
            # self.txtBox_EODHr.place(x=650,y=260)            
            # self.txtBox_EODMin = Tkinter.Entry(self.TopFrame,width=5,textvariable = self.txtBox_EODMin_text)
            # self.txtBox_EODMin.place(x=700,y=260)    

        except Exception  as ex:
            Logs.WriteLog(ex,"set_Top_Frame_GUI")

    def btn_start_clickEvent(self):
        try:
            pass
        except Exception as ex:
            Logs.WriteLog(ex,"btn_start_click()")

    def insertText(self,extBox:"TextBox instance",value:"Text to Enter"):#to insert text to textBox
        try:
            self.txtBox_emaPeriodLong.insert(Tkinter.END,str(value))
            self.txtBox_emaPeriodLong.update()
        except Exception as ex:
            Logs.WriteLog(traceback.format_exc(),"GUI.insertText")

    def btn_showCalculation_clickEvent(self):
        try:
            pass
        except Exception as ex:
            Logs.WriteLog(ex,"btn_showCalculation_clickEvent()")
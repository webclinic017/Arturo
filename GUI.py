import tkinter as Tkinter
import Log
import traceback
from tkinter import ttk,Text
import GlobalVariables
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
            self.set_Bottom_Frame_GUI(80)
            #self.mainForm.resizable(0,0)    
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"__init__()")
        
    def calculatePer(self,per,total):
        try:
            return int(per * total / 100)
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"calculatePer()")

    def set_Bottom_Frame_GUI(self,per):
        try:
            #init tabControl
            self.TabControl = ttk.Notebook(self.mainForm,width=self.width,height=self.calculatePer(per,self.heigth))
            
            #init tabs
            self.tradeTab = ttk.Frame(self.TabControl,width=self.width,height=self.calculatePer(per,self.heigth))
            self.messageTab = ttk.Frame(self.TabControl,width=self.width,height=self.calculatePer(per,self.heigth))
            self.scriptListTab = ttk.Frame(self.TabControl,width=self.width,height=self.calculatePer(per,self.heigth))
            
            #Adding tab to tabControl
            self.TabControl.add(self.messageTab, text ='Message')
            self.TabControl.add(self.scriptListTab,text='Script')
            self.TabControl.add(self.tradeTab, text ='Trades')

            #add widget to messageTab
            self.txtBox_message = Text(self.messageTab,width=self.width,height=self.calculatePer(per,self.heigth))
            self.txtBox_message.pack()
            #elf.txtBox_message.insert(Tkinter.END,"Hello world")
            self.TabControl.pack(expand = 1, fill ="both")

            #add widget to scriptListTab
            self.set_table_to_scriptTab()

        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"set_Tab_to_GUI()")

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
            Log.WriteLog(traceback.format_exc(),"set_table_to_scriptTab")

    

    def set_Top_Frame_GUI(self):
        try:
            #Button
            self.btn_start = Tkinter.Button(self.TopFrame, text ="Start", command = self.btn_start_clickEvent,width=self.btn_width) #,width=self.btn_width,height=self.btn_height)
            self.btn_start.place(x=50,y=20)
            # #label 
            # lable11 = Tkinter.Label(self.TopFrame,text="Entry TF")
            # lable11.place(x=350,y=80)
            # #comboBox
            # entryTF = ttk.Combobox(self.TopFrame, width = 12, textvariable = self.selectedEntryTF) 
            # entryTF['values'] = ('1min','3mins','5mins','15mins','1hour')
            # entryTF.current(0)             
            # entryTF.place(x=350,y=100)

            # #label
            # lable12 = Tkinter.Label(self.TopFrame,text="EMA Period-Long")
            # lable12.place(x=500,y=80)

            # #textBox
            # self.txtBox_emaPeriodLong_text.set("5")
            # self.txtBox_emaPeriodLong = Tkinter.Entry(self.TopFrame,width=10,textvariable = self.txtBox_emaPeriodLong_text)
            # self.txtBox_emaPeriodLong.place(x=500,y=100)

            # #label
            # label3 = Tkinter.Label(self.TopFrame,text="EMA Period-Short")
            # label3.place(x=650,y=80)

            # #textBox
            # self.txtBox_emaPeriodShort_text.set("3")
            # self.txtBox_emaPeriodShort = Tkinter.Entry(self.TopFrame,width=10,textvariable = self.txtBox_emaPeriodShort_text)
            # self.txtBox_emaPeriodShort.place(x=650,y=100)            

            # #label
            # label4 = Tkinter.Label(self.TopFrame,text="Stochastic Period-1")
            # label4.place(x=800,y=80)

            # #textBox
            # self.txtBox_stochasticPeriod1_text.set("7")
            # self.txtBox_stochasticPeriod1 = Tkinter.Entry(self.TopFrame,width=10,textvariable = self.txtBox_stochasticPeriod1_text)
            # self.txtBox_stochasticPeriod1.place(x=800,y=100)

            # #label
            # label5 = Tkinter.Label(self.TopFrame,text="Stochastic Period-2")
            # label5.place(x=950,y=80)

            # #textBox
            # self.txtBox_stochasticPeriod2_text.set("7")
            # self.txtBox_stochasticPeriod2 = Tkinter.Entry(self.TopFrame,width=10,textvariable = self.txtBox_stochasticPeriod2_text)
            # self.txtBox_stochasticPeriod2.place(x=950,y=100)

            # #label
            # label6 = Tkinter.Label(self.TopFrame,text="Stochastic Period-3")
            # label6.place(x=1100,y=80)

            # #textBox
            # self.txtBox_stochasticPeriod3_text.set("3")
            # self.txtBox_stochasticPeriod3 = Tkinter.Entry(self.TopFrame,width=10,textvariable = self.txtBox_stochasticPeriod3_text)
            # self.txtBox_stochasticPeriod3.place(x=1100,y=100)
            
            # #label
            # label7 = Tkinter.Label(self.TopFrame,text="Comm %")
            # label7.place(x=350,y=160)

            # #textBox
            # self.txtBox_slippage_text.set("0")
            # self.txtBox_slippage = Tkinter.Entry(self.TopFrame,width=10,textvariable = self.txtBox_slippage_text)
            # self.txtBox_slippage.place(x=350,y=180)

            # #label
            # label8 = Tkinter.Label(self.TopFrame,text="Trade Qty")
            # label8.place(x=500,y=160)

            # #textBox
            # self.txtBox_tradeQty_text.set("100000")
            # self.txtBox_tradeQty = Tkinter.Entry(self.TopFrame,width=10,textvariable = self.txtBox_tradeQty_text)
            # self.txtBox_tradeQty.place(x=500,y=180)

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
            Log.WriteLog(ex,"set_Top_Frame_GUI")

    def btn_start_clickEvent(self):
        try:
            pass
        except Exception as ex:
            Log.WriteLog(ex,"btn_start_click()")

    def insertText(self,extBox:"TextBox instance",value:"Text to Enter"):#to insert text to textBox
        try:
            self.txtBox_emaPeriodLong.insert(Tkinter.END,str(value))
            self.txtBox_emaPeriodLong.update()
        except Exception as ex:
            Log.WriteLog(traceback.format_exc(),"GUI.insertText")

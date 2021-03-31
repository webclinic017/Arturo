from tkinter import ttk 
import tkinter as tk 
import traceback   
import GlobalVariables
# Creating tkinter window 
class GridView():

    def __init__(self,window):
        try:
            self.treeview = ttk.Treeview(window, selectmode ='browse',height=30)
            self.treeview['show'] = 'headings'
            verscrlbar = ttk.Scrollbar(window,orient ="vertical",command = self.treeview.yview) 
            verscrlbar.pack(side ='right', fill ='x') 
            self.treeview.configure(xscrollcommand = verscrlbar.set)
            # set Theme
            s = ttk.Style(window)
            s.theme_use("clam")
        except Exception as ex:
            print(traceback.format_exc(),"GridView.__init__()")

    def set_columns(self,columns):
        try:
            no_col = tuple([str(x) for x in range(len(columns))])
            self.treeview["columns"] = no_col
            self.treeview['show'] = 'headings'
            
            for i in no_col:
                self.treeview.column(i, width = 100 , anchor ='c')        
                self.treeview.heading(i, text =columns[int(i)])
        except Exception as ex:
            print(traceback.format_exc(),"GridView.set_columns")

    def addRows(self,data):
        try:
            for row in data:
                self.treeview.insert("", 'end', text ="L1",values =tuple(row))
        except Exception as ex:
            print(traceback.format_exc(),"GridView.dataSource")

    def add_color(self):
        try:
            self.treeview.tag_configure(GlobalVariables.POS,foreground='green',background='white')
            self.treeview.tag_configure(GlobalVariables.NEG,foreground='red' , background='white')
        except Exception as ex:
            print(traceback.format_exc(),"GridView.add_color()")

    def clear_treeView(self):
        try:
            for i in self.treeview.get_children():
                self.treeview.delete(i)
        except Exception as ex:
            print("clear_treeView",traceback.format_exc())
    def set_column_value(self,item,index,value):
        try:
            self.treeview.set(item,index,value)
        except  Exception as ex:
            print(traceback.format_exc(),"set_column_value")
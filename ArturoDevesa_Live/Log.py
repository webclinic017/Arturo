# -*- coding: utf-8 -*-
"""
@author: smit
"""
from os import path
import GlobalVariables
from datetime import datetime 
def WriteLog(error,method):
    try:
        print("Exception logged ")
        if(path.exists(GlobalVariables.ExceptionLog) == False):      
            file = open(GlobalVariables.ExceptionLog,"w+")
            file.write("Date : "+str(datetime.now())+"\n")
            file.write("Method : "+str(method) +"\n")
            file.write("Errror : "+str(error) +"\n")
            file.write("-------------------------------------------------------------------------\n")      
            file.close()
        if(path.exists(GlobalVariables.ExceptionLog) == True):
            file = open(GlobalVariables.ExceptionLog,"a+")
            file.write("Date : "+str(datetime.now())+"\n")
            file.write("Method : "+str(method) +"\n")
            file.write("Errror : "+str(error) +"\n")
            file.write("-------------------------------------------------------------------------\n")      
            file.close()
    except Exception as ex:
        print("Error Log.patternLog : ",ex)
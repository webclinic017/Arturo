# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 11:16:20 2021

@author: Owner
"""
import Log
import traceback
class Bar():
    def __init__(self):
        try:
            self.dt = None
            self.dt_prev = None
            self.open = 0
            self.high = 0
            self.low = 0
            self.close = 0
            self.volume = 0
            self.count = 0
            self.ema_Long=0
            self.ema_Short=0
            self.stochastic = 0
            self.stochastic_signal = 0   
            self.count = 0
        except Exception as ex:
           Log.WriteLog(traceback.format_exc(),"__init__")
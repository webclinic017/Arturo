import matplotlib.pyplot as plt
import matplotlib.ticker as mTicker
import matplotlib.dates as mDate
import mplfinance
import traceback
import Log
import GlobalVariables
import numpy as np
import pandas as pd



def loadGraph(symbol:"Name"):
    try:
        fileName =  GlobalVariables.calculationDataPath+symbol+".csv"
        data = pd.read_csv(fileName,parse_dates=True)
        data = data.set_index('DateTime')
        data.index.name = 'Date'
        print(data.head(10))
        mplfinance.plot(data,type='candle')

        # fig = plt.figure()
        # ax1 = plt.subplot(1,1,1)
        # ax1.xaxis.set_major_locator(mTicker.MaxNLocator(10))
        # ax1.xaxis.set_major_formatter(mDate.DateFormatter('%m/%d/%Y %H:%M'))

        # for label in ax1.xaxis.get_ticklabels():
        #     label.set_rotation(45)

        # plt.show()
    except Exception as ex:
        Log.WriteLog(traceback.format_exc(),"loadGraph")

def bytespdate2num(fmt, encoding='utf-8'):
    def bytesconverter(b):
        s = b.decode(encoding)
        return (mDate.datestr2num(s))
    return bytesconverter

loadGraph("NIFTY50")
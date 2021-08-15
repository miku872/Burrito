import os.path
import start
import pandas as pd
import Constants

projectPath = Constants.ProjectPath
def getEMA(symbol, window, candleSize, apiProvider=None, timeSeries=None, interval=None):
    if timeSeries is None:
        if os.path.exists(projectPath + "/resources/" + symbol + "/" + candleSize):
            timeSeries = pd.read_json(projectPath + "/resources/" + symbol + "/" + candleSize + "/" + symbol + ".json",
                                      convert_dates=True)
        else:
            start.getSeries(apiProvider, symbol, candleSize)
            return getEMA(symbol, window, candleSize, interval)

    if interval is not None:
        df_mask = (interval[0] < timeSeries['timestamp']) & (timeSeries['timestamp'] < interval[1])
        timeSeries = timeSeries[df_mask]

    timeSeries['EMA' + str(window)] = timeSeries['Close'].ewm(span=window, adjust=False).mean()
    return timeSeries

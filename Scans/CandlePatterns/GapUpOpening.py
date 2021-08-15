import os.path
import start
import pandas as pd
import numpy as np
from Scans.Scan import Scan
from Technicals.Technicals import Technicals
import Constants

projectPath = Constants.ProjectPath


class GapUpOpening(Scan):
    def __init__(self):
        pass

    def isCriteriaMet(self, symbol, candleSize="DAILY", apiProvider=None, timeSeries=None, interval=None):
        if timeSeries is None:
            if os.path.exists(projectPath + "/resources/" + symbol + "/" + candleSize):
                timeSeries = pd.read_json(
                    projectPath + "/resources/" + symbol + "/" + candleSize + "/" + symbol + ".json",
                    convert_dates=True)
            else:
                timeSeries = start.getSeries(apiProvider, symbol, candleSize)
                if timeSeries is not None:
                    return self.isCriteriaMet(symbol, candleSize, interval)
                else:
                    return False

        if interval is not None:
            df_mask = (interval[0] <= timeSeries['timestamp']) & (timeSeries['timestamp'] <= interval[1])
            timeSeries = timeSeries[df_mask]

        if timeSeries is not None:
            technicals = Technicals(symbol, timeSeries, apiProvider=apiProvider)
            close0 = technicals.Close(candleSize)
            close1 = technicals.Close(candleSize, 1)
            open0 = technicals.Open(candleSize)
            open1 = technicals.Open(candleSize, 1)
            low0 = technicals.Low(candleSize)
            low1 = technicals.Low(candleSize, 1)
            high0 = technicals.High(candleSize)
            high1 = technicals.High(candleSize, 1)
            timeSeries['Signal'] = np.where(np.logical_and(timeSeries['Open'] > timeSeries['Close'].shift(),
                                                           timeSeries['Close'] > timeSeries['High'].shift()), 1, 0)
        return timeSeries

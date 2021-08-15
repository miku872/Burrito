import os.path
import start
import pandas as pd
from Scans.Scan import Scan
from Technicals.Technicals import Technicals
import Constants

projectPath = Constants.ProjectPath


class Hammer(Scan):
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
            open0 = technicals.Open(candleSize)
            low0 = technicals.Low(candleSize)
            high0 = technicals.High(candleSize)

            if ((close0 > open0 > low0 and (open0 - low0) >= 3 * (close0 - open0) and (high0 - close0) < (
                    close0 - open0)) or
                    (open0 > close0 > low0 and (close0 - low0) >= 3 * (open0 - close0) and (high0 - open0) < (
                            open0 - close0))):
                return True
        return False

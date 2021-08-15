import os.path
import start
import pandas as pd
from Scans.MACrossOver.MACrossOverScan import isMACrossOver
from Scans.Scan import Scan
import Constants

projectPath = Constants.ProjectPath


class Day20SMACrossDay200SMAFromAbove(Scan):
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
            return isMACrossOver(symbol, [200,20], "SMA", candleSize=candleSize, timeSeries=timeSeries)

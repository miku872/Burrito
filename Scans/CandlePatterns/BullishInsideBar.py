import os.path
import start
import pandas as pd
from Scans.Scan import Scan
from Technicals.Technicals import Technicals
import Constants

projectPath = Constants.ProjectPath


class BullishInsideBar(Scan):
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

            close1 = technicals.Close(candleSize, 1);
            open1 = technicals.Open(candleSize, 1)
            low1 = technicals.Low(candleSize, 1)
            high1 = technicals.High(candleSize, 1)

            if (high0 - low0) <= 0.75*(high1 - low1) and abs(open0 - close0) < abs(open1 - close1) and high0 < high1 \
                    and low0 > low1 and open0 < close0 and open1 > close1 and close0 <  open1 and open0 > close1:
                return True
        return False

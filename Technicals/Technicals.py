import os.path
import start
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL
import Constants

projectPath = Constants.ProjectPath


class Technicals:
    symbol = None
    timeSeries = None

    def __init__(self, symbol, timeSeries=None, apiProvider=None):
        self.symbol = symbol
        self.timeSeries = timeSeries
        self.apiProvider = None

    def setTimeSeries(self, candleSize):
        if os.path.exists(projectPath + "resources/" + self.symbol + "/" + candleSize):
            self.timeSeries = pd.read_json(projectPath +
                                           "resources/" + self.symbol + "/" + candleSize + "/" + self.symbol + ".json",
                                           convert_dates=True)
        else:
            self.timeSeries = start.getSeries(self.apiProvider, self.symbol, candleSize)

    def Close(self, candleSize, offset=0):
        if self.timeSeries is None:
            self.setTimeSeries(candleSize)

        if candleSize == "DAILY":
            return self.timeSeries['Close'].tail(offset + 1).iloc[0]
        return

    def Open(self, candleSize, offset=0):
        if self.timeSeries is None:
            self.setTimeSeries(candleSize)

        if candleSize == "DAILY":
            return self.timeSeries['Open'].tail(offset + 1).iloc[0]
        return

    def High(self, candleSize, offset=0):
        if self.timeSeries is None:
            self.setTimeSeries(candleSize)

        if candleSize == "DAILY":
            return self.timeSeries['High'].tail(offset + 1).iloc[0]
        return

    def Low(self, candleSize, offset=0):
        if self.timeSeries is None:
            self.setTimeSeries(candleSize)

        if candleSize == "DAILY":
            return self.timeSeries['Low'].tail(offset + 1).iloc[0]
        return

    def Volume(self, candleSize, offset=0):
        if self.timeSeries is None:
            self.setTimeSeries(candleSize)

        if candleSize == "DAILY":
            return self.timeSeries['Volume'].tail(offset + 1).iloc[0]
        return

    def SMA(self, window, type, candleSize, offset=0):
        if self.timeSeries is None:
            self.setTimeSeries(candleSize)

        interval = window + offset

        trimmedSeries = self.timeSeries.tail(interval).copy()

        trimmedSeries['SMA' + type] = trimmedSeries[type].rolling(window=window).mean()

        return trimmedSeries['SMA' + type].iloc[window - 1]

    def EMA(self, window, type, candleSize, offset=0):
        if self.timeSeries is None:
            self.setTimeSeries(candleSize)

        interval = window + offset

        trimmedSeries = self.timeSeries.tail(interval).copy()
        trimmedSeries['EMA' + type] = trimmedSeries['Close'].ewm(span=window, adjust=False).mean()

        return trimmedSeries['EMA' + type].iloc[window - 1]

    def getChannelSupportAndResistances(self, window, candleSize):
        if self.timeSeries is None:
            self.setTimeSeries(candleSize)
        existingLevelsFilePath = projectPath + "/resources/" + self.symbol + "/" + candleSize + "/" + "channels.txt"
        if os.path.exists(existingLevelsFilePath):
            file = open(existingLevelsFilePath, 'r')
            for line in file:
                levels = line.strip().split(",")
                break
        else:
            res = STL(self.timeSeries['Close'], period=180).fit()
            seasonal = res.seasonal.to_numpy()
            trend = res.trend.to_numpy()

            pos = []
            neg = []
            for i in range(0, len(seasonal)):
                if seasonal[i] < 0:
                    neg.append(trend[i] + seasonal[i])
                else:
                    pos.append(trend[i] + seasonal[i])
            plt.plot(pos, 'g--', neg, 'r--')
            plt.show()
            print()

    def gapUpOpening(self, candleSize="DAILY"):
        if self.timeSeries is None:
            self.setTimeSeries(candleSize)

        if self.Open(candleSize) > self.Close(candleSize, 1):
            return True
        return False

import start
from Technicals import SMA
from Technicals import EMA
import numpy as np
from Strategy.Strategy import Strategy


class MACrossOver(Strategy):

    params = {}

    def __init__(self, params):
        self.params = params

    def runBackTest(self, apiProvider, symbol, initialCap=100000):

        if "candleSize" in self.params.keys():
            candleSize = self.params['candleSize']
        else:
            print("candle size not provided")
            raise
            return

        if "windows" in self.params.keys():
            windows = self.params['windows']
        else:
            print("window size not provided")
            raise
            return
        if 'maType' in self.params.keys():
            maType = self.params['maType']
        else:
            maType = 'SMA'

        initialCapCopy = initialCap
        timeseries = start.getSeries(apiProvider, symbol, candleSize)

        if timeseries is not None:
            # print("init cap " + str(initialCap))

            if maType == "SMA":
                data0 = SMA.getSMA(symbol, windows[0], candleSize)
                timeseries = SMA.getSMA(symbol, windows[1], candleSize, timeSeries=data0)
            elif maType == 'EMA':
                data0 = EMA.getEMA(symbol, windows[0], candleSize)
                timeseries = SMA.getEMA(symbol, windows[1], candleSize, timeSeries=data0)

            timeseries['Signal'] = timeseries[maType + str(windows[0])] - timeseries[maType + str(windows[1])]
            timeseries['Position'] = (timeseries['Signal'].apply(np.sign) + 1) / 2
            # print(timeseries.to_string())
            entered = 0
            stocksPurchased = 0
            entryPrice = 0
            for index, row in timeseries.iterrows():
                spotPrice = row['Close']
                if entered == 0 and row['Position'] > 0:
                    entered = 1
                    entryPrice = spotPrice
                    stocksPurchased = int(initialCap / entryPrice)
                    initialCap = initialCap - stocksPurchased * entryPrice

                if entered and (row['Position'] <= 0 or spotPrice < 0.95 * entryPrice):
                    initialCap = initialCap + stocksPurchased * spotPrice
                    entered = 0
                    stocksPurchased = 0
                    exitPrice = spotPrice
            if entered:
                initialCap += stocksPurchased * spotPrice
            # print(initialCap-initialCapCopy)

            return ((initialCap - initialCapCopy) / initialCapCopy) * 100

    def deployStrategy(self, apiProvider, symbolList : list):
        pass

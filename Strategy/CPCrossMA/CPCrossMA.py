import start
from Technicals import SMA
from Technicals import EMA
import numpy as np
from Strategy.Strategy import Strategy


class CPCrossMA(Strategy):
    params = {}

    def __init__(self, params):
        self.params = params

    def runStrategy(self, apiProvider, symbol, initialCap=100000):

        if "candleSize" in self.params.keys():
            candleSize = self.params['candleSize']
        else:
            print("candle size not provided")
            raise
            return
        if 'window' in self.params.keys():
            window = self.params['window']
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
            if maType == "SMA":
                data = SMA.getSMA(symbol, window, candleSize)
            elif maType == 'EMA':
                data = EMA.getEMA(symbol, window, candleSize)
            data['Signal'] = data['Close'] - data[maType+str(window)]
            data['Position'] = (data['Signal'].apply(np.sign) + 1) / 2
            entered = 0
            stocksPurchased = 0
            entryPrice = 0
            for index, row in data.iterrows():
                spotPrice = row['Close']
                if entered == 0 and row['Position'] > 0:
                    entered = 1
                    entryPrice = spotPrice
                    stocksPurchased = int(initialCap / entryPrice)
                    initialCap = initialCap - stocksPurchased * entryPrice

                if entered and (row['Position'] <= 0 or spotPrice < 0.95 * entryPrice):
                    initialCap = initialCap + stocksPurchased * spotPrice
                    entered = 0
            if entered:
                initialCap += stocksPurchased * spotPrice

            return ((initialCap - initialCapCopy) / initialCap) * 100


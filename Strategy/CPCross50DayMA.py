from Strategy.Strategy import Strategy
from Strategy.CPCrossMA.CPCrossMA import CPCrossMA


class CPCross50DayMA(Strategy):
    params = {}

    def __init__(self):
        self.params = {"candleSize": "DAILY", "window": 50, "maType": "SMA"}

    def runBackTest(self, apiProvider, symbol, initialCap=100000):
        strategy = CPCrossMA(self.params)
        return strategy.runBackTest(apiProvider, symbol)


# def priceGreaterThanSMAWithHighVolumes(symbol, candleSize, smaCPWindow=50, smaVolumeWindow=20):
#     hit = []
#     apiProvider = ApiProvider()
#     timeseries = start.getSeries(apiProvider, symbol, candleSize)
#     if timeseries is not None:
#         indicator = Indicators(symbol, timeseries)
#
#         smaCP = indicator.SMA(smaCPWindow, "Close", "DAILY")
#         closePrice = indicator.Close("DAILY")
#         smaVol = indicator.SMA(smaVolumeWindow, "Volume", "DAILY")
#         dayVolume = indicator.Volume("DAILY", 0)
#
#         if smaCP < closePrice and smaVol < dayVolume:
#             hit.append(symbol)
#             print(symbol)


# for symbol in symbols:
#     if symbol == "M&M":
#         continue
#     priceGreaterThanSMAWithHighVolumes(symbol, "DAILY")
#     print(i)
#     i += 1

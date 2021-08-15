from Strategy.Strategy import Strategy
class ResistanceBreakWithHighVolumes(Strategy):

    def __init__(self):
        pass

    def runStrategy(self, apiProvider, symbol, initialCap=100000):
        return
    # yet to be written
    # hit = []
    # apiProvider = ApiProvider()
    # timeseries = start.getSeries(apiProvider, symbol, candleSize)
    # if timeseries is not None:
    #     indicator = Indicators(symbol, timeseries)
    #
    #     closePrice = indicator.Close("DAILY")
    #     smaVol = indicator.SMA(20, "Volume", "DAILY")
    #     dayVolume = indicator.Volume("DAILY", 0)
    #
    #     if resistanceLevel < closePrice and smaVol < dayVolume:
    #         hit.append(symbol)
    #         print(symbol)
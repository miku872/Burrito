from Utils.Symbols import getNifty50List
import start
from Technicals.Technicals import Technicals
from ApiProviders.AngelSmartApi.ClassResolver.ApiProvider import ApiProvider

nifty50 = getNifty50List()
i=1;

hit = []
failedList=[]


def resistanceBreakWithHighVolumes(symbol, candleSize, resistanceLevel):
    hit = []
    apiProvider = ApiProvider.getInstance()
    timeseries = start.getSeries(apiProvider, symbol, candleSize)
    if timeseries is not None:
        technicals = Technicals(symbol, timeseries)

        closePrice = technicals.Close("DAILY")
        smaVol = technicals.SMA(20, "Volume", "DAILY")
        dayVolume = technicals.Volume("DAILY", 0)

        if resistanceLevel < closePrice and smaVol < dayVolume:
            hit.append(symbol)
            print(symbol)

def priceGreaterThanSMAWithHighVolumes(symbol, candleSize, smaCPWindow=50, smaVolumeWindow=20):

    apiProvider = ApiProvider.getInstance()
    timeseries = start.getSeries(apiProvider, symbol, candleSize)
    if timeseries is not None:
        technicals = Technicals(symbol, timeseries)

        smaCP = technicals.SMA(smaCPWindow, "Close", "DAILY")
        closePrice = technicals.Close("DAILY")
        smaVol = technicals.SMA(smaVolumeWindow, "Volume", "DAILY")
        dayVolume = technicals.Volume("DAILY", 0)

        if smaCP < closePrice and smaVol < dayVolume:
            hit.append(symbol)
            print(symbol)

# for symbol in nifty50:
#     if symbol=="M&M":
#         continue
#     priceGreaterThanSMAWithHighVolumes(symbol,"DAILY")
#     print(i)
#     i+=1

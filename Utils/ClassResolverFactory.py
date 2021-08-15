from pydoc import locate

strategyMap = {"CPCross50DayMA" : "Strategy.CPCross50DayMA.CPCross50DayMA",
               "20DayMACrossOver50DayMA" : "Strategy.Day20MACrossOverDay50MA.Day20MACrossOverDay50MA"}
apiProviderMap = {"AngelSmartApi": "ApiProviders.AngelSmartApi.ClassResolver.ApiProvider.ApiProvider",
                  "AlphaVantage" : "ApiProviders.AlphaVantage.ClassResolver.ApiProvider.ApiProvider"}
scannersMap = {"Hammer": "Scans.CandlePatterns.Hammer.Hammer", "ReverseHammer": "Scans.CandlePatterns.ReverseHammer.ReverseHammer",
               "GapUpOpening": "Scans.CandlePatterns.GapUpOpening.GapUpOpening",
               "BullishInsideBar": "Scans.CandlePatterns.BullishInsideBar.BullishInsideBar",
               "BullishEngulfing": "Scans.CandlePatterns.BullishEngulfing.BullishEngulfing",
               "20DaySMACross50DaySMAFromBelow": "Scans.MACrossOver.Day20SMACrossDay50SMAFromBelow.Day20SMACrossDay50SMAFromBelow",
               "100DaySMACross200DaySMAFromBelow": "Scans.MACrossOver.Day100SMACrossDay200SMAFromBelow.Day100SMACrossDay200SMAFromBelow",
               "50DaySMACross200DaySMAFromBelow" : "Scans.MACrossOver.Day50SMACrossDay200SMAFromBelow.Day50SMACrossDay200SMAFromBelow",
               "20DaySMACross50DaySMAFromAbove": "Scans.MACrossOver.Day20SMACrossDay50SMAFromAbove.Day20SMACrossDay50SMAFromAbove",
               "50DaySMACross100DaySMAFromAbove": "Scans.MACrossOver.Day50SMACrossDay100SMAFromAbove.Day50SMACrossDay100SMAFromAbove",
               "50DaySMACross200DaySMAFromAbove": "Scans.MACrossOver.Day50SMACrossDay200SMAFromAbove.Day50SMACrossDay200SMAFromAbove",
               "20DaySMACross200DaySMAFromAbove": "Scans.MACrossOver.Day20SMACrossDay200SMAFromAbove.Day20SMACrossDay200SMAFromAbove",

               }
def getClassObject(className):
    my_class = locate(strategyMap[className])
    return my_class()

def getApiProvider(className):
    my_class = locate(apiProviderMap[className])
    return my_class()

def getScanner(className):
    my_class = locate(scannersMap[className])
    return my_class()



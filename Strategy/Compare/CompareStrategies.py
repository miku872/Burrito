from BackTest.RunBackTest import RunBackTest
from Strategy.Day20MACrossOverDay50MA import Day20MACrossOverDay50MA
from Strategy.CPCross50DayMA import CPCross50DayMA
from ApiProviders.AngelSmartApi.ClassResolver.ApiProvider import ApiProvider

def CompareStrategies(strategies):


    compareDic = {}
    for stratagy in strategies:
        avgReturns = RunBackTest(stratagy)
        compareDic[type(stratagy).__name__] = avgReturns
    return compareDic

strategy = Day20MACrossOverDay50MA()
symbolList = ['DRREDDY','INFY']
strategy.deployStrategy(ApiProvider.getInstance(),symbolList)
# strategies = [Day20MACrossOverDay50MA(), CPCross50DayMA()]
# print(CompareStrategies(strategies))





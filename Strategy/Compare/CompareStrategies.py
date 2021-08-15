from BackTest.RunBackTest import RunBackTest
from Strategy.Day20MACrossOverDay50MA import Day20MACrossOverDay50MA
from Strategy.CPCross50DayMA import CPCross50DayMA


def CompareStrategies(strategies):


    compareDic = {}
    for stratagy in strategies:
        avgReturns = RunBackTest(stratagy)
        compareDic[type(stratagy).__name__] = avgReturns
    return compareDic


# strategies = [Day20MACrossOverDay50MA(), CPCross50DayMA()]
# print(CompareStrategies(strategies))





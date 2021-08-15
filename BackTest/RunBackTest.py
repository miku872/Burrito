from Utils.Symbols import getNifty50List

from ApiProviders.AngelSmartApi.ClassResolver.ApiProvider import ApiProvider


def RunBackTest(strategy):
    avgReturn = 0
    i = 0
    nifty50 = getNifty50List()
    apiProvider = ApiProvider()
    for symbol in nifty50:
        if symbol != "M&M":
            returns = strategy.runStrategy(symbol,  apiProvider)
            if returns is not None:
                avgReturn += returns
                i += 1
    if i > 0:
        print(str(avgReturn / i))
        return avgReturn / i


from Strategy.Strategy import Strategy
from Strategy.MACrossOver.MACrossOver import MACrossOver


class Day20MACrossOverDay50MA(Strategy):

    params = {}

    def __init__(self):
        self.params = {"candleSize": "DAILY", "windows": [20, 50], "maType": "SMA"}

    def runStrategy(self, apiProvider, symbol, initialCap=100000):
        strategy = MACrossOver(self.params)
        return strategy.runStrategy(apiProvider, symbol)
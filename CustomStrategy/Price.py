from CustomStrategy.Indicator import Indicator
from Technicals.Technicals import Technicals


class Price(Indicator):

    def __init__(self, properties):
        super().__init__(properties)
        self.validOperations = ["comparator", "operator"]
        self.name = "price"
        self.sign = "price"
        self.group = "indicatorsw"

    def getResult(self):
        if "symbol" in self.properties.keys():
            symbol = self.properties["symbol"]
        if "candlesize" in self.properties.keys():
            candle = self.properties["candlesize"]
        if "offset" in self.properties.keys():
            offset = self.properties["offset"]

        return Technicals(symbol).Close(candle,2)



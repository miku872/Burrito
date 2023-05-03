from Scans.MACrossOver.Day5SMACrossDay20SMAFromBelow import Day5SMACrossDay20SMAFromBelow
from Scans.MACrossOver.Day5SMACrossDaySMAFromAbove import Day5SMACrossDay20SMAFromAbove
from Strategy.Strategy import Strategy
from Strategy.MACrossOver.MACrossOver import MACrossOver
from pojo.AbstractOrder import AbstractOrder

class Day5MACrossOverDay20MA(Strategy):

    params = {}

    def __init__(self):
        self.params = {"candleSize": "DAILY", "windows": [5, 20], "maType": "SMA"}

    def runBackTest(self, apiProvider, symbol, initialCap=100000):
        strategy = MACrossOver(self.params)
        return strategy.runBackTest(apiProvider, symbol)

    def deployStrategy(self, apiProvider, symbolList : list):

        if "candleSize" in self.params.keys():
            candleSize = self.params['candleSize']
        else:
            print("candle size not provided")
            raise
            return

        if "windows" in self.params.keys():
            windows = self.params['windows']
        else:
            print("window size not provided")
            raise
            return
        if 'maType' in self.params.keys():
            maType = self.params['maType']
        else:
            maType = 'SMA'

        positions = apiProvider.getPositions()
        holdings = apiProvider.getHoldings()
        symbol_map = {}
        for position in positions.data:
            if symbol_map.get(position.symbolname):
                symbol_map[position.symbolname] += position.buyqty
            else:
                symbol_map[position.symbolname] = position.buyqty

        for holding in holdings.data:
            if symbol_map.get(holding.symbolname):
                symbol_map[holding.symbolname] += holding.quantity
            else:
                symbol_map[holding.symbolname] = holding.quantity

        for symbol in symbolList:
            buyScan = Day5SMACrossDay20SMAFromBelow()
            sellScan = Day5SMACrossDay20SMAFromAbove()
            if buyScan.isCriteriaMet(symbol, candleSize, apiProvider):
                if(symbol_map.get(symbol)):
                    continue
                else:
                    try:
                        print("buying  " + symbol)
                        ltp = apiProvider.get_ltp(symbol)
                        quantity = int(15000/ltp)
                        orderParams = {"variety" : "REGULAR", "order_type" : "MARKET", "transaction_type" : "BUY",
                                       "exchange" : "NSE", "quantity" : quantity, "validity" : "DAY", "duration" : "DAY",
                                       "symbol" : symbol, "product_type" : "DELIVERY"}

                        order = AbstractOrder(orderParams)
                        apiProvider.place_order(order)
                    except Exception as e:
                        raise e
            elif sellScan.isCriteriaMet(symbol, candleSize, apiProvider):
                if (symbol_map.get(symbol)):
                    #sell
                    try:
                        sellQuantity = 0
                        ltp = apiProvider.get_ltp(symbol)
                        for position in positions:
                            if position.data.symbolname == symbol:
                                sellQuantity = position.data.netqty
                                break

                        for holding in holdings:
                            if holding.data.symbolname == symbol:
                                sellQuantity = holding.data.quantity
                                break

                        quantity = sellQuantity
                        if quantity > 0:
                            print("selling  " + symbol)

                            orderParams = {"variety": "REGULAR", "order_type": "MARKET", "transaction_type": "SELL",
                                           "exchange": "NSE", "quantity": quantity, "duration": "DAY",
                                           "symbol": symbol, "product_type": "DELIVERY"}

                            order = AbstractOrder(orderParams)
                            apiProvider.place_order(order)
                    except Exception as e:
                        raise e
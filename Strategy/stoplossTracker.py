from Utils.ClassResolverFactory import getApiProvider, getStrategy
from flask import request
from pojo.AbstractOrder import AbstractOrder

def runStopLossTrackerUsingAPI(apiProvider):
    try:
        print("running stoploss tracker")
        positions = apiProvider.getPositions()
        holdings = apiProvider.getHoldings()
        symbol_map = {}

        for holding in holdings.data:
                symbol_map[holding.symbolname] = [holding.quantity, holding.averageprice, holding.ltp]
        for position in positions.data:
            if symbol_map.get(position.symbolname):
                continue
            else:
                symbol_map[position.symbolname] = [position.netqty, position.buyavgprice, position.ltp]

        for symbol in symbol_map.keys():
            avgBuyPrice = symbol_map[symbol][1]
            ltp = symbol_map[symbol][2]
            print(symbol_map[symbol])
            if ltp < avgBuyPrice and float(avgBuyPrice-ltp)/float(avgBuyPrice) > 0.05:
                orderParams = {"variety": "REGULAR", "order_type": "MARKET", "transaction_type": "SELL",
                   "exchange": "NSE", "quantity": symbol_map[symbol][0], "duration": "DAY",
                   "symbol": symbol, "product_type": "DELIVERY"}

                order = AbstractOrder(orderParams)
                apiProvider.place_order(order)
    except Exception as e:
        print(e)









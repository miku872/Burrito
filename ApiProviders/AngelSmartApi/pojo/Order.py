from pojo.AbstractOrder import AbstractOrder
import ApiProviders.AngelSmartApi.ClassResolver.ApiProvider as ApiProvider

class Order(AbstractOrder):
    def __init__(self, order : AbstractOrder):
        self.order = order

    def getOrder(self):
        angelOrder = {}
        params = self.order.params
        angelOrder["quantity"] = params.get("quantity")
        angelOrder["duration"] = params.get("validity")
        symbol = params.get("symbol")
        symbol_to_trading_symbol_map = ApiProvider.getSymbolToTradingSymbol()
        symbol_to_trading_token_map = ApiProvider.getSymbolToTokenMap()
        angelOrder["tradingsymbol"] = symbol_to_trading_symbol_map.get(symbol)
        angelOrder["symboltoken"] = symbol_to_trading_token_map.get(symbol)
        angelOrder["producttype"] = params.get("product_type")
        if params.get("variety").upper() == "REGULAR":
            angelOrder["variety"] = "NORMAL"
        if (params.get("order_type").upper() == "LIMIT"):
            angelOrder["ordertype"] = "LIMIT"
            angelOrder["price"] = params.get("price")
        elif (params.get("order_type").upper() == "MARKET"):
            angelOrder["ordertype"] = "MARKET"
        if(params.get("transaction_type").upper() == "BUY"):
            angelOrder["transactiontype"] = "BUY"
        else:
            angelOrder["transaction_type"] = "SELL"
        if params.get("exchange") is not None:
            angelOrder["exchange"] = params.get("exchange").upper()


        elif params.get("variety").upper() == "AMO":
            pass
        elif params.get("variety").upper() == "BRACKET":
            pass

        return angelOrder


import ApiProviders.AngelSmartApi.ClassResolver.ApiProvider as ApiProvider
class Data(object):
    def __init__(self, data):
        self.tradingSymbol = data.get("tradingsymbol")
        self.exchange = data.get("exchange")
        self.isin = data.get("isin")
        self.t1quantity = data.get("t1quantity")
        self.realisedquantity = data.get("realisedquantity")
        self.quantity = int(data.get("quantity"))
        self.authorisedquantity = data.get("authorisedquantity")
        self.profitandloss = data.get("profitandloss")
        self.product = data.get("product")
        self.collateralquantity = data.get("collateralquantity")
        self.collateraltype = data.get("collateraltype")
        self.haircut = data.get("haircut")
        self.averageprice = data.get("averageprice")
        self.ltp = data.get("ltp")
        self.symboltoken = data.get("symboltoken")
        self.close = data.get("close")
        self.symbolname = ApiProvider.getTradingSymbolToSymbol().get(self.tradingSymbol)



class Holding:
    def __init__(self, json_data):
        self.status = json_data.get("status");
        self.message = json_data.get("message");
        self.errorcode = json_data.get("errorcode");
        self.data = []
        if json_data.get('data'):
            for holding in json_data.get('data'):
                self.data.append(Data(holding));

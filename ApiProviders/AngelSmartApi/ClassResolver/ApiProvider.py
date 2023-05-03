from ApiProviders.AbstractApiProvider import AbstractApiProvier
from ApiProviders.AngelSmartApi.ResponseParser.Parser import Parser
from smartapi.smartConnect import SmartConnect
import datetime
import os.path
import pandas as pd
import Constants
from ApiProviders.AngelSmartApi.pojo.Position import Position
from ApiProviders.AngelSmartApi.pojo.Holding import Holding
import pyotp
import threading

from ApiProviders.AngelSmartApi.pojo.Order import Order

projectPath = Constants.ProjectPath
intervalMap = {"DAILY": "ONE_DAY", "ONE_MINUTE": "ONE_MINUTE",
               "THREE_MINUTE": "THREE_MINUTE", "FIVE_MINUTE": "FIVE_MINUTE", "TEN_MINUTE": "TEN_MINUTE",
               "FIFTEEN_MINUTE": "FIFTEEN_MINUTE", "THIRTY_MINUTE": "THIRTY_MINUTE", "ONE_HOUR": "ONE_HOUR"}


def getSymbolToTokenMap():
    file = open(projectPath + "ApiProviders/AngelSmartApi/Resources/NiftySymbols.csv", 'r')
    symbolToTokenMap = {}
    for row in file:
        rowData = row.strip().split(",")
        symbolToTokenMap[rowData[0]] = rowData[1]
    return symbolToTokenMap


def getSymbolToTradingSymbol():
    file = open(projectPath + "ApiProviders/AngelSmartApi/Resources/NiftySymbols.csv", 'r')
    symbolToTradingSymbol = {}
    for row in file:
        rowData = row.strip().split(",")
        symbolToTradingSymbol[rowData[0]] = rowData[2]
    return symbolToTradingSymbol

def getTokenToSymbol():
    file = open(projectPath + "ApiProviders/AngelSmartApi/Resources/NiftySymbols.csv", 'r')
    tokenToSymbol = {}
    for row in file:
        rowData = row.strip().split(",")
        tokenToSymbol[rowData[1]] = rowData[0]
    return tokenToSymbol

def getTradingSymbolToSymbol():
    file = open(projectPath + "ApiProviders/AngelSmartApi/Resources/NiftySymbols.csv", 'r')
    tradingSymbolToSymbol = {}
    for row in file:
        rowData = row.strip().split(",")
        tradingSymbolToSymbol[rowData[2]] = rowData[0]
    return tradingSymbolToSymbol


class ApiProvider(AbstractApiProvier):
    functions = {}
    refreshToken = ""
    feedToken = ""
    obj = ""
    userProfile = ""
    __instance = None

    @staticmethod
    def getInstance():
        if ApiProvider.__instance == None:
            ApiProvider.__instance = ApiProvider()
        return ApiProvider.__instance

    def __init__(self):
        # create object of call
        self.functions["DAILY"] = "TIME_SERIES_DAILY"
        self.session = None
        apiParams = self.getApiParams()
        apiKey = apiParams['apiKey']
        clientCode = apiParams['clientCode']
        password = apiParams['password']
        totp = pyotp.TOTP(apiParams['totp']).now()
        self.lock = threading.Lock()
        self.buylock = threading.Lock()
        self.selllock = threading.Lock()


        self.obj = SmartConnect(api_key=apiKey,
                                # optional
                                # access_token = "your access token",
                                # refresh_token = "your refresh_token"
                                )
        if self.session is None:
            self.session = self.obj.generateSession(clientCode, password, totp)
        #
        # self.timeSeriesColumn["DAILY"] = 'Time Series (Daily)'

    def getResponseParser(self, interval):
        return Parser(intervalMap[interval])

    def getApiParams(self):

        params = {}
        with open(projectPath + 'ApiProviders/AngelSmartApi/Resources/ApiConfig', 'r') as file:
            for line in file:
                param = line.strip().split("=")
                params[param[0]] = param[1]
        file.close()
        return params

    def getRefreshStamp(self, response):
        return response['data'][-1][0]

    def getResponse(self, symbol, function, start=None, end=None):
        try:
            # login api call
            if self.session is None:
                self.session = self.obj.generateSession(clientCode, password, totp)
            self.refreshToken = self.session['data']['refreshToken']

            # fetch the feedtoken
            self.feedToken = self.obj.getfeedToken()

            # fetch User Profile
            self.userProfile = self.obj.getProfile(self.refreshToken)

            symbolToTokenMap = getSymbolToTokenMap()

            if start is not None:
                if function == "DAILY":
                    start = start + " 09:16"

            if end is None:
                today = str(datetime.date.today())
                end = today + " 09:16"
            else:
                end = str(end) + " 09:16"
            historicParam = {
                "exchange": "NSE",
                "symboltoken": symbolToTokenMap[symbol],
                "interval": intervalMap[function],
                "fromdate": start,
                "todate": end
            }
            response = self.obj.getCandleData(historicParam)
            if response['status'] == True and response['message'] == "SUCCESS":
                if (response['data'] and len(response['data']) > 0):
                    return response
            else:
                # raise Exception(message= "Couldn't get requested data for " + symbol + "from api provider")
                print(response['message'])
            return None
        except Exception as e:
            print(e)
            raise e

    def getCDCWatermark(self, symbol, interval):
        if intervalMap[interval] == "ONE_DAY":
            limit = 2000
            suffix = ""
            if os.path.exists(projectPath + "resources/" + symbol + "/" + interval):
                localMetaData = pd.read_json(projectPath + "resources/" + symbol + "/" + interval + "/" + "MetaData.json",
                                             convert_dates=True)
                waterMark = localMetaData['Last Refreshed'][0]
                return waterMark
        if intervalMap[interval] == "ONE_MINUTE":
            limit = 30
            suffix = " 09:15"

        elif intervalMap[interval] == "THREE_MINUTE":
            limit = 90
            suffix = " 09:15"

        elif intervalMap[interval] == "FIVE_MINUTE":
            limit = 90
            suffix = " 09:15"

        elif intervalMap[interval] == "TEN_MINUTE":
            limit = 90
            suffix = " 09:15"

        elif intervalMap[interval] == "FIFTEEN_MINUTE":
            limit = 180
            suffix = " 09:15"

        elif intervalMap[interval] == "THIRTY_MINUTE":
            limit = 180
            suffix = " 09:15"

        elif intervalMap[interval] == "ONE_HOUR":
            limit = 365
            suffix = " 09:15"
        days_before = (datetime.date.today() - datetime.timedelta(days=limit)).isoformat()
        waterMark = str(days_before) + suffix
        return waterMark

    def getPositions(self):
        try:
            self.lock.acquire()
            # code to be executed in a synchronized manner
            # ...
            positionResponse = self.obj._getRequest("api.position")
            position = Position(positionResponse)
            return position
        except Exception as e:
            print(e)
        finally:
            self.lock.release()

    def getHoldings(self):
        try:
            self.lock.acquire()
            # code to be executed in a synchronized manner
            # ...
            holdingResponse= self.obj._getRequest("api.holding")
            holding = Holding(holdingResponse)
            return holding

        except Exception as e:
            print(e)
        finally:
            self.lock.release()

    def place_order(self, order : Order):
        try:
            order = Order(order)
            angelOrder = order.getOrder()
            if angelOrder.get("transactiontype")=="SELL":
                try :
                    self.selllock.acquire()
                    stockInHold = False
                    holdings = self.getHoldings()
                    for holding in holdings.data:
                        if holding.symbolname == angelOrder["tradingsymbol"]:
                            stockInHold = True
                            break
                    if stockInHold == False:
                        positions = self.getPositions()
                        for position in positions.data:
                            if position.symbolname == angelOrder["tradingsymbol"]:
                                stockInHold = True
                                break
                    if stockInHold:
                        orderId = self.obj.placeOrder(angelOrder)
                except Exception as e:
                    print(e)
                finally:
                    self.selllock.release()
            else:
                try :
                    self.buylock.acquire()
                    stockInHold = False
                    availableFundsResponse = self.obj.rmsLimit()
                    availableFunds = 0.0
                    if availableFundsResponse and availableFundsResponse['status']==True:
                        if availableFundsResponse.get('data') and availableFundsResponse['data'].get('net'):
                            availableFunds = float(availableFundsResponse['data']['net'])
                    if availableFunds > 10000:
                        holdings = self.getHoldings()
                        for holding in holdings.data:
                            if holding.symbolname==angelOrder["tradingsymbol"]:
                                stockInHold = True
                                break
                        if stockInHold == False:
                            positions = self.getPositions()
                            for position in positions.data:
                                if position.symbolname == angelOrder["tradingsymbol"]:
                                    stockInHold = True
                                    break
                        if stockInHold==False:
                            orderId = self.obj.placeOrder(angelOrder)
                            print("The order id is: {}".format(orderId))

                except Exception as e:
                    print(e)
                finally:
                    self.buylock.release()
        except Exception as e:
            print("Order placement failed: {}".format(e.message))

    def get_ltp(self, symbol, exchange="NSE"):
        token_map = getSymbolToTokenMap()
        trading_symbol_map = getSymbolToTradingSymbol()
        symboltoken = token_map.get(symbol)
        tradingsymbol = trading_symbol_map.get(symbol)

        response = self.obj.ltpData(exchange,tradingsymbol,symboltoken)
        if response['status'] == True and response['message'] == "SUCCESS":
            return response['data']['ltp']
        else:
            raise
# apiprovider = ApiProvider.getInstance()
# try:
#     logout=obj.terminateSession('Your Client Id')
#     print("Logout Successfull")
# except Exception as e:
#     print("Logout failed: {}".format(e.message))

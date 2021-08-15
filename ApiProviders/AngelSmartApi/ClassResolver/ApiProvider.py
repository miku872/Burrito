from ApiProviders.AbstractApiProvider import AbstractApiProvier
from ApiProviders.AngelSmartApi.ResponseParser.Parser import Parser
from smartapi.smartConnect import SmartConnect
import datetime
import os.path
import pandas as pd
import Constants

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


class ApiProvider(AbstractApiProvier):
    functions = {}
    refreshToken = ""
    feedToken = ""
    obj = ""
    userProfile = ""

    def __init__(self):
        # create object of call
        self.functions["DAILY"] = "TIME_SERIES_DAILY"
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
            apiParams = self.getApiParams()
            apiKey = apiParams['apiKey']
            clientCode = apiParams['clientCode']
            password = apiParams['password']

            self.obj = SmartConnect(api_key=apiKey,
                                    # optional
                                    # access_token = "your access token",
                                    # refresh_token = "your refresh_token"
                                    )

            # login Api call

            data = self.obj.generateSession(clientCode, password)
            self.refreshToken = data['data']['refreshToken']

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
                historicParam = {
                    "exchange": "NSE",
                    "symboltoken": symbolToTokenMap[symbol],
                    "interval": intervalMap[function],
                    "fromdate": start,
                    "todate": end
                }
                response = self.obj.getCandleData(historicParam)
                if response['status'] == True and response['message'] == "SUCCESS" and len(response['data']) > 0:

                    return response
                else:
                    raise Exception(message= "Couldn't get requested data for " + symbol + "from api provider")
                    print(response['message'])
                return None
        except Exception as e:
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

# try:
#     logout=obj.terminateSession('Your Client Id')
#     print("Logout Successfull")
# except Exception as e:
#     print("Logout failed: {}".format(e.message))

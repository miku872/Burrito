from ApiProviders.AbstractApiProvider import AbstractApiProvier
from ApiProviders.AlphaVantage.ResponseParser.Parser import Parser
import os.path
import pandas as pd
import requests
import os
import Constants

projectPath = Constants.ProjectPath


class ApiProvider(AbstractApiProvier):
    functions = {}
    timeSeriesColumn = {}

    def __init__(self):
        self.functions["DAILY"] = "TIME_SERIES_DAILY"
        self.functions["DAILY_ADJUSTED"] = "TIME_SERIES_DAILY_ADJUSTED"
        # self.functions["WEEKLY", '')
        # self.functions["WEEKLY_ADJUSTED", "")
        # self.functions["MONTHLY", '')
        # self.functions["MONTHLY_ADJUSTED", "")

        self.timeSeriesColumn["DAILY"] = 'Time Series (Daily)'
        self.timeSeriesColumn["DAILY_ADJUSTED"] = 'Time Series (Daily)'
        # self.timeSeriesColumn["WEEKLY", '')
        # self.timeSeriesColumn["WEEKLY_ADJUSTED", "")
        # self.timeSeriesColumn["MONTHLY", '')
        # self.timeSeriesColumn["MONTHLY_ADJUSTED", "")

    def getUri(self, apiKey, symbol, function, start=None, end=None):
        if start is None:
            return "https://www.alphavantage.co/query?function=" + function + "&symbol=BSE:" + symbol + "&outputsize=full&apikey=" + apiKey
        else:
            return "https://www.alphavantage.co/query?function=" + function + "&symbol=BSE:" + symbol + "&outputsize=compact&apikey=" + apiKey

    def getResponseParser(self, interval):
        return Parser(interval)

    def getApiParams(self):
        params = {}
        with open(projectPath + 'ApiProviders/AlphaVantage/Resources/ApiConfig', 'r') as file:
            for line in file:
                param = line.strip().split("=")
                params[param[0]] = param[1]
        file.close()
        return params

    def getRefreshStamp(self, response):
        return response['Meta Data']['3. Last Refreshed']

    def getResponse(self, symbol, function, start=None, end=None):
        apiParams = self.getApiKey();
        apiKey = apiParams['apiKey'];
        url = self.getUri(apiKey, symbol, self.functions[function], start=start)
        try:
            response = requests.get(url)
            data = response.json()
            return data
        except:
            print("error accessing the api")
            raise

    def getCDCWatermark(self, symbol, interval):
        waterMark = None
        if os.path.exists(projectPath + "resources/" + symbol + "/" + interval):
            localMetaData = pd.read_json(projectPath + "resources/" + symbol + "/" + interval + "/" + "MetaData.json",
                                         convert_dates=True)
            waterMark = localMetaData['Last Refreshed'][0]
        return waterMark

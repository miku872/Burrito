from abc import ABC, abstractmethod

class AbstractApiProvier:
    def __init__(self):
        return

    @abstractmethod
    def getResponse(self, symbol, function, start=None, end=None):
        pass

    @abstractmethod
    def getResponseParser(self, interval):
        pass

    @abstractmethod
    def getApiParams(self):
        pass

    @abstractmethod
    def getRefreshStamp(self, response):
        pass

    @abstractmethod
    def getCDCWatermark(self, symbol, interval):
        pass


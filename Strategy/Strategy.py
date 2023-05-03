from abc import ABC, abstractmethod

class Strategy:
    def __init__(self):
        pass

    @abstractmethod
    def runBackTest(self, apiProvider, symbol, initialCap=100000):
        pass

    @abstractmethod
    def deployStrategy(self, apiProvider, symbolList : list):
        pass


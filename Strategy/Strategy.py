from abc import ABC, abstractmethod

class Strategy:
    def __init__(self):
        pass

    @abstractmethod
    def runStrategy(self, apiProvider, symbol, initialCap=100000):
        pass
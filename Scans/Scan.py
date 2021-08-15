from abc import ABC, abstractmethod

class Scan:
    def __init__(self):
        return

    @abstractmethod
    def isCriteriaMet(self, symbol, candleSize="DAILY", apiProvider=None, timeSeries=None, interval=None):
        pass

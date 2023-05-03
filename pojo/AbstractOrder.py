from abc import ABC, abstractmethod


class AbstractOrder:
    def __init__(self, params):
        self.params = params

    @abstractmethod
    def getOrder(self):
        pass


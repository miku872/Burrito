from CustomStrategy.StrategyElement import StrategyElement


class Operator(StrategyElement):
    def __init__(self, properties):
        super().__init__(properties)
        self.group = "operator"

    def getResult(self):
        pass
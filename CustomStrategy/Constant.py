from CustomStrategy.Indicator import Indicator


class Constant(Indicator):

    def __init__(self, properties):
        super().__init__(properties)
        self.validOperations = ["comparator", "operator"]
        self.name = "constant"
        self.sign = "constant"
        self.group = "constant"

    def getResult(self):
        return self.properties["value"]



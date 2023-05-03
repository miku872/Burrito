from CustomStrategy.Operator import Operator


class Equals(Operator):
    def __init__(self, properties):
        super().__init__(properties)
        self.name = "equals"
        self.sign = "="

    def getResult(self):
        if len(self.properties)==2:
            return self.properties["left"] == self.properties["right"]

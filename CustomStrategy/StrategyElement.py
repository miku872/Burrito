class StrategyElement:
    name = None
    group = None
    sign = None
    validOperations = []
    properties = dict()

    def __init__(self, properties):
        self.name = None
        self.group = None
        self.sign = None
        self.validOperations = []
        self.properties = properties

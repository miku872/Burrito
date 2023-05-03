from CustomStrategy.Price import Price
from CustomStrategy.Sum import Sum
from CustomStrategy.Equals import Equals
from CustomStrategy.Constant import Constant

if __name__=="__main__":
    print(
        Equals({ "left" :
            Sum({
                "left" : Price({"symbol" : "ADANIPORTS", "candlesize" : "DAILY", "offset" : 2}).getResult(),
                "right" : Constant({"value" : 10}).getResult()
            }).getResult(),

            "right" : 703
        }).getResult()
    )
from flask import request, jsonify, Response
from Utils.ClassResolverFactory import getStrategy
from Utils.ClassResolverFactory import getApiProvider

from api.BackTest import runBackTest
from Utils.Symbols import getNifty50List


def compare():
    try:
        if 'strategies' in request.args:
            strategies = request.args['strategies'].strip().split(",")
        else:
            raise
        if 'instruments' in request.args and len(request.args['instruments']) > 0:
            symbols = request.args['instruments'].strip().split(",")
        else:
            symbols = getNifty50List()

        if 'apiProvider' in request.args:
            apiProviderName = request.args['apiProvider']
            apiProvider = getApiProvider(apiProviderName)


        response = {"result": []}

        for strategyName in strategies:
            returns = 0
            i = 0
            strategy = getStrategy(strategyName)
            for symbol in symbols:
                print(symbol)
                returnsForSymbol = runBackTest(strategy, symbol, apiProvider)
                if returnsForSymbol is not None:
                    returns += returnsForSymbol
                    i += 1
            if i > 0:
                returns = round(returns / i, 2)
                response["result"].append({"name": strategyName, "OverallReturns": returns, "AnnualizedReturns": 12})
            else:
                response[strategyName] = "error while running " + strategyName + " backtest"

        return jsonify(response)

    except Exception as e:
        Response("{'message':" + e + "'}", status=500, mimetype='application/json')

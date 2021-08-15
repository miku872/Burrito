from flask import request, jsonify, Response
from Utils.ClassResolverFactory import getClassObject
from Utils.ClassResolverFactory import getApiProvider

from Api.BackTest import RunBackTest
from Utils.Symbols import getNifty50List


def compare():
    try:
        if 'strategies' in request.args:
            strategies = request.args['strategies'].strip().split(",")
        else:
            raise
        if 'instruments' in request.args:
            symbols = request.args['instruments'].strip().split(",")

        if 'apiProvider' in request.args:
            apiProviderName = request.args['apiProvider']
            apiProvider = getApiProvider(apiProviderName)

        else:
            symbols = getNifty50List()
        response = {"result": []}

        for strategyName in strategies:
            returns = 0
            i = 0
            strategy = getClassObject(strategyName)
            for symbol in symbols:
                returnsForSymbol = RunBackTest(strategy, symbol, apiProvider)
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

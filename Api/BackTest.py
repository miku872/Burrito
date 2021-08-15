from flask import request, jsonify, Response
from Utils.ClassResolverFactory import getClassObject
from Utils.ClassResolverFactory import getApiProvider


def run():
    try:
        symbol = None
        if 'instrument' in request.args:
            symbol = request.args['instrument']
        if 'strategy' in request.args:
            strategyName = request.args['strategy']
        if 'apiProvider' in request.args:
            apiProviderName = request.args['apiProvider']
            apiProvider = getApiProvider(apiProviderName)
        strategy = getClassObject(strategyName)

        returns = RunBackTest(strategy, symbol, apiProvider)
        if returns is not None:
            response = jsonify({"returns": round(returns, 2)})
        else:
            response = jsonify({"returns": "there was an error while running backtest"})
        return response
    except Exception as e:
        Response("{'message':"+e+"'}", status=500, mimetype='application/json')


def RunBackTest(strategy, symbol, apiProvider):
    returns = strategy.runStrategy(apiProvider, symbol)
    return returns

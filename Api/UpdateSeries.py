from Utils.Symbols import getNifty50List
import start
from Utils.ClassResolverFactory import getApiProvider
from flask import request, jsonify
from flask import Response


def update():
    try:
        if 'apiProvider' in request.args:
            apiProviderName = request.args['apiProvider']
            apiProvider = getApiProvider(apiProviderName)
        else:
            return Response("{'message':'apiProvider not given'}", status=400, mimetype='application/json')
        candleSize = ["DAILY"]
        nifty50 = getNifty50List()
        for candle in candleSize:
            for symbol in nifty50:
                if symbol=="M&M":
                    continue
                print(candle, symbol)
                start.getSeries(apiProvider, symbol, candle)
        response = jsonify({"response": 200})
        return response
    except Exception as e:
        Response("{'message':'failed to update'}", status=500, mimetype='application/json')


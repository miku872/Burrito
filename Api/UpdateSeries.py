from Utils.Symbols import getNifty500List
from Utils.Symbols import getNifty50List
import start
from Utils.ClassResolverFactory import getApiProvider
from flask import request, jsonify
from flask import Response

def updateManual(apiProvider):
    try:
        if apiProvider:
            apiProviderName = apiProvider
            apiProvider = getApiProvider(apiProviderName)
        else:
            return Response("{'message':'apiProvider not given'}", status=400, mimetype='application/json')
        candleSize = ["DAILY"]
        nifty50 = getNifty50List()
        for candle in candleSize:
            for symbol in nifty50:
                if symbol=="M&M" or symbol=="ADANIGREEN":
                    continue
                start.getSeries(apiProvider, symbol, candle)
        response = jsonify({"response": 200})
        return response
    except Exception as e:
        Response("{'message':'failed to update'}", status=500, mimetype='application/json')
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
                if symbol=="M&M" or symbol=="ADANIGREEN":
                    continue
                start.getSeries(apiProvider, symbol, candle)
        response = jsonify({"response": 200})
        return response
    except Exception as e:
        print(e)
        Response("{'message':'failed to update'}", status=500, mimetype='application/json')
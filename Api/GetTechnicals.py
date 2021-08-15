import start
from Utils.ClassResolverFactory import getApiProvider
from Technicals.Technicals import Technicals
from flask import request, jsonify, Response


def getTechnicals():
    try:
        if 'apiProvider' in request.args:
            apiProviderName = request.args['apiProvider']
            apiProvider = getApiProvider(apiProviderName)
        else:
            raise
        if 'instruments' in request.args:
            symbols = request.args['instruments'].strip().split(",")
        if 'candleSize' in request.args:
            candleSize = request.args['candleSize']

        response = {"result": []}

        for symbol in symbols:
            try:

                timeSeries = start.getSeries(apiProvider, symbol, candleSize)

                technicals = Technicals(symbol, timeSeries)
                sma = round(technicals.SMA(20, "Close", candleSize), 2)

                ema = round(technicals.EMA(20, "Close", candleSize), 2)

                rsi = 1.09

                macd = 1.09

                response["result"].append({"instrument": symbol, "sma": sma, "ema": ema, "rsi": rsi, "macd": macd})
            except:
                continue

        response = jsonify(response)
        return response
    except Exception as e:
        Response("{'message':"+e+"'}", status=500, mimetype='application/json')

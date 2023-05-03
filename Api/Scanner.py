from Utils.ClassResolverFactory import getApiProvider, getScanner
from Utils.Symbols import getNifty500List
from Utils.Symbols import getNifty50List

from flask import request, jsonify, Response


def runScan():
    try:
        if 'apiProvider' in request.args:
            apiProviderName = request.args['apiProvider']
            apiProvider = getApiProvider(apiProviderName)
        else:
            raise
        if 'instruments' in request.args:
            if len(request.args['instruments'])>0 :
                symbols = request.args['instruments'].strip().split(",")
            else:
                symbols = getNifty50List()
        if 'scanners' in request.args:
            scanners = request.args['scanners'].strip().split(",")

        response = {"result": []}

        for scannerName in scanners:
            scanner = getScanner(scannerName)
            passedSymbols = []
            for symbol in symbols:
                if symbol=="WIPRO":
                    print("yo")
                success = scanner.isCriteriaMet(symbol, apiProvider=apiProvider)
                if success:
                    passedSymbols.append(symbol)
            response["result"].append({"name": scannerName, "passedSymbols": passedSymbols})

        return jsonify(response)
    except Exception as e:
        Response("{'message':'error while running scan'}", status=500, mimetype='application/json')

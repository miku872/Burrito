import json
import concurrent.futures
from Utils.Symbols import getNifty500List
from pojo.AbstractOrder import AbstractOrder

from Utils.Symbols import getNifty50List
import Strategy.stoplossTracker as StopLossTracker
from Utils.ClassResolverFactory import getApiProvider, getStrategy
from flask import request, jsonify, Response
from ApiProviders.AngelSmartApi.ClassResolver.ApiProvider import ApiProvider
from Strategy.Day20MACrossOverDay50MA import Day20MACrossOverDay50MA

import time



def runAlgo():
    try:
        print(request)
        if 'apiProvider' in request.args:
            apiProviderName = request.args['apiProvider']
            apiProvider = getApiProvider(apiProviderName)
        else:
            raise
        if 'strategies' in request.args:
            json_object = json.loads(request.args['strategies'])
            num = len(json_object)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []

                while (True):
                    # Create a queue for communication between the worker threads and the main thread

                    # Submit the algorithms to the executor
                    for i in range(num):
                        try :
                            panel_data = json_object[i]
                            strategy = getStrategy(panel_data['selectedStrategy'])
                            stocks = panel_data['selectedStocks']
                            if strategy:
                                if stocks and len(stocks)>0:
                                    executor.submit(strategy.deployStrategy(apiProvider,stocks))
                                else:
                                    stocks = getNifty50List();
                                    executor.submit(strategy.deployStrategy(apiProvider,stocks))
                        except Exception as e:
                            print(e)
                    print("adding stop loss to executor")
                    executor.submit(StopLossTracker.runStopLossTrackerUsingAPI(apiProvider))
                    concurrent.futures.wait(futures)
                    time.sleep(300)



        response = {"result": []}
        return response
    except Exception as e:
        response = {"result": []}
        return response
        raise e

def runAlgoCustom():
    try:
        apiProvider = ApiProvider()
        json_object = [ { "selectedStrategy" : "20DayMACrossOver50DayMA", "selectedStocks" : ["INFY"]}]
        # print(request)
        # if 'apiProvider' in request.args:
        #     apiProviderName = request.args['apiProvider']
        #     apiProvider = getApiProvider(apiProviderName)
        # else:
        #     raise
        # if 'strategies' in request.args:
        #     json_object = json.loads(request.args['strategies'])
        num = len(json_object)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []

            while (True):
                # Create a queue for communication between the worker threads and the main thread

                # Submit the algorithms to the executor
                for i in range(num):
                    try:
                        panel_data = json_object[i]
                        strategy = getStrategy(panel_data['selectedStrategy'])
                        stocks = panel_data['selectedStocks']
                        if strategy:
                            if stocks and len(stocks) > 0:
                                executor.submit(strategy.deployStrategy(apiProvider, stocks))
                            else:
                                stocks = getNifty50List();
                                executor.submit(strategy.deployStrategy(apiProvider, stocks))
                    except Exception as e:
                        print(e)
                concurrent.futures.wait(futures)
                time.sleep(300)

        # response = {"result": []}
        # return response
    except Exception as e:
        response = {"result": []}
        return response
        raise e
# def getPositions():
#     apiProvider = ApiProvider()
#
#     positions = apiProvider.getPositions()
#     holdings = apiProvider.getHoldings()
#
#     print(positions)
#
# getPositions()
    # Add new tasks to the queue

    # Wait for all the algorithms to finish
    # concurrent.futures.wait(futures)



import pandas as pd
import io
import requests

nifty_50_url = "https://www1.nseindia.com/content/indices/ind_nifty50list.csv"
nifty_500_url = "https://www1.nseindia.com/content/indices/ind_nifty500list.csv"
def getNifty50List():
    s = requests.get(nifty_50_url).content
    df = pd.read_csv(io.StringIO(s.decode('utf-8')))
    x = df.Symbol
    return x

def getNifty500List():
    s = requests.get(nifty_500_url).content
    df = pd.read_csv(io.StringIO(s.decode('utf-8')))
    x = df.Symbol
    return x

# import json
# import pandas as pd
# import io
# import requests
#
# nifty_50_url = "https://www1.nseindia.com/content/indices/ind_nifty50list.csv"
# nifty_500_url = "https://www1.nseindia.com/content/indices/ind_nifty500list.csv"
# file = open(r'/Users/mohit.dhariwal/Documents/symbols.txt','w+')
# def getNifty50List():
#     s = requests.get(nifty_50_url).content
#     df = pd.read_csv(io.StringIO(s.decode('utf-8')))
#     x = df.Symbol
#     return x
#
# def getNifty500List():
#     s = requests.get(nifty_500_url).content
#     df = pd.read_csv(io.StringIO(s.decode('utf-8')))
#     x = df.Symbol
#     return x
#
# nifty500 = getNifty500List().tolist()
# result = {}
# f = open("/Users/mohit.dhariwal/Documents/AngelBrokingSymbols.json",'r')
# data = json.loads(f.read())
# for dt in data:
#     if dt['symbol'] in nifty500:
#         result[dt['name']] = dt['token']
#
# for key in sorted(result):
#     file.writelines(key + "," + result[key] + '\n')
#
# print('yo')



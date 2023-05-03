import http.client
import pandas as pd
import io
import requests
import Constants


url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
nifty_50_url = "https://www1.nseindia.com/content/indices/ind_nifty50list.csv"
nifty_500_url = "https://www1.nseindia.com/content/indices/ind_nifty500list.csv"
def getNifty50List():
    s = requests.get(nifty_50_url).content
    df = pd.read_csv(io.StringIO(s.decode('utf-8')))
    print(df.columns)
    # x = df['Symbol']
    return df

def getNifty500List():
    s = requests.get(nifty_500_url).content
    df = pd.read_csv(io.StringIO(s.decode('utf-8')))
    x = df.Symbol
    return x

def update_data():
    s = requests.get(url).content
    df = pd.read_json(io.StringIO(s.decode('utf-8')))
    columns_to_check = ['symbol']
    df = df[df[columns_to_check].applymap(lambda x: str(x).endswith('EQ')).any(axis=1)]
    df = df[df['instrumenttype'] == '']
    nifty_50 = getNifty50List()
    left_join = nifty_50.merge(df, left_on = 'Symbol', right_on = 'name', how ='left')
    # print()
    projectPath = Constants.ProjectPath
    # file = open(projectPath + "ApiProviders/AngelSmartApi/Resources/NiftySymbols.csv", 'r')
    columns_to_write = ['name', 'token', 'symbol']

    left_join[columns_to_write].to_csv(projectPath + "ApiProviders/AngelSmartApi/Resources/NiftySymbols.csv", index=False)

update_data()

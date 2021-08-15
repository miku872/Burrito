import pandas as pd
import io
import requests

nifty_50_url = "https://www1.nseindia.com/content/indices/ind_nifty50list.csv"

def getNifty50List():
    s = requests.get(nifty_50_url).content
    df = pd.read_csv(io.StringIO(s.decode('utf-8')))
    x = df.Symbol
    return x

import os.path
import start
import pandas as pd
from Scans.MACrossOver.MACrossOverScan import isMACrossOver
from Scans.Scan import Scan
import Constants
import pandas as pd
from ApiProviders.AngelSmartApi.ClassResolver.ApiProvider import ApiProvider

projectPath = Constants.ProjectPath


class MACDBasedTrendSignal(Scan):

    def __init__(self):
        pass

    def isCriteriaMet(self, symbol, candleSize="DAILY", apiProvider=None, timeSeries=None, interval=None):


        # Set the start and end dates for the historical data
        if timeSeries is None:
            if os.path.exists(projectPath + "/resources/" + symbol + "/" + candleSize):
                timeSeries = pd.read_json(
                    projectPath + "/resources/" + symbol + "/" + candleSize + "/" + symbol + ".json",
                    convert_dates=True)
            else:
                timeSeries = start.getSeries(apiProvider, symbol, candleSize)
                if timeSeries is not None:
                    return self.isCriteriaMet(symbol, candleSize, interval)
                else:
                    return False
        if interval is not None:
            df_mask = (interval[0] <= timeSeries['timestamp']) & (timeSeries['timestamp'] <= interval[1])
            timeSeries = timeSeries[df_mask]

        if timeSeries is not None:

            timeSeries.loc[:, 'ma12'] = timeSeries['Close'].rolling(window=12).mean()
            timeSeries.loc[:, 'ma26'] = timeSeries['Close'].rolling(window=26).mean()

            # Calculate the MACD line and signal line
            timeSeries.loc[:, 'macd_line'] = timeSeries['ma12'] - timeSeries['ma26']
            timeSeries.loc[:, 'signal_line'] = timeSeries['macd_line'].rolling(window=9).mean()

            # Generate trading signals based on the MACD crossover
            timeSeries.loc[:, 'position'] = 0
            timeSeries.loc[:, 'position'][timeSeries['macd_line'] > timeSeries['signal_line']] = 1
            timeSeries.loc[:, 'position'][timeSeries['macd_line'] < timeSeries['signal_line']] = -1

            print(timeSeries.to_string())

            # Calculate the daily returns based on the trading signals
            timeSeries.loc[:, 'returns'] = timeSeries['Close'].pct_change() * timeSeries['position'].shift(1)
            print(timeSeries.to_string())


            # Calculate the cumulative returns and plot the results
            timeSeries.loc[:, 'cumulative_returns'] = (1 + timeSeries['returns']).cumprod()
            print(timeSeries.to_string())
            timeSeries.loc[:, 'cumulative_returns'].plot()

scan = MACDBasedTrendSignal()
scan.isCriteriaMet("SBIN","DAILY",ApiProvider())

# # Download historical data for a stock
# df = yf.download('AAPL', start=start_date, end=end_date)
#
# # Calculate the 12-day and 26-day moving averages
# df['ma12'] = df['Close'].rolling(window=12).mean()
# df['ma26'] = df['Close'].rolling(window=26).mean()
#
# # Calculate the MACD line and signal line
# df['macd_line'] = df['ma12'] - df['ma26']
# df['signal_line'] = df['macd_line'].rolling(window=9).mean()
#
# # Generate trading signals based on the MACD crossover
# df['position'] = 0
# df['position'][df['macd_line'] > df['signal_line']] = 1
# df['position'][df['macd_line'] < df['signal_line']] = -1
#
# # Calculate the daily returns based on the trading signals
# df['returns'] = df['Close'].pct_change() * df['position'].shift(1)
#
# # Calculate the cumulative returns and plot the results
# df['cumulative_returns'] = (1 + df['returns']).cumprod()
# df['cumulative_returns'].plot()

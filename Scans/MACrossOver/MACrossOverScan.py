import numpy as np
from Technicals import SMA, EMA
import Constants

projectPath = Constants.ProjectPath


def isMACrossOver(symbol,
                  windows,
                  maType,
                  candleSize="DAILY",
                  timeSeries=None):
    if timeSeries is not None:

        maxWindowSize = max(windows)
        timeSeries = timeSeries.tail(maxWindowSize + 3)
        if maType == "SMA":
            data0 = SMA.getSMA(symbol, windows[0], candleSize, timeSeries=timeSeries)
            timeseries = SMA.getSMA(symbol, windows[1], candleSize, timeSeries=data0)
        elif maType == 'EMA':
            data0 = EMA.getEMA(symbol, windows[0], candleSize, timeSeries=timeSeries)
            timeseries = SMA.getEMA(symbol, windows[1], candleSize, timeSeries=data0)

        timeseries.loc[:, 'Signal'] = timeseries[maType + str(windows[0])] - timeseries[maType + str(windows[1])]
        timeseries.loc[:, 'Position'] = (timeseries['Signal'].apply(np.sign) + 1) / 2

        isValidCrossOver0 = timeSeries['Position'].values[-1] - timeSeries['Position'].values[-2]
        isValidCrossOver1 = timeSeries['Position'].values[-1] - timeSeries['Position'].values[-3]

        if isValidCrossOver0 > 0 or isValidCrossOver1 > 0:
            return True

    return False

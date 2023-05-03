import pandas as pd


class Parser:
    timeSeriesColumns = []
    metaDataColumns = []
    timeSeriesColumn = ""
    metaDataColumn = None
    metaDataColumnIndex = [3]
    interval = ""

    def __init__(self, interval):
        self.interval = interval
        self.metaDataColumns = ['Information', 'Symbol', 'Last Refreshed', 'Output Size', 'Time Zone']

        self.timeSeriesColumns = ['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']

    def parsedDataset(self, response):
        dataList = response['data']
        df = pd.DataFrame(dataList, columns=self.timeSeriesColumns)
        if self.interval=="ONE_DAY":
            df['timestamp'] = df['timestamp'].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))
        df.sort_index(inplace=True, ascending=True)
        # extract the default columns
        df = df[self.timeSeriesColumns]
        return df

    def parsedMetadata(self, response):
        # 'Meta Data', index = 3
        dataList = response['data']
        if self.interval == "ONE_DAY":
            latestDataPoint = pd.Timestamp(dataList[-1][0]).strftime('%Y-%m-%d')
        metaData = {'Information': 'Equity', 'Symbol': 'xyz', 'Last Refreshed': latestDataPoint, 'Output Size': 0,
                    'Time Zone': 'GMT +5:30'}
        df = pd.DataFrame(metaData, columns=self.metaDataColumns, index=self.metaDataColumnIndex)
        df.sort_index(inplace=True, ascending=True)
        df = df[self.metaDataColumns]
        return df

    # def parsePositions(self, response):


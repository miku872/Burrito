import pandas as pd

class Parser:
    timeSeriesColumns = []
    metaDataColumns = []
    renameDict = {}
    timeSeriesColumn = ""
    metaDataColumn = "Meta Data"
    metaDataColumnIndex = [3]

    def __init__(self, interval):
        self.metaDataColumns = ['Information', 'Symbol', 'Last Refreshed', 'Output Size', 'Time Zone']

        if interval == "DAILY":
            self.timeSeriesColumns = ['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
            self.renameDict = {'1. open': 'Open',
                            '2. high': 'High',
                            '3. low': 'Low',
                            '4. close': 'Close',
                            '5. volume': 'Volume'}
            self.timeSeriesColumn = 'Time Series (Daily)'

        elif interval == "DAILY_ADJUSTED":
            self.timeSeriesColumns = ['timestamp', 'Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume']
            self.renameDict = {'1. open': 'Open',
                               '2. high': 'High',
                               '3. low': 'Low',
                               '4. close': 'Close',
                               '5. adjusted close': 'AdjClose',
                               '6. volume': 'Volume'}
            self.timeSeriesColumn = 'Time Series (Daily)'

        # self.timeSeriesColumn["WEEKLY", '')
        # self.timeSeriesColumn["WEEKLY_ADJUSTED", "")
        # self.timeSeriesColumn["MONTHLY", '')
        # self.timeSeriesColumn["MONTHLY_ADJUSTED", "")


    def parsedDataset(self, dataset):
        def convert_response(d):
            # convert the response into datetimerecords that can be
            # parsed by Pandas
            # 'Time Series (Daily)'
            for dt, prec in d[self.timeSeriesColumn].items():
                r = {'timestamp': dt}
                r.update(prec)
                yield r

        # pass your response 'page'
        df = pd.DataFrame(convert_response(dataset))
        # rename the columns
        df = df.rename(columns=self.renameDict)
        df['timestamp'] = df['timestamp'].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))
        # df.set_index('datetime', inplace=True)
        df.sort_index(inplace=True, ascending=False)
        # extract the default columns
        df = df[self.timeSeriesColumns]
        return df

    def parsedMetadata(self, metadata):
        # 'Meta Data', index = 3
        df = pd.DataFrame(metadata[self.metaDataColumn], self.metaDataColumnIndex)
        # df = pd.DataFrame.from_dict(df, index=[3])
        df = df.rename(columns={'1. Information': 'Information',
                                '2. Symbol': 'Symbol',
                                '3. Last Refreshed': 'Last Refreshed',
                                '4. Output Size': 'Output Size',
                                '5. Time Zone': 'Time Zone'})

        df['Last Refreshed'] = df['Last Refreshed'].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))

        df.sort_index(inplace=True, ascending=False)
        df = df[self.metaDataColumns]
        return df
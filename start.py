import json
import os.path

import datetime as datetime
import pandas as pd
import Constants

projectPath = Constants.ProjectPath
failedList = []


def getComparator():
    return str(datetime.date.today())


def getSeries(apiProvider, symbol, candleSize, start=None, end=None):
    try:
        if start is None:
            start = apiProvider.getCDCWatermark(symbol, candleSize)
        if candleSize == "DAILY":
            comparator = getComparator();
            if start != comparator:
                response = apiProvider.getResponse(symbol, candleSize, start=start, end=end)
                if response is not None:
                    parser = apiProvider.getResponseParser(candleSize)

                    refreshStamp = apiProvider.getRefreshStamp(response)

                    timeSeriesData = parser.parsedDataset(response)
                    metaData = parser.parsedMetadata(response)

                    if os.path.exists(projectPath + "resources/" + symbol + "/" + candleSize):
                        if start == refreshStamp:
                            pass
                        else:
                            localData = pd.read_json(
                                projectPath + "resources/" + symbol + "/" + candleSize + "/" + symbol + ".json",
                                convert_dates=False)
                            df_mask = timeSeriesData['timestamp'] > start
                            cdcDF = timeSeriesData[df_mask]
                            updatedData = localData.append(cdcDF)

                            updatedDataJson = updatedData.to_json(orient="records")
                            parsedUpdatedDataJson = json.loads(updatedDataJson)
                            with open(projectPath + "resources/" + symbol + "/" + candleSize + "/" + symbol + ".json", 'w',
                                      encoding='utf-8') as f:
                                json.dump(parsedUpdatedDataJson, f, ensure_ascii=False, indent=4, sort_keys=False)

                            localMetaDataJson = metaData.to_json(orient="records")
                            parsedMetaDataJson = json.loads(localMetaDataJson)
                            with open(projectPath + "resources/" + symbol + "/" + candleSize + "/" + "Metadata.json",
                                      'w') as f:
                                json.dump(parsedMetaDataJson, f, ensure_ascii=False, indent=4, sort_keys=False)
                            return updatedData
                    else:
                        try:
                            os.makedirs(projectPath + "resources/" + symbol + "/" + candleSize + "/")
                            metaDataJson = metaData.to_json(orient="records")
                            parsedMD = json.loads(metaDataJson)

                            latestDFJson = timeSeriesData.to_json(orient="records")
                            parsedDF = json.loads(latestDFJson)
                            with open(projectPath + "resources/" + symbol + "/" + candleSize + "/" + symbol + ".json",
                                      'w') as f:
                                json.dump(parsedDF, f, ensure_ascii=False, indent=4, sort_keys=False)
                            with open(projectPath + "resources/" + symbol + "/" + candleSize + "/Metadata.json", 'w') as f:
                                json.dump(parsedMD, f, ensure_ascii=False, indent=4, sort_keys=False)
                            return timeSeriesData
                        except:
                            os.removedirs(projectPath + "resources/" + symbol + "/" + candleSize + "/")
            else:
                return pd.read_json(projectPath + "resources/" + symbol + "/" + candleSize + "/" + symbol + ".json",
                                    convert_dates=True)
        else:
            response = apiProvider.getResponse(symbol, candleSize, start=start)
            if response is not None:
                parser = apiProvider.getResponseParser(candleSize)
                timeSeriesData = parser.parsedDataset(response)
                return timeSeriesData
    except Exception as e:
        raise e

    return None

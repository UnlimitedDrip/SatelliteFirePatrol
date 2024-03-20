from processDataManager import downloadFile
from processData import processFiles
from getData import getDataHelper, getDataCustomRange
from datetime import datetime, timedelta
from Averaging import AverageTempManager
import time


def main(startDate, endDate, dataPath, processedDataPath):
    timeStart = time.time()

    currentDate = datetime.strptime(startDate, "%Y-%m-%d")

    while currentDate <=  datetime.strptime(endDate, "%Y-%m-%d"):
        currentDateStr = currentDate.strftime("%Y-%m-%d")
        currentDate += timedelta(days=1)
        currentEndDateStr = currentDate.strftime("%Y-%m-%d")
        print(currentDateStr)
        filesToProcess = []

        # Get most recent data
        data = getDataCustomRange(printData=False, startDate=currentDateStr, endDate=currentEndDateStr)
        # print(data)
        if data:
            for entry in data["feed"]["entry"]:
                filename = entry["producer_granule_id"]
                links = entry["links"]
                downloadLink = links[0]["href"]

                # Downlod the file
                if downloadFile(downloadLink, f"{dataPath}/" + filename):
                    filesToProcess.append(filename)


            # process new data
            for file in filesToProcess:
                processFiles(f"{dataPath}/{file}", f"{processedDataPath}/" + file.replace(".h5", ".geojson"))
                AverageTempManager(f"{processedDataPath}/" + file.replace(".h5", ".geojson"))


    print(f"Time to execute in total {time.time() - timeStart}")

if __name__ == "__main__":
    currentTime = datetime.now()
    startDate = "2019-09-16" # ISO format
    endDate =  "2024-01-01"# ISO format
    dataPath = "Data/"
    processedDataPath = "ProcessedData/"

    main(startDate, endDate, dataPath, processedDataPath)

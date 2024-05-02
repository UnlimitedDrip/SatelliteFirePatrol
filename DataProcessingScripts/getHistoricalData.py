from processDataManager import downloadFile, checkIfFileInCSV
from processData import processFiles
from getData import getDataHelper, getDataCustomRange
from datetime import datetime, timedelta
from Averaging import AverageTempManager
import time
import csv
import subprocess
import os
import json

def main(startDate, endDate, dataPath, processedDataPath, csvPath):
    timeStart = time.time()
    csvData = []

    if not os.path.exists(csvPath):
        with open(csvPath, "w") as file:
            pass
    else:
        with open(csvPath, "r") as file:
            csvReader = csv.reader(file)
            for row in csvReader:
                csvData.extend(row)

    currentDate = datetime.strptime(startDate, "%Y-%m-%d")
    endDate = datetime.strptime(endDate, "%Y-%m-%d") + timedelta(days=0)

    while currentDate <= endDate:

        print(f"Current: {currentDate}, End {endDate}")

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

                # Check if file is already found locally
                if not checkIfFileInCSV(filename, csvData):
                    # Downlod the file
                    if downloadFile(downloadLink, f"{dataPath}/" + filename):
                        # Download the cloud masking file
                        cloudMaskLink = downloadLink.replace("ECO2LSTE.001", "ECO2CLD.001").replace("_L2_LSTE_", "_L2_CLOUD_")
                        cloudMaskFileName = filename.replace("_L2_LSTE_", "_L2_CLOUD_")
                        if downloadFile(cloudMaskLink, os.path.join(dataPath, cloudMaskFileName)):
                            filesToProcess.append(filename)
                            csvData.append(filename)
                else:
                    print("File already used")


        # process new data
        for file in filesToProcess:
            processFiles( os.path.join(dataPath, file), os.path.join( processedDataPath, file.replace(".h5", ".geojson") ) )
            averageTempFileCreated, averageFileName = AverageTempManager(processedDataPath, os.path.join( processedDataPath, file.replace(".h5", ".geojson") ), file.replace(".h5", ".geojson") )

            if averageTempFileCreated:
                csvData.append(averageFileName)

            #  Write to csv
            with open(csvPath, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(csvData)

    print(f"Time to execute in total {time.time() - timeStart}")

    directory = "/projects/climate_data"
    command = "publish_data ben/capstone_project"
    result = subprocess.run(command, cwd=directory, shell=True, capture_output=True, text=True)

    # Print the output
    print(result.stdout)

if __name__ == "__main__":
    currentTime = datetime.now()

    rawDataPath = ""
    processedDataPath = ""
    dataCsvPath = ""
    startDate = ""
    endDate = ""
    with open("dataConfig.json", "r") as dataConfigFile:
        dataConfigData = json.load(dataConfigFile)
        rawDataPath = dataConfigData["RawDataPath"]
        processedDataPath = dataConfigData["ProcessedDataPath"]
        dataCsvPath = dataConfigData["DataCsvPath"]
        startDate = dataConfigData["HistoricalStartDate"]
        endDate = dataConfigData["HistoricalEndDate"]

    main(startDate, endDate, rawDataPath, processedDataPath, dataCsvPath)

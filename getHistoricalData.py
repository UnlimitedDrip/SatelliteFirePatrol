from processDataManager import downloadFile
from processData import processFiles
from getData import getDataHelper


def main(startDate, endDate, dataPath, processedDataPath):
    filesToProcess = []

    # Get most recent data
    data = getDataCustomRange(printData=False, startDate=startDate, endDate=endDate)
    for entry in data["feed"]["entry"]:
        filename = entry["producer_granule_id"]
        links = entry["links"]
        downloadLink = links[0]["href"]

        # Downlod the file
        downloadFile(downloadLink, "Data/" + filename)
        filesToProcess.append(filename)


    # process new data
    for file in filesToProcess:
        processFiles(file, "ProcessedData/" + file.replace(".h5", ".geojson"))


if __name__ == "__main__":
    startDate = None # ISO format
    endDate = None # ISO format
    dataPath = "Data/"
    processedDataPath = "ProcessedData/"

    main(startDate, endDate, dataPath, processedDataPath)

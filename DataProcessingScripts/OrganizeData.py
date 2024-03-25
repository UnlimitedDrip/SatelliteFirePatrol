import os
import re
import shutil
from datetime import date

def createMonthFolder(base_folder, year, month):
    # Create the year folder
    yearFolder = os.path.join(base_folder, str(year))
    if not os.path.exists(yearFolder):
        os.makedirs(yearFolder)

    # Create the month folder
    monthFolder = os.path.join(yearFolder, str(month))
    if not os.path.exists(monthFolder):
        os.makedirs(monthFolder)

    return monthFolder

def readFileName(filePath):
    # Extract filename from the file path
    filename = os.path.basename(filePath)

    # Regex to find date in the filename
    datePattern = re.compile(r'(\d{4})(\d{2})\d{2}')
    match = datePattern.search(filename)

    if match:
        year, month = match.groups()
        # Call to organize by date
        monthFolder = createMonthFolder("ProcessedData", year, month)
        inputFolder = "ProcessedData"
        outputFolder1 = "H5"
        outputFolder2 = "GeoJSON"
        fileTypes1 = {".h5"}
        fileTypes2 = {".geojson"}

        organizeDataByType(inputFolder, monthFolder, outputFolder1, outputFolder2, fileTypes1, fileTypes2)
    else:
        return None

def organizeDataByType(inputFolder, destinationFolder, outputFolder1, outputFolder2, fileTypes1, fileTypes2):
    # Iterate through files in the input folder
    for root, _, files in os.walk(inputFolder):
        for file in files:
            filePath = os.path.join(root, file)
            _, fileExtension = os.path.splitext(file)

            # Extract date from the filename
            dateMatch = re.search(r'(\d{4})(\d{2})\d{2}', file)
            if dateMatch:
                year, month = dateMatch.groups()
                dateFolder = destinationFolder

                # Checks the extension and adds their destination based on type
                if fileExtension.lower() in fileTypes1:
                    outputFolder = os.path.join(dateFolder, outputFolder1)
                elif fileExtension.lower() in fileTypes2:
                    outputFolder = os.path.join(dateFolder, outputFolder2)
                else:
                    # Skip files with unknown extensions
                    continue

                # Create output folder if it doesn't exist
                os.makedirs(outputFolder, exist_ok=True)

                # Move the file to the folder
                destinationPath = os.path.join(outputFolder, file)
                shutil.move(filePath, destinationPath)
            else:
                # Skip files without a valid date in the filename
                continue

import numpy as np
import geojson
import h5py
import time
import json
from global_land_mask import globe

# Converts kelvin to F
# Scale the kelvin temp by .02
def tempConversion(tempValue):
    tempValue *= .02
    return (tempValue - 273.15) * (9/5) + 32

def check_quality(qc_flags):
    # Check bits 14 and 15 for quality assurance (less than 2k error)
    lst_accuracy_bits = np.bitwise_and(qc_flags, 0xC000) >> 14
    if lst_accuracy_bits != 0:
        return True

    return False


def checkUh(bit0P, bit1P, bit14P, bit15P, i, j):
    bit0 = bit0P[i][j]
    bit1 = bit1P[i][j]
    bit14 = bit14P[i][j]
    bit15 = bit15P[i][j]

    return (((bit0 == 0) and (bit1 == 0) and (bit14 == 1) and (bit15 == 1)) or ((bit0 == 0) and (bit1 == 0) and (bit14 == 0) and (bit15 == 1)))

# Accepts input and output file name
# Converts file to geojson of temperature
def processFiles(filenameInput, filenameOutput):

    cloudMaskFileName = filenameInput.replace("_L2_LSTE_", "_L2_CLOUD_")

    # Opens the file and gets box lat and long points as well as temp data
    with h5py.File(f"{filenameInput}", "r") as file:
        # Load bounding coordinates
        lstData = file['SDS']['LST'][:]
        qcData = file['SDS']['QC'][:]
        bit0 = np.bitwise_and(qcData, 1)
        bit1 = np.bitwise_and(qcData, 2)
        bit14 = np.bitwise_and(qcData, 2**14) >> 14
        bit15 = np.bitwise_and(qcData, 2**15) >> 15


        west = file["StandardMetadata/WestBoundingCoordinate"][0]
        east = file["StandardMetadata/EastBoundingCoordinate"][0]
        north = file["StandardMetadata/NorthBoundingCoordinate"][0]
        south = file["StandardMetadata/SouthBoundingCoordinate"][0]

    with h5py.File(f"{cloudMaskFileName}", "r") as file:
        # Lo    ad bounding coordinates
        cloudMask = file["SDS"]["CloudMask"][:]
        bit0CloudMask = np.bitwise_and(cloudMask, 1)
        bit1CloudMask = np.bitwise_and(cloudMask, 2) >> 1

    numOfRows, numOfCols = len(lstData), len(lstData[0])  # As mentioned in your data structure

    lats = np.linspace(north, south, numOfRows)
    longs = np.linspace(west, east, numOfCols)


    lat, long = lats[0], longs[0]

    features = []

    timeStart = time.time()

    count = 0
    divider = lstData.shape[0]


    # Get coordstep from config
    coordStep = 10
    with open("dataConfig.json", "r") as dataConfigFile:
        dataConfigData = json.load(dataConfigFile)
        coordStep = int(dataConfigData["ProcessingDataCoordStep"])


    # Iterate through the LST data and convert each data point to a GeoJSON point feature
    for i in range(0, lstData.shape[0], coordStep):
        count += 1
        progress = (count / divider) * coordStep
        print(f"Progress: [{int(progress * 50) * '#'}{' ' * (50 - int(progress * 50))}] {progress * 100:.2f}%", end='\r', flush=True)
        for j in range(0, lstData.shape[1], coordStep):
            lat, lon = lats[i], longs[j]

            # Converts point to geojson form
            # if globe.is_land(lat, lon) and (bit0CloudMask[i, j] == 1 and bit1CloudMask[i, j] == 1) and check_quality(qcData[i][j]):
            if globe.is_land(lat, lon) and checkUh(bit0, bit1, bit14, bit15, i,j):
                convertedTempF = tempConversion(float(lstData[i, j]))

                if convertedTempF > 0:

                    feature = geojson.Feature(
                        geometry=geojson.Point((lon, lat)),
                        properties={"LST": convertedTempF}
                    )
                    features.append(feature)


    # Get data ready to be written to file
    feature_collection = geojson.FeatureCollection(features)

    timeEnd = time.time()
    print(f"\nTime to execute: {timeEnd - timeStart}")

    with open(filenameOutput, 'w') as f:
        json.dump(feature_collection, f)

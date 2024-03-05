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

# Accepts input and output file name
# Converts file to geojson of temperature
def processFiles(filenameInput, filenameOutput):

    # Opens the file and gets box lat and long points as well as temp data
    with h5py.File(f"Data/{filenameInput}", "r") as file:
        # Load bounding coordinates
        lstData = file['SDS']['LST'][:]


        west = file["StandardMetadata/WestBoundingCoordinate"][0]
        east = file["StandardMetadata/EastBoundingCoordinate"][0]
        north = file["StandardMetadata/NorthBoundingCoordinate"][0]
        south = file["StandardMetadata/SouthBoundingCoordinate"][0]


    numOfRows, numOfCols = len(lstData), len(lstData[0])  # As mentioned in your data structure

    lats = np.linspace(north, south, numOfRows)
    longs = np.linspace(west, east, numOfCols)


    lat, long = lats[0], longs[0]

    features = []

    timeStart = time.time()

    # shp file
    # lst - cloudmask_qaqc.py
        # cloud masks
        # quality control

    count = 0
    divider = lstData.shape[0]
    coordStep = 10
    # Iterate through the LST data and convert each data point to a GeoJSON point feature
    for i in range(0, lstData.shape[0], coordStep):
        count += 1
        progress = (count / divider) * coordStep
        print(f"Progress: [{int(progress * 50) * '#'}{' ' * (50 - int(progress * 50))}] {progress * 100:.2f}%", end='\r', flush=True)
        for j in range(0, lstData.shape[1], coordStep):
            lat, lon = lats[i], longs[j]

            # Converts point to geojson form
            if globe.is_land(lat, lon):
                feature = geojson.Feature(
                    geometry=geojson.Point((lon, lat)),
                    properties={"LST": tempConversion(float(lstData[i, j]))}
                )
                features.append(feature)

    # Get data ready to be written to file
    feature_collection = geojson.FeatureCollection(features)

    timeEnd = time.time()
    print(f"\nTime to execute: {timeEnd - timeStart}")

    with open(filenameOutput, 'w') as f:
        json.dump(feature_collection, f)

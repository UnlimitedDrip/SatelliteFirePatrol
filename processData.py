import numpy as np
import geojson
import h5py
import time
import json

# Converts kelvin to F
# Scale the kelvin temp by .02
def tempConversion(tempValue):
    tempValue *= .02
    return (tempValue - 273.15) * (9/5) + 32

# Converts row/col index to lat, long
def index_to_latlong(row_index, col_index):
    return lats[row_index], longs[col_index]

# Accepts input and output file name
# Converts file to geojson of temperature
def processFiles(filenameInput, filenameOutput):

    # Opens the file and gets box lat and long points as well as temp data
    with h5py.File(f"Data/{filenameInput}", "r") as file:
        # Load bounding coordinates
        lst_data = file['SDS']['LST'][:]


        west = file["StandardMetadata/WestBoundingCoordinate"][0]
        east = file["StandardMetadata/EastBoundingCoordinate"][0]
        north = file["StandardMetadata/NorthBoundingCoordinate"][0]
        south = file["StandardMetadata/SouthBoundingCoordinate"][0]


    num_rows, num_cols = len(lst_data), len(lst_data[0])  # As mentioned in your data structure

    lats = np.linspace(north, south, num_rows)
    longs = np.linspace(west, east, num_cols)


    lat, long = lats[0], longs[0]

    features = []

    timeStart = time.time()

    # shp file
    # lst - cloudmask_qaqc.py
        # cloud masks
        # quality control

    count = 0
    divider = lst_data.shape[0]
    # Iterate through the LST data and convert each data point to a GeoJSON point feature
    for i in range(0, lst_data.shape[0], 10):
        count += 1
        progress = count / divider
        print(f"Progress: [{int(progress * 50) * '#'}{' ' * (50 - int(progress * 50))}] {progress * 100:.2f}%", end='\r', flush=True)
        for j in range(0, lst_data.shape[1], 10):
            lat, lon = lats[i], longs[j]

            # Converts point to geojson form
            if lst_data[i,j] != 0:
                feature = geojson.Feature(
                    geometry=geojson.Point((lon, lat)), 
                    properties={"LST": tempConversion(float(lst_data[i, j]))}
                )
                features.append(feature)

    # Get data ready to be written to file
    feature_collection = geojson.FeatureCollection(features)

    timeEnd = time.time()
    print(f"Time to execute: {timeEnd - timeStart}")

    with open(filenameOutput, 'w') as f:
        json.dump(feature_collection, f)

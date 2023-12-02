import numpy as np
import geojson
import h5py
import time
import json

def tempConversion(tempValue):
    tempValue *= .02
    return (tempValue - 273.15) * (9/5) + 32

def processFiles(filenameInput, filenameOutput):
    filename = "ECOSTRESS_L2_LSTE_08603_010_20200111T171110_0601_01.h5"

    with h5py.File(f"Data/{filename}", "r") as file:
        # Load bounding coordinates

        # print(file['SDS']['LST'].keys())
        print(file['SDS']['LST'][:][1][4000:5000])
        print("\n"*5)
        print(file['L2 LSTE Metadata'].keys())
        print(file['L2 LSTE Metadata']['Emis2GoodAvg'][:])
        print("\n"*5)
        lst_data = file['SDS']['LST'][:]


        west = file["StandardMetadata/WestBoundingCoordinate"][0]
        east = file["StandardMetadata/EastBoundingCoordinate"][0]
        north = file["StandardMetadata/NorthBoundingCoordinate"][0]
        south = file["StandardMetadata/SouthBoundingCoordinate"][0]


    # Assuming the LST data has shape (num_rows, num_cols)
    num_rows, num_cols = len(lst_data), len(lst_data[0])  # As mentioned in your data structure

    # Create arrays of latitudes and longitudes
    lats = np.linspace(north, south, num_rows)
    longs = np.linspace(west, east, num_cols)

    def index_to_latlong(row_index, col_index):
        return lats[row_index], longs[col_index]

    # Test conversion
    lat, long = index_to_latlong(0, 0)
    print(f"(0, 0) maps to ({lat}, {long})")

    # Create an empty list to store our GeoJSON features
    features = []

    timeStart = time.time()

    # Iterate through the LST data and convert each data point to a GeoJSON point feature
    print(lst_data.shape[0])
    print(lst_data.shape[1])
    count = 0
    divider = lst_data.shape[0]
    for i in range(0, lst_data.shape[0], 2):
        print(f"Progress: {count / divider}")
        count += 1
        for j in range(0, lst_data.shape[1], 2):
            lat, lon = index_to_latlong(i, j)  # Make sure this returns (latitude, longitude)

            if lst_data[i,j] != 0:
                feature = geojson.Feature(
                    geometry=geojson.Point((lon, lat)),  # Assuming (longitude, latitude)
                    properties={"LST": tempConversion(float(lst_data[i, j]))}
                )
                features.append(feature)

    feature_collection = geojson.FeatureCollection(features)

    timeEnd = time.time()
    print(f"Time to execute: {timeEnd - timeStart}")

    with open(filenameOutput, 'w') as f:
        json.dump(feature_collection, f)

from global_land_mask import globe
import numpy as np
import time
import geojson
import json
import os

# Returns (true, averageTempFileName) if new average temp file was created
# Returns (false, averageTempFileName) is no new file was created
def AverageTempManager(directoryPath, filePath, newFileName):

    # Get year and month from file name
    baseParse = newFileName.split('_')[5].split('T')[0]
    year = baseParse[0:4]
    month = baseParse[4:6]
    fileCreated = False

    print(f"Year: {year}\nMonth: {month}")

    # see if month's average file
    averageFileName = os.path.join(directoryPath, f"{year}_{month}_average.geojson")
    # averageFileName = f"ProcessedData/{year}_{month}_average.geojson"
    if not os.path.exists( f"{averageFileName}" ):
        # make the averaging file
        CreateAverageTempFile(averageFileName)
        fileCreated = True

    # Average with the new file
    AverageTemp(averageFileName, filePath)

    return (fileCreated, averageFileName)

def AverageTemp(averageTempFileName, newFileName):
    features = []
    tempDict = {}
    averageGeojsonData = None
    newTempGeojsonData = None
    timeStart = time.time()

    with open(averageTempFileName, 'r') as file:
        averageGeojsonData = geojson.load( file )

    # Create dictionary of average lst temps with [lon][lat] as the keys
    for feature in averageGeojsonData["features"]:
        lon, lat = feature["geometry"]["coordinates"]
        lst = feature["properties"]['LST']
        numOfReadings = feature["properties"]['numOfReadings']
        sumLST = feature["properties"]['sumLST']

        if lon not in tempDict:
            tempDict[lon] = {}

        tempDict[lon][lat] = {"LST": lst, "sumLST": sumLST, "numOfReadings": numOfReadings}

    with open(newFileName, 'r') as file:
        newTempGeojsonData = geojson.load( file )

    for feature in newTempGeojsonData["features"]:
        lon, lat = feature["geometry"]["coordinates"]

        lon = round(lon, 2)
        lat = round(lat, 2)

        if lon in tempDict and lat in tempDict[lon]:

            tempDict[lon][lat]["numOfReadings"] += 1
            tempDict[lon][lat]["sumLST"] += feature["properties"]["LST"]
            tempDict[lon][lat]["LST"] = tempDict[lon][lat]["sumLST"] / tempDict[lon][lat]["numOfReadings"]

    # convert tempDict to feature collection
    for lonKey in tempDict.keys():
        for latKey in tempDict[lonKey].keys():

            feature = geojson.Feature(
                geometry=geojson.Point((lonKey, latKey)),
                properties={
                         "LST": tempDict[lonKey][latKey]["LST"],
                         "sumLST": tempDict[lonKey][latKey]["sumLST"],
                         "numOfReadings": tempDict[lonKey][latKey]["numOfReadings"]
                        }
            )

            features.append(feature)


    # Write new data to average geojson
    # Get data ready to be written to file
    feature_collection = geojson.FeatureCollection(features)

    timeEnd = time.time()
    print(f"Time to average new file: {timeEnd - timeStart}")

    with open(averageTempFileName, 'w') as f:
        json.dump(feature_collection, f)


    return

def CreateAverageTempFile(averageTempFileName):
    # [-159.567123, 16.994625],  // Southwest coordinates: [longitude, latitude]
    # [-154.612488, 22.203054]   // Northeast coordinates: [longitude, latitude]
    timeStart = time.time()
    features = []

    coordStep = .01
    latStart = 16.9
    latEnd = 22.6
    lonStart = -160.8
    lonEnd = -154.61

    # Create a feature collection from south west to northeast iterating by .01
    for lat in np.arange(latStart, latEnd, coordStep):
        for lon in np.arange(lonStart, lonEnd, coordStep):
            if( globe.is_land(lat, lon) ):
                # round lat and long to 2 decimal places
                lat = round(lat, 2)
                lon = round(lon, 2)

                feature = geojson.Feature(
                    geometry=geojson.Point((lon, lat)),
                    properties={"LST": 0, "sumLST": 0, "numOfReadings": 0}
                )

                features.append(feature)


    # Get data ready to be written to file
    feature_collection = geojson.FeatureCollection(features)

    timeEnd = time.time()
    print(f"Time to create base averaging file: {timeEnd - timeStart}")

    with open(averageTempFileName, 'w') as f:
        json.dump(feature_collection, f)

    return


# CreateTempFile("ahhh.geojson")
# AverageTemp("ahhh.geojson", 'ProcessedData/ECOSTRESS_L2_LSTE_25502_004_20230104T082406_0601_02.geojson')

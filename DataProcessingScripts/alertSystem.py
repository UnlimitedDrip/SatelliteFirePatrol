import os
import json
import geojson
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



# Takes in geojson and loops through set alerts
def checkForAlerts(geojsonFilePath, alertFilePath):
    positiveAlerts = []
    alertsToCheck = None
    geojsonData = None

    geojsonFileName = os.path.basename(geojsonFilePath)


    # Read in alerts
    with open(alertFilePath, "r") as alertFile:
        alertsToCheck = json.load(alertFile)

    # Read in geojson
    with open(geojsonFilePath, "r") as geojsonFile:
        geojsonData = geojson.load(geojsonFile)

    # loop through alerts
    for alert in alertsToCheck:
        alertBoundingBox = alert["Bounding Box"]

        alertTempThreshold = alert["Temperature Threshold"]
        alertTriggeredCount = 0

        # Loop through points in geojson
        for feature in geojsonData['features']:
            pointLon, pointLat = feature.geometry.coordinates
            # Check if current lat and lon within bounding box
            if isPointInBoundingBox( pointLon, pointLat, alertBoundingBox  ):
                temperature = feature.properties.get('LST', None)

                #  Check if point is above temp Threshold
                if temperature > alertTempThreshold:
                    #  Incrememnt alertTriggered
                    alertTriggeredCount += 1

        if alertTriggeredCount > 0:
            sendAlerts(alert, alertTriggeredCount, geojsonFileName)
            alertTriggeredCount = 0


def isPointInBoundingBox(pointLon, pointLat, boundingBox):
    latStart, latEnd, lonStart, lonEnd = boundingBox

    if pointLat >= latStart and pointLat <= latEnd and pointLon >= lonStart and pointLon <= lonEnd:
        return True

    return False


def sendAlerts(alert, alertTriggeredCount, geojsonFileName):
    # Get base stats of geojson file
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    baseParse = geojsonFileName.split('_')[5].split('T')
    dateParse = baseParse[0]
    timeParse = baseParse[1]
    year = dateParse[0:4]
    month = months[int(dateParse[4:6])]
    day = dateParse[6:8]

    hour = timeParse[0:2]
    min = timeParse[2:4]
    sec = timeParse[4:6]

    # Construct alert string
    latStart, latEnd, lonStart, lonEnd = alert["Bounding Box"]
    alertString = f"Hello,\n\n\nYour alert \n\n\tlatitude start	→ {latStart}\n\tlatitude end	→ {latEnd}\n\tlongitude start	→ {lonStart}\n\tlongitude end	→ {lonEnd}\n\nhas been triggered on {month} {day}, {year} at {hour}:{min}:{sec} with {alertTriggeredCount} points exceeding temperature threshold ({alert['Temperature Threshold']})"


    username = 'thermalwatch25@gmail.com'
    password = '@|IIDK,k!_6)A.RJ+q[?'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(username, password)


    # Send alert
    print(f"Sent Alert: \n{alertString}")




checkForAlerts('ProcessedData/ECOSTRESS_L2_LSTE_05331_001_20190614T185704_0601_03.geojson', 'alertTesting.json')

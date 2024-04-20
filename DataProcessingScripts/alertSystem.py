import os
import json
import geojson
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sib_api_v3_sdk import ApiClient, Configuration
from sib_api_v3_sdk.api.transactional_emails_api import TransactionalEmailsApi
from sib_api_v3_sdk.models.send_smtp_email import SendSmtpEmail



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
                    #  Increment alertTriggered
                    alertTriggeredCount += 1

        if alertTriggeredCount > 0:
            sendAlerts(alert, alertTriggeredCount, geojsonFileName)
            alertTriggeredCount = 0


def isPointInBoundingBox(pointLon, pointLat, boundingBox):
    latStart, latEnd, lonStart, lonEnd = boundingBox

    if pointLat >= latStart and pointLat <= latEnd and pointLon >= lonStart and pointLon <= lonEnd:
        return True

    return False


def sendAlerts(alert, alertTriggeredCount, geojsonFileName, sendMessage=True):

    # Get api key
    apiKey = ""
    with open("dataConfig.json", "r") as dataConfigFile:
        dataConfigData = json.load(dataConfigFile)
        apiKey = dataConfigData["BrevoApiKey"]

    #Return out of function if no api key is gotten
    if apiKey == "":
        print("No api key provided\nPlease add an api key to dataConfig.json")
        return

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
    header = "Hello,"
    bodyIntro = "Your alert"
    latStart, latEnd, lonStart, lonEnd = alert["Bounding Box"]

    alertInfo = (f"has been triggered on {month} {day}, {year} at {hour}:{min}:{sec} with {alertTriggeredCount} points exceeding temperature threshold ({alert['Temperature Threshold']})")
    # alertString = f"Hello,\n\n\nYour alert \n\n\tlatitude start	→ {latStart}\n\tlatitude end	→ {latEnd}\n\tlongitude start	→ {lonStart}\n\tlongitude end	→ {lonEnd}\n\nhas been triggered on {month} {day}, {year} at {hour}:{min}:{sec} with {alertTriggeredCount} points exceeding temperature threshold ({alert['Temperature Threshold']})"

    htmlMessage = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>Alert Message</title>
    <style>
      pre {{
        white-space: pre-wrap;
        font-family: monospace;
      }}
    </style>
    </head>
    <body>
    <pre>
    {header}

    {bodyIntro}

        latitude start	→ {latStart}
        latitude end	→ {latEnd}
        longitude start	→ {lonStart}
        longitude end	→ {lonEnd}

    {alertInfo}
    </pre>
    </body>
    </html>
    """


    if sendMessage:
        # Configure API key authorization
        configuration = Configuration()
        configuration.api_key['api-key'] = apiKey

        # Create an instance of the API class
        api_instance = TransactionalEmailsApi(ApiClient(configuration))
        send_smtp_email = SendSmtpEmail(
            to=[{"email": alert["Email"], "name": "N/A"}],
            sender={"email": "thermalwatch25@gmail.com", "name": "ThermalWatch"},
            subject="Alert Triggered",
            html_content=f"{htmlMessage}"
        )

        try:
            # Send the email
            api_response = api_instance.send_transac_email(send_smtp_email)
            print(api_response)
        except Exception as e:
            print("An exception occurred when calling TransactionalEmailsApi->send_transac_email: %s\n" % e)


        # Send alert
        print(f"Sent Alert: \n{htmlMessage}")




checkForAlerts('ProcessedData/ECOSTRESS_L2_LSTE_05331_001_20190614T185704_0601_03.geojson', 'alertTesting.json')

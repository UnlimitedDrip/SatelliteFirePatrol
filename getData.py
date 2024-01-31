import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime, timedelta


# Requests ecostress data and returns a list of the responses
def getData(printData=True):

    # Current date and time
    current_time = datetime.now()

    # Format the current date and time as required by the API, typically in ISO format
    formatted_current_time = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Get start date
    start_date = (current_time - timedelta(days=10)).strftime('%Y-%m-%dT%H:%M:%SZ')


    data = getDataHelper(start_date, formatted_current_time)

    if data:
        if printData:
            print(json.dumps(data, indent=4))

    return data

def getDataCustomRange(printData=True, startDate, endDate):

    data = getDataHelper(startDate, endDate)

    if data:
        if printData:
            print(json.dumps(data, indent=4))

    return data


def getDataHelper(startDate, endDate):
    headers = {
    'Authorization': 'eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6InpoYWxsZW1leWVyIiwiZXhwIjoxNzAyNzY5MjIwLCJpYXQiOjE2OTc1ODUyMjAsImlzcyI6IkVhcnRoZGF0YSBMb2dpbiJ9.afDgMBmlw4PtQYLZ7A8MDulwDE8Jjrln_MkU_QxfrnyRq2FVBlBDvfhfBWFAwUtXWwgfPrw9GmfFS_JKpOaTsuPm01g2iI--C_QebWeDY5JDhiFdZ_Eo2hu0y3fs3EhBrJ8X4Lt_ZkmW4Xlc4Ox_0oNDnByKEmeyG11SZMZgZmKj3bmIVT64zfO-ZRgAd5lZemH2G7YslT0qQ1l3P9ZdaDt0JmgQ73i8kwZ_MW_ukl3WOL5C2o2hB08s8ZayW1Fp6ZXFCeKJuy0VWnpniw8TmuAlFu8pzctw7G56cfvRbgChy_qHqRp9fooWIf9h_DsAJ_6RCmQFoKDy_HeJ7RT4aA',
    }

    # Ecostress API endpoint
    api_endpoint = 'https://cmr.earthdata.nasa.gov/search/granules.json'

    params = {
    'short_name': 'ECO2LSTE',
    # [west_longitude,south_latitude,east_longitude,north_latitude]
    'bounding_box': '-160.703887,18.394145,-154.429128,22.376492',  # This is the bounding box for Hawaii
    'temporal': f'{start_date},{endDate}',
    }

    headers = {
        'accept': 'application/json',
    }
    response = requests.get(api_endpoint, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

    return data

# getData()

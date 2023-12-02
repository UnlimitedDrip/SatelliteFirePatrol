import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime, timedelta


def getData(printData=True):
    headers = {
    'Authorization': 'eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6InpoYWxsZW1leWVyIiwiZXhwIjoxNzAyNzY5MjIwLCJpYXQiOjE2OTc1ODUyMjAsImlzcyI6IkVhcnRoZGF0YSBMb2dpbiJ9.afDgMBmlw4PtQYLZ7A8MDulwDE8Jjrln_MkU_QxfrnyRq2FVBlBDvfhfBWFAwUtXWwgfPrw9GmfFS_JKpOaTsuPm01g2iI--C_QebWeDY5JDhiFdZ_Eo2hu0y3fs3EhBrJ8X4Lt_ZkmW4Xlc4Ox_0oNDnByKEmeyG11SZMZgZmKj3bmIVT64zfO-ZRgAd5lZemH2G7YslT0qQ1l3P9ZdaDt0JmgQ73i8kwZ_MW_ukl3WOL5C2o2hB08s8ZayW1Fp6ZXFCeKJuy0VWnpniw8TmuAlFu8pzctw7G56cfvRbgChy_qHqRp9fooWIf9h_DsAJ_6RCmQFoKDy_HeJ7RT4aA',
    }

    # Define the API endpoint
    api_endpoint = 'https://cmr.earthdata.nasa.gov/search/granules.json'


    # Current date and time
    current_time = datetime.now()

    # Format the current date and time as required by the API, typically in ISO format
    formatted_current_time = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    # You might want to look a few days or weeks back if the most recent data has not been processed yet.
    # For example, to look back 30 days from the current date:
    start_date = (current_time - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')

    # This is a simplified example; you'll need to adjust the parameters based on your specific data needs
    params = {
    'short_name': 'ECOSTRESS',  # This is a general name; specific datasets have specific short_names
    'bounding_box': '-154.0378492,18.589585,-160.744026,22.696332',  # This would search for data across the entire globe
    'temporal': f'{start_date},{formatted_current_time}',  # This would search for data in the year 2020
    }

    headers = {
        'accept': 'application/json',
    }

    # Make the HTTP request
    # response = requests.get(api_endpoint, params=params, headers=headers)

    url = "https://cmr.earthdata.nasa.gov/search/granules.json?short_name=ECO2LSTE&bounding_box=-180,-90,180,90&temporal=2020-01-01T00:00:00Z,2020-12-31T23:59:59Z"
    response = requests.get(url, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if printData:
            print(json.dumps(data, indent=4))
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")


    return data

# getData()

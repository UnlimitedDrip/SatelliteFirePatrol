from processData import processFiles
from getData import getData
import json
import geojson
import requests
from requests.auth import HTTPBasicAuth
import os

class SessionWithHeaderRedirection(requests.Session):

    AUTH_HOST = 'urs.earthdata.nasa.gov'

    def __init__(self, username, password):

        super().__init__()

        self.auth = (username, password)



    # Overrides from the library to keep headers when redirected to or from

    # the NASA auth host.

    def rebuild_auth(self, prepared_request, response):

        headers = prepared_request.headers

        url = prepared_request.url



        if 'Authorization' in headers:

            original_parsed = requests.utils.urlparse(response.request.url)

            redirect_parsed = requests.utils.urlparse(url)



        if ((original_parsed.hostname != redirect_parsed.hostname) and \

        redirect_parsed.hostname != self.AUTH_HOST and \

        original_parsed.hostname != self.AUTH_HOST):

            del headers['Authorization']



        return



def downloadFile(url, filename):
    username = "__"
    password = "__"
    token = 'eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6InpoYWxsZW1leWVyIiwiZXhwIjoxNzAyNzY5MjIwLCJpYXQiOjE2OTc1ODUyMjAsImlzcyI6IkVhcnRoZGF0YSBMb2dpbiJ9.afDgMBmlw4PtQYLZ7A8MDulwDE8Jjrln_MkU_QxfrnyRq2FVBlBDvfhfBWFAwUtXWwgfPrw9GmfFS_JKpOaTsuPm01g2iI--C_QebWeDY5JDhiFdZ_Eo2hu0y3fs3EhBrJ8X4Lt_ZkmW4Xlc4Ox_0oNDnByKEmeyG11SZMZgZmKj3bmIVT64zfO-ZRgAd5lZemH2G7YslT0qQ1l3P9ZdaDt0JmgQ73i8kwZ_MW_ukl3WOL5C2o2hB08s8ZayW1Fp6ZXFCeKJuy0VWnpniw8TmuAlFu8pzctw7G56cfvRbgChy_qHqRp9fooWIf9h_DsAJ_6RCmQFoKDy_HeJ7RT4aA'

    session = SessionWithHeaderRedirection(username, password)
    # session = SessionWithHeaderRedirection(token)


    try:
        response = session.get(url, stream=True)
        print(response.status_code)

        response.raise_for_status()

        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024*1024):
                file.write(chunk)

    # headers={"Authorization": "Bearer " + token}
    #
    # session = requests.session()
    # session.auth = HTTPBasicAuth(username, password)
    # response = session.get(url, headers=headers)
    # response.raise_for_status()
    except requests.exceptions.HTTPError as e:

        # handle any errors here

        print(e)


def main(getDataFlag=True, folderPath = ""):
    filesToProcess = []

    if getDataFlag:
        data = getData(printData=False)
        for entry in data["feed"]["entry"]:
            filename = entry["producer_granule_id"]

            links = entry["links"]
            downloadLink = links[0]["href"]

            # print(downloadLink)

            downloadFile(downloadLink, "Data/" + filename)
            filesToProcess.append(filename)
    else:
        for (dirpath, dirnames, filenames) in os.walk(folderPath):
            filesToProcess.extend(file for file in filenames)



    # process data

    for file in filesToProcess:
        processFiles(file, "ProcessedData/" + file.replace(".h5", ".geojson"))




if __name__ == "__main__":
    # main(False, "Data/")
    main()

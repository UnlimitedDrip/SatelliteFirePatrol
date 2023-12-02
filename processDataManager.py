from processData import processFiles
from getData import getData
import json
import geojson
import requests
from requests.auth import HTTPBasicAuth

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
    username = "zhallemeyer"
    password = "Momo_is_waifu05!"
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


def main():
    data = getData(printData=False)
    # filesToProcess = ["ECOSTRESS_L2_LSTE_08603_010_20200111T171110_0601_01.h5", "ECOSTRESS_L2_LSTE_08719_001_20200119T040945_0601_01.h5", "ECOSTRESS_L2_LSTE_08780_001_20200123T023443_0601_01.h5", "ECOSTRESS_L2_LSTE_08902_001_20200130T232741_0601_01.h5", "ECOSTRESS_L2_LSTE_09024_001_20200207T202041_0601_01.h5", "ECOSTRESS_L2_LSTE_09030_011_20200208T061207_0601_01.h5", "ECOSTRESS_L2_LSTE_09045_008_20200209T052434_0601_01.h5", "ECOSTRESS_L2_LSTE_09091_010_20200212T043833_0601_01.h5", "ECOSTRESS_L2_LSTE_09106_013_20200213T035100_0601_01.h5", "ECOSTRESS_L2_LSTE_09146_001_20200215T171336_0601_01.h5"]
    filesToProcess = []

    for entry in data["feed"]["entry"]:
        filename = entry["producer_granule_id"]

        links = entry["links"]
        downloadLink = links[0]["href"]

        # print(downloadLink)

        downloadFile(downloadLink, "Data/" + filename)
        filesToProcess.append(filename)



    # process data

    for file in filesToProcess:
        processFiles(file, "ProcessedData/" + file.replace(".h5", ".geojson"))




if __name__ == "__main__":
    main()
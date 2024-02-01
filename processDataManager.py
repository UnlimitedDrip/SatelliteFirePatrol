from processData import processFiles
from getData import getData
import json
import geojson
import shutil
import requests
from requests.auth import HTTPBasicAuth
import os

#data organization variables
input_folder = "ProcessedData"
output_folder_1 = "ProcessedData/H5"
output_folder_2 = "ProcessedData/GeoJSON"
file_types_1 = {".h5"} 
file_types_2 = {".geojson"}


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



# Downlods file at the url provided (change username and password)
def downloadFile(url, filename):
    username = "_"
    password = "_"
    token = 'eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6InpoYWxsZW1leWVyIiwiZXhwIjoxNzAyNzY5MjIwLCJpYXQiOjE2OTc1ODUyMjAsImlzcyI6IkVhcnRoZGF0YSBMb2dpbiJ9.afDgMBmlw4PtQYLZ7A8MDulwDE8Jjrln_MkU_QxfrnyRq2FVBlBDvfhfBWFAwUtXWwgfPrw9GmfFS_JKpOaTsuPm01g2iI--C_QebWeDY5JDhiFdZ_Eo2hu0y3fs3EhBrJ8X4Lt_ZkmW4Xlc4Ox_0oNDnByKEmeyG11SZMZgZmKj3bmIVT64zfO-ZRgAd5lZemH2G7YslT0qQ1l3P9ZdaDt0JmgQ73i8kwZ_MW_ukl3WOL5C2o2hB08s8ZayW1Fp6ZXFCeKJuy0VWnpniw8TmuAlFu8pzctw7G56cfvRbgChy_qHqRp9fooWIf9h_DsAJ_6RCmQFoKDy_HeJ7RT4aA'

    session = SessionWithHeaderRedirection(username, password)

    try:
        response = session.get(url, stream=True)
        print(response.status_code)

        response.raise_for_status()

        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024*1024):
                file.write(chunk)

    except requests.exceptions.HTTPError as e:

        # handle any errors here

        print(e)


# Downloads and converts the most recent data from NASA Ecostress
def main(getDataFlag=True, folderPath = ""):
    filesToProcess = []

    # check if new data is wanted
    if getDataFlag:
        # Get most recent data
        data = getData(printData=False)
        for entry in data["feed"]["entry"]:
            filename = entry["producer_granule_id"]
            links = entry["links"]
            downloadLink = links[0]["href"]

            # Downlod the file
            downloadFile(downloadLink, "Data/" + filename)
            filesToProcess.append(filename)
    # Otherwise, process the data that is avaliable locally
    else:
        for (dirpath, dirnames, filenames) in os.walk(folderPath):
            filesToProcess.extend(file for file in filenames)

    # process new data
    for file in filesToProcess:
        processFiles(file, "ProcessedData/" + file.replace(".h5", ".geojson"))
    
    #call to organizer function
    organize_data_by_type(input_folder, output_folder_1, output_folder_2, file_types_1, file_types_2)


def organize_data_by_type(input_folder, output_folder_1, output_folder_2, file_types_1, file_types_2):
    
    for root, _, files in os.walk(input_folder):
        
        for file in files:
            
            file_path = os.path.join(root, file)
            _, file_extension = os.path.splitext(file)

            
            if file_extension.lower() in file_types_1:
                output_folder = output_folder_1
            
            elif file_extension.lower() in file_types_2:
                output_folder = output_folder_2
            
            else:
                # Skip files with unknown extensions
                continue

            # Create output folder if it doesn't exist
            os.makedirs(output_folder, exist_ok=True)

            # Move the file to the folder
            destination_path = os.path.join(output_folder, file)

            shutil.move(file_path, destination_path)






if __name__ == "__main__":
    # main(False, "Data/")
    main()

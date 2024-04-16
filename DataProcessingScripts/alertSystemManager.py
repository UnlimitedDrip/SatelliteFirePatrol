import requests
import json 

url = 'http://localhost:3000/alertsystem'

with open("dataConfig.json", "r") as dataConfigFile:
    apiKey = json.load(dataConfigFile)["AWSApiKey"]

headers = {'api-key': apiKey}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    with open('alertTesting.json', 'wb') as f:
        f.write(response.content)
else:
    print("Failed to download file. Status code:", response.status_code)

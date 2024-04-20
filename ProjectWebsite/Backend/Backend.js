// =========== READ ME ===========
// DEPENDENCIES: npm install express cors axios
// TO RUN: node Backend.js
// ===============================

const express = require('express');
const cors = require('cors');
const axios = require('axios');
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');
const app = express();
app.use(cors());
app.use(bodyParser.json());

// ===================== RECIEVING FUNCTIONS =====================

// Get base data csv
app.get('/api/data', async (req, res) => {
    try {
        const response = await axios.get('https://rcdata.nau.edu/climate_data/capstone_project/data.csv');
        res.send(response.data);
    } catch (error) {
        res.status(500).send('Error fetching data');
    }
});

// Serve GeoJSON files
app.get('/api/geojson/:filename', async (req, res) => {
    const filename = req.params.filename;
    const externalUrl = `https://rcdata.nau.edu/climate_data/capstone_project/${filename}`;
    console.log(`Request for ${filename} recieved`);

    try {
        const response = await axios.get(externalUrl, { responseType: 'arraybuffer' });
        res.send(response.data);
        console.log(`Request for ${filename} sent`);
    } catch (error) {
        if (error.response) {
            res.status(error.response.status).send("Error fetching the file from the external source.");
        } else {
            console.error('Error fetching the external file:', error.message);
            res.status(500).send("Internal server error.");
        }
    }
});

// Get alerts associated with id parameter
app.get('/api/getalerts/:id', async (req, res) => {
    const id = req.params.id;
    const filePath = 'alertSystemStorage.json';
    let foundAlerts = [];
    console.log(`Request for alert system info - ${id} recieved`);
    
    // Read the existing JSON file
    fs.readFile(filePath, (err, fileData) => {
        if (err && err.code === 'ENOENT') {
            return res.status(500).send({ message: 'No alerts found' });
        } 
        else {
            // File exists, parse it and add the new alert
            const alerts = JSON.parse(fileData);

            for( let alert of alerts )
            {
                if( alert["Email"] === id)
                {
                    foundAlerts.push(alert);
                }
            }

            if(foundAlerts.length > 0)
            {
                return res.status(200).send(foundAlerts);
            }
            else 
            {
                return res.status(200).send({ message: 'No alerts found' });
            }
        }
    });

});


// ===================== SENDING FUNCTIONS =====================

app.use(express.static('public'));
app.get('/alertsystem', (req, res) => {
    console.log("Recieved request for alert system");
    const apiKey = req.headers['api-key'];
    let jsonData = null;

    // Get api key from config file
    try {
        const data = fs.readFileSync('../../DataProcessingScripts/dataConfig.json', 'utf8');
        jsonData = JSON.parse(data);
        console.log(jsonData);
    } catch (error) {
        console.error('Error reading the JSON file:', error);
    }

    // Check if api key matches
    if ( apiKey === jsonData["AWSApiKey"])
    {
        console.log("API key validated");
        // Get path
        const filePath = path.join(__dirname, 'alertSystemStorage.json');
        // send file
        res.sendFile(filePath, (err) => {
            if (err) {
                console.log('Error sending file:', err);
                res.status(500).send('Failed to send file');
            } else {
                console.log('File sent successfully');
            }
        });
    }
    else {
        res.status(403).send('Failed to send file');
    }

});

// ===================== POSTING FUNCTIONS =====================

app.post('/add-alert', (req, res) => {
    const data = req.body;
    const filePath = 'alertSystemStorage.json';
    let validationFlag = false;
    let expectedKeys = ["Bounding Box", "Temperature Threshold", "Email"]
    console.log("Recieved Add Alert Request");

    // Check if data is in correct form
    try 
    {
        if( Object.keys(data).length != 3 || !hasRequiredKeys(data, expectedKeys) 
            || !isNumber(data["Temperature Threshold"]) || !(isNumber(data["Temperature Threshold"]) > 0)
            || data["Bounding Box"].length != 4
            || !isValidEmail(data["Email"]) || !isNumber(data["Bounding Box"][0])
            || !isNumber(data["Bounding Box"][1]) || !isNumber(data["Bounding Box"][2])
            || !isNumber(data["Bounding Box"][3]) )
        {
            console.log("FAILED")
            return res.status(406).send({ message: 'Data failed validation' });
        }
    }
    catch( error )
    {
        if (error) return res.status(406).send({ message: 'Data failed validation' });
    }

    

    // Read the existing JSON file
    fs.readFile(filePath, (err, fileData) => {
        if (err && err.code === 'ENOENT') {
        // File does not exist, create it with the first alert
        fs.writeFile(filePath, JSON.stringify([data]), (err) => {
            if (err) return res.status(500).send({ message: 'Error saving data' });
            return res.send({ message: 'Alert added successfully' });
        });
        } else {
        // File exists, parse it and add the new alert
        const alerts = JSON.parse(fileData);
        alerts.push(data);
        fs.writeFile(filePath, JSON.stringify(alerts), (err) => {
            if (err) return res.status(500).send({ message: 'Error saving data' });
            console.log("SUCCESS")
            return res.send({ message: 'Alert added successfully' });
        });
        }
    });
});

app.post('/remove-alert', (req, res) => {
    const data = req.body;
    const filePath = 'alertSystemStorage.json';
    const boundingBoxToRemove = req.body["Bounding Box"];
    const id = req.body["Email"];
    console.log("Recieved Remove Alert Request");

    // Read the existing JSON file
    fs.readFile(filePath, (err, fileData) => {
        if (err && err.code === 'ENOENT') {
            return res.status(500).send({ message: 'No alerts found' });
        } 
        else {
            // File exists, parse it and add the new alert
            let alerts = JSON.parse(fileData);
            let removeIndex = -1;
            let index = 0;

            for(let alert of alerts)
            {
                if( alert["Email"] == id && 
                    boundingBoxToRemove[0] == alert["Bounding Box"][0] &&
                    boundingBoxToRemove[1] == alert["Bounding Box"][1] &&
                    boundingBoxToRemove[2] == alert["Bounding Box"][2] &&
                    boundingBoxToRemove[3] == alert["Bounding Box"][3])
                {
                    removeIndex = index;
                }
                index++;
            }

            if (index > -1) {
                alerts.splice(removeIndex, 1); 
                fs.writeFile(filePath, JSON.stringify(alerts), (err) => {
                    if (err) return res.status(500).send({ message: 'Error saving data' });
                    return res.send({ message: 'Alert removed successfully' });
                });
            }
            else {
                return res.send({ message: 'No Alert found to be deleted' });
            }
        

        }
    });
});

function hasRequiredKeys(jsonObject, requiredKeys) {
    return requiredKeys.every(key => key in jsonObject);
}

function isNumber(value) {
    return typeof value === 'number';
}

function isValidEmail(email) {
    var regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
  }
  

// ===================== SET UP FUNCTIONS =====================
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

// =========== READ ME ===========
// DEPENDENCIES: npm install express cors axios
// TO RUN: node Backend.js
// ===============================



const express = require('express');
const cors = require('cors');
const axios = require('axios');
const app = express();
const path = require('path');
const fs = require('fs');
app.use(cors());

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


// ===================== SET UP FUNCTIONS =====================
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

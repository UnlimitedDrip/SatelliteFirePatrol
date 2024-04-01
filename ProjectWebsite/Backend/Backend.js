// =========== READ ME ===========
// DEPENDENCIES: npm install express cors axios
// TO RUN: node Backend.js
// ===============================



const express = require('express');
const cors = require('cors');
const axios = require('axios');
const app = express();
app.use(cors());


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

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

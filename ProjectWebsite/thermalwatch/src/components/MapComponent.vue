<template>
<div id="map-container">
  <div id="map"></div>
</div>

<div class="map-overlay">

  <div class="map-overlay-item">
    <div class='cal'>
      <datepicker
        v-model="selected"
        :locale="locale"
        :upperLimit="to"
        :lowerLimit="from"
        :disabled-dates="disabledDates"
        @update:modelValue="dateSelected"
      />
    </div>

    <div class="map-temp-info-container">
      <h2 class="temp-info" id="temp-info">55°F</h2>
    </div>

    <select id="dropdownYear" @change="updateYear($event)"></select>

  </div>


  <div class="map-overlay-inner">
    <h2 id="slider-text">Temperatures over 2019</h2>
    <label ref="month"></label>
    <input id="slider" type="range" min="0" max="11" step="1" value="0" @change="updateDataListSlider($event)" ref="slider">
  </div>

  <div class="map-overlay-inner">
    <div id="legend" class="legend">
      <div class="bar"></div>
      <div> Fahrenheit (f)</div>
    </div>
    <button @click="downloadCurrentGeoJSON()">Download GeoJSON</button>
    <button id="create-alert-button" @click="createAlert()">Create an Alert</button>

    <div class="number-input-container">
      <label for="emailInput">Enter a valid email</label>
      <input type="email" id="emailInput" name="emailInput">
      <label for="numberInput">Enter a temperature threshold in Fahrenheit</label>
      <input type="number" id="numberInput" name="numberInput">
      <button type="submit" @click="submitAlert()">Submit</button>
      <p>Click a drag to draw a rectangle and enter a temperature max. If the temperature threshold is exceeded, you will be emailed</p>
    </div>
  </div>
</div>

</template>

<script>
// Lines needed to be changed for url are 405, 425, 441, 455, 489, 505, 522
import mapboxgl from 'mapbox-gl';
import Datepicker from 'vue3-datepicker';
import { enUS } from 'date-fns/locale';
// import "@mapbox/mapbox-gl-draw/dist/mapbox-gl-draw.css";


export default {
  data() {
    return {
      locale: enUS,
      to: new Date(), //present day
      from: new Date(2019, 0, 1), // January 1st, 2019
      disabledDates: {
        dates: []
      },
      preventDisableDateSelection: true,
      selected: new Date(),
      dataList: [],
      map: null,
      year: 2023,
      month: 1,
      latStart: null,
      latEnd: null,
      lonStart: null,
      lonEnd: null,
    };
  },
  components: {
    Datepicker
  },
  methods: {
    filterByMonth(month) {
      const months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
      ];
      // Set the label to the month using Vue's ref
      this.$refs.month.textContent = months[month];
    },
    updateDataListSlider(event) {
      var monthVal = Number(event.target.value)+1;
      this.month = monthVal;
      this.updateAverageOverlayHelper()
    },
    updateYear(event){
      this.year = event.target.options[event.target.selectedIndex].value;
      document.getElementById('slider-text').textContent = `Temperatures over ${this.year}`
      this.updateAverageOverlayHelper()
    },
    updateAverageOverlayHelper() {
      const prefix = this.month >= 10 ? "" : "0";
      const averageFilename = `${this.year}_${prefix}${this.month}_average.geojson`;
      this.dataList = [averageFilename];
      this.fetchFile(averageFilename);
    },
    dateSelected(newDate) {
      if( newDate )
      {
        // get date in form -> yyyymmdd
        const date = this.formatDate(newDate);
        // Get date data
        let files = this.getFilesFromDate(date)

        this.dataList = []
        for(let index = 0; index < files.length; index++)
        {
          this.fetchFileMutliple(files[index], index)
          this.dataList.push(files[index])
        }
      }
    },
    async setDisabledDates() {
      // Set starting date and end date we want to disable data for
      let start = new Date("01/01/2019");
      let end = new Date();

      var date = new Date(start);
      while(date <= end){
        // Convert date to string and get file data for that date
        let dateStr = this.formatDate(date);
        let files = this.getFilesFromDate(dateStr);

        // If there is no file data for that date, disable it
        if(files.length == 0){
          this.disabledDates.dates.push(new Date(date));
        }

        // Index to next date
        var newDate = date.setDate(date.getDate() + 1);
        date = new Date(newDate);
      }
    },
    formatDate(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}${month}${day}`;
    },
    getFilesFromDate(date){
      if( !this.fileContent ) return;

      const options = this.fileContent.split(',');

      const matchingFiles = options.filter(option => {
        const parts = option.split('_');
        if (parts.length < 6) return false;
        const fileDate = parts[5].split('T')[0];
        return fileDate === date;
      });

      return matchingFiles
    },
    removeOldLayers() {
      const map = this.map;
      if (!map) return;

      // remove old layers
      map.getStyle().layers.forEach((layer) => {
        if (layer.id.startsWith('temperature-circles')) {
          map.removeLayer(layer.id);
        }
      });

      const existingSources = map.getStyle().sources;
      // Remove existing sources
      if (existingSources) {
        Object.keys(existingSources).forEach((sourceId) => {
          if (sourceId.startsWith('lst')) {
            map.removeSource(sourceId);
          }
        });
      }
    },
    reloadMapOverlay() {

      const map = this.map;
      if (!map) return;

      this.removeOldLayers();

      this.dataList.forEach((data, index) => {
          this.reloadMapOverlayHelper(data, index);
      });
    },
    reloadMapOverlayHelper(geojsonData, index, removeOldLayersFlag=true) {

      const map = this.map;
      if (!map) return;

      if(removeOldLayersFlag)
      {
        this.removeOldLayers()
      }
      map.addSource('lst' + index, {
        type: 'geojson',
        data: geojsonData
      });

      map.addLayer({
        'id': 'temperature-circles' + index,
        'type': 'circle',
        'source': 'lst' + index,
        'paint': {
          'circle-color': [
            'interpolate',
            ['linear'],
            ['get', 'LST'],
            0, '#313695',
            50, '#009966',
            100, '#d73027',
            150, '#A020F0'
          ],
          'circle-radius': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5, 1,
            8, 2,
            10, 5,
            11, 10,
            15, 75,
          ],
          'circle-opacity':  [
            'interpolate',
            ['linear'],
            ['zoom'],
            5, .4,
            15, .7
          ],
        }
      });


      // Mouse enter event
      map.on('mouseenter', 'temperature-circles' + index, (e) => {
        map.getCanvas().style.cursor = 'pointer';
        //const coordinates = e.features[0].geometry.coordinates.slice();
        const temperature = e.features[0].properties.LST;

        document.getElementById("temp-info").textContent = temperature.toFixed(2) + "°F";
      });

    },
    createAlert() {
      const map = this.map;
      if (!map) return;
      // remove old layers
      map.getStyle().layers.forEach((layer) => {
        if (layer.id.startsWith('rectangle')) {
          console.log("rah")
          map.removeLayer(layer.id);
        }
      });
      const existingSources = map.getStyle().sources;
      // Remove existing sources
      if (existingSources) {
        Object.keys(existingSources).forEach((sourceId) => {
          if (sourceId.startsWith('rectangle')) {
            map.removeSource(sourceId);
          }
        });
      }

      // Check if creating or canceling
      if(this.drawingRectangle)
      {
        document.getElementById('create-alert-button').innerText = 'Create an Alert';
        document.querySelector('.number-input-container').style.display = 'none';
        this.drawingRectangle = false;
      }
      else
      {
        document.getElementById('create-alert-button').innerText = 'Cancel Alert';
        document.querySelector('.number-input-container').style.display = 'block';

        this.drawingRectangle = true;
        this.map.on('mousedown', this.onMouseDown);
        this.map.once('mouseup', this.onMouseUp);
      }
    },
    onMouseDown(e) {

      if(!this.drawingRectangle) return;

      // Prevent the default map drag behavior
      this.map.dragPan.disable();

      // Record the start position
      this.start = e.lngLat;

      // Add a temporary rectangle to the map
      this.map.addSource('rectangle', {
          type: 'geojson',
          data: {
              type: 'Feature',
              geometry: {
                  type: 'Polygon',
                  coordinates: [[
                      [this.start.lng, this.start.lat],
                      [this.start.lng, this.start.lat],
                      [this.start.lng, this.start.lat],
                      [this.start.lng, this.start.lat],
                      [this.start.lng, this.start.lat]
                  ]]
              }
          }
      });

      // Add rectangle as layer
      this.map.addLayer({
          id: 'rectangle',
          type: 'fill',
          source: 'rectangle',
          layout: {},
          paint: {
              'fill-color': '#088',
              'fill-opacity': 0.5
          }
      });

      // Listen for mouse movement to update the rectangle
      this.map.on('mousemove', this.onMouseMove);
    },
    onMouseMove(e) {
      // Update the rectangle's coordinates based on the current pointer location
      const current = e.lngLat;
      const coordinates = this.map.getSource('rectangle')._data.geometry.coordinates[0];
      coordinates[1] = [current.lng, this.start.lat];
      coordinates[2] = [current.lng, current.lat];
      coordinates[3] = [this.start.lng, current.lat];
      coordinates[4] = [this.start.lng, this.start.lat];

      this.latStart = Math.min(this.start.lat, current.lat);
      this.latEnd = Math.max(this.start.lat, current.lat);
      this.lonStart = Math.min(this.start.lng, current.lng);
      this.lonEnd = Math.max(this.start.lng, current.lng);

      this.map.getSource('rectangle').setData({
          type: 'Feature',
          geometry: {
              type: 'Polygon',
              coordinates: [coordinates]
          }
      });
    },
    onMouseUp() {
      // Remove the temporary event listeners
      this.map.off('mousemove', this.onMouseMove);

      // Allow the map to be panned again
      this.map.dragPan.enable();

      // Set drawing mode to false
      this.drawingRectangle = false;

      // Optionally, handle the rectangle (e.g., make an API call or update the state)
    },
    submitAlert() {

      const map = this.map;
      if (!map) return;
      // remove old layers
      map.getStyle().layers.forEach((layer) => {
        if (layer.id.startsWith('rectangle')) {
          console.log("rah")
          map.removeLayer(layer.id);
        }
      });
      const existingSources = map.getStyle().sources;
      // Remove existing sources
      if (existingSources) {
        Object.keys(existingSources).forEach((sourceId) => {
          if (sourceId.startsWith('rectangle')) {
            map.removeSource(sourceId);
          }
        });
      }

      document.querySelector('.number-input-container').style.display = 'none';

      // Add Alert to database
      let boundingBox = [this.latStart, this.latEnd, this.lonStart, this.lonEnd];
      let temperatureThreshold =  Number(document.getElementById('numberInput').value);
      let email =  document.getElementById('emailInput').value;

      let jsonObject = {"Bounding Box": boundingBox, "Temperature Threshold": temperatureThreshold, "Email": email};

      fetch('http://35.82.41.91:3000/add-alert', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonObject)
      })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error('Error:', error));

      this.latStart = null;
      this.latEnd = null;
      this.lonStart = null;
      this.lonEnd = null;

      document.getElementById('create-alert-button').innerText = 'Create an Alert';
    },
    async getAlerts(id) {
      try {
        const targetUrl = `35.82.41.91:3000/api/getalerts/${id}`;
        const response = await fetch(targetUrl);

        if (!response.ok) {
          throw new Error('Failed to fetch');
        }

        let alertArray = await response.text();
        console.log(alertArray)
      }
      catch(error)
      {
        console.log("No alerts found")
      }
    },
    async removeAlert(alert) {
      fetch('35.82.41.91:3000/remove-alert', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(alert)
      })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error('Error:', error));
    },
    async fetchDataCsv() {
      try {
        // Update the target URL to the endpoint of your Node.js backend server
        const targetUrl = 'http://35.82.41.91/:3000/api/data';
        const response = await fetch(targetUrl);
        if (!response.ok) throw new Error('Network response was not ok');
        this.fileContent = await response.text();

        const options = this.fileContent.split(',')

        // Populate yearly average dropdown
        const averages = options.filter( element => element.startsWith('20') )

        // Get averageYears from averages
        const averageYears = averages.map( element => element.split("_")[0] )
        const uniqueAverageYears = Array.from(new Set(averageYears));
        const dropdownYear = document.getElementById("dropdownYear");

        uniqueAverageYears.forEach(option => {
          const optionElement = document.createElement("option");
          optionElement.textContent = option;
          dropdownYear.appendChild(optionElement);
        });

        //fetch most recent file
        this.fetchFile(options[ options.length - 1 ])

        // Set disabled dates from data
        this.setDisabledDates()
      } catch (error) {
        console.error('There was a problem fetching the file:', error);
      }

    },
    async fetchFile(filename) {

      try {
        const targetUrl = `http://35.82.41.91:3000/api/geojson/${filename}`;
        const response = await fetch(targetUrl);
        if (!response.ok) throw new Error('Network response was not ok');
        const geojsonData = await response.json(); // Parse the GeoJSON data

        this.reloadMapOverlayHelper(geojsonData, 0);
        this.dataList = [filename];
      } catch (error) {
        console.error('There was a problem fetching the GeoJSON file:', error);
      }

    },
    async fetchFileMutliple(filename, index) {
      this.removeOldLayers();

      try {
        const targetUrl = `http://35.82.41.91:3000/api/geojson/${filename}`;
        const response = await fetch(targetUrl);
        if (!response.ok) throw new Error('Network response was not ok');
        const geojsonData = await response.json(); // Parse the GeoJSON data

        this.reloadMapOverlayHelper(geojsonData, index, false);
      } catch (error) {
        console.error('There was a problem fetching the GeoJSON file:', error);
      }

    },
    async downloadCurrentGeoJSON() {
      for( let index = 0; index < this.dataList.length; index++ )
      {
        let filename = this.dataList[index];
        console.log(`Attempting to download ${filename}`)
        try {
          const url = `http://35.82.41.91:3000/api/geojson/${filename}`;
          const response = await fetch(url);
          const data = await response.json();
          const blob = new Blob([JSON.stringify(data)], {type: 'application/json'});
          const downloadUrl = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = downloadUrl;
          a.download = filename;
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(downloadUrl);
          document.body.removeChild(a);
        } catch (error) {
          console.error('Failed to download GeoJSON', error);
        }

      }

    }

  },
  mounted() {
    mapboxgl.accessToken = 'pk.eyJ1IjoidW5saW1pdGVkZHJpcCIsImEiOiJjbHNqbDNyZHExbnhnMmttbmJzMGxnMHUyIn0._TP9MLLTlUfbizgm0jvYDw';
    // Get Data csv (list of all files avaliable)
    this.fetchDataCsv();
    // Create map
    const map = new mapboxgl.Map({
      container: 'map',
      style: 'mapbox://styles/unlimiteddrip/clsjl5pkn005b01r67tuvbga5',
      bounds: [
        [-159.567123, 16.994625],  // Southwest coordinates: [longitude, latitude]
        [-154.612488, 22.203054]   // Northeast coordinates: [longitude, latitude]
      ],

      maxBounds: [
        [-170, 17],  // Southwest coordinates: [longitude, latitude]
        [-140, 25]   // Northeast coordinates: [longitude, latitude]
      ],

      center: [-159, 16],
      maxZoom: 23,
      minZoom: 5,
    });

    // Load data
    map.on('load', () => {
      this.map = map; // Assigning map to a component property for future reference

      this.reloadMapOverlay(); // Initial load of map overlay
    });

    // Set default to January when the component is mounted
    this.filterByMonth(0);

    // Set month depending on where the slider is positioned
    this.$refs.slider.addEventListener('input', (e) => {
      const month = parseInt(e.target.value, 10);
      this.filterByMonth(month);
    });
  }
}


// function filterByMonth(month) {
//   const months = [
//       "January",
//       "February",
//       "March",
//       "April",
//       "May",
//       "June",
//       "July",
//       "August",
//       "September",
//       "October",
//       "November",
//       "December"
//     ]
//     // Set the label to the month
//     document.getElementById('month').textContent = months[month];
//   }

//   document.addEventListener("DOMContentLoaded", function() {
//     // Set default to January
//     filterByMonth(0);

//     // Set month depending on where the slider is positioned
//     document.getElementById('slider').addEventListener('input', (e) => {
//       const month = parseInt(e.target.value, 10);
//       filterByMonth(month);
//   });
// });



</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

@import url('https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-draw/v1.4.3/mapbox-gl-draw.css');

body {
  margin: 0;
  padding: 0;
}

#map-container {
  position: fixed;
  width: 100%;
  height: 100%;
}

#map {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 100%;
}

.map-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 25%;
  padding: 10px;
  margin: 10px;
  font: 12px/20px 'Helvetica Neue', Arial, Helvetica, sans-serif;
  background: white;
  border: 2.5px solid black;
  border-radius: 10px;
}


.map-overlay-item {
  margin: 10px;
}


.map-overlay-inner {
  background-color: #fff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  border-radius: 3px;
  padding: 10px;
  margin: 10px;
  border: 2.5px solid black;
}

.map-overlay h2 {
  line-height: 24px;
  margin: 0 0 10px;
}

.map-overlay .legend .bar {
  height: 10px;
  width: 100%;
  background: linear-gradient(to right, #313695, #009966, #d73027, #A020F0);
}

.map-overlay input {
  background-color: transparent;
  width: 100%;
  margin: 0;
  cursor: ew-resize;
}

.number-input-container {
  display: none;
  padding: 10px;
  background: #FFF;
  width: 200px;
}

.number-input-container input, .number-input-container button {
  width: 100%;
  border: 1px solid #000;
}

.number-input-container button {
  background-color: #007BFF;
  color: white;
  cursor: pointer;
}

.number-input-container button:hover {
  background-color: #0056b3;
}

footer {
  background-color: #283618;
  height: 10vh;
}


</style>

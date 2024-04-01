<template>
  <div id="map-container">
    <div id="map"></div>
  </div>
  <div class="map-overlay">

    <select id="dropdown" @change="updateDataList($event)"></select>
    <select id="dropdownYear" @change="updateYear($event)"></select>

    <div class="map-temp-info-container">
      <h2 class="temp-info" id="temp-info">55°F</h2>
    </div>

    <div class="map-overlay-inner">
    <h2 id="slider-text">Temperatures over 2023</h2>
    <label id="month"></label>
    <input id="slider" type="range" min="0" max="11" step="1" value="0" @change="updateDataListSlider($event)">
  </div>

  <div class="map-overlay-inner">
    <div id="legend" class="legend">
      <div class="bar"></div>
      <div>Celsius (c)</div>
    </div>
  </div>

    <VueDatePicker
      v-model="selectedDate"
      :highlighted="highlightedDates"
      @selected="dateSelected"
    />

  </div>
</template>

<script>
import mapboxgl from 'mapbox-gl';

export default {
  data() {
    return {
      dataList: [
      "data/2023_01_average.geojson"
      ],
      map: null,
      year: 2023,
      month: 1,
    };
  },
  methods: {
    updateDataList(event) {
      const selectedIndex = event.target.selectedIndex;
      const selectedValue = event.target.options[selectedIndex].value;
      this.dataList = ["data/" + selectedValue];
      this.fetchFile(selectedValue);
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
      if (this.month >=10 ){
        this.dataList = [`data/${this.year}_${this.month}_average.geojson`];
      }
      else {
        this.dataList = [`data/${this.year}_0${this.month}_average.geojson`];
      }
      this.reloadMapOverlay();
    },
    reloadMapOverlay() {

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
      this.dataList.forEach((data, index) => {
          this.reloadMapOverlayHelper(data, index);
      });
    },

    reloadMapOverlayHelper(geojsonData, index) {

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
            15, 50
          ],
          'circle-opacity': 0.4
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
    async fetchDataCsv() {
      try {
        // Update the target URL to the endpoint of your Node.js backend server
        const targetUrl = 'http://localhost:3000/api/data';
        const response = await fetch(targetUrl);
        if (!response.ok) throw new Error('Network response was not ok');
        this.fileContent = await response.text();

        // Populate dropdown with all files
        const dropdown = document.getElementById("dropdown");
        const options = this.fileContent.split(',')
        console.log(options)
        options.forEach(option => {
          const optionElement = document.createElement("option");
          optionElement.textContent = option;
          dropdown.appendChild(optionElement);
        });

      } catch (error) {
        console.error('There was a problem fetching the file:', error);
      }
    },
    async fetchFile(filename) {
      
      try {
        const targetUrl = `http://localhost:3000/api/geojson/${filename}`;
        const response = await fetch(targetUrl);
        if (!response.ok) throw new Error('Network response was not ok');
        const geojsonData = await response.json(); // Parse the GeoJSON data

        this.reloadMapOverlayHelper(geojsonData, 0); 
      } catch (error) {
        console.error('There was a problem fetching the GeoJSON file:', error);
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

    const dropdownYear = document.getElementById("dropdownYear");
    const optionsYear = [2023,2022,2021,2020,2019];

    optionsYear.forEach(option => {
      const optionElement = document.createElement("option");
      optionElement.textContent = option;
      dropdownYear.appendChild(optionElement);
    });
  }
}

const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
  ]

function filterByMonth(month) {
    // Set the label to the month
    document.getElementById('month').textContent = months[month];
  }

  document.addEventListener("DOMContentLoaded", function() {
    // Set default to January
    filterByMonth(0);

    // Set month depending on where the slider is positioned
    document.getElementById('slider').addEventListener('input', (e) => {
      const month = parseInt(e.target.value, 10);
      filterByMonth(month);
  });
});



</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  body { margin: 0; padding: 0; }

  div {
    display: block;
  }

  footer {
    background-color: #283618;
    height: 10vh;
  }

  #map-container{
    position: fixed;
    width: 100%;
    height: 100%;
  }
  #map { position: absolute; top: 0; bottom: 0; width: 100%; }


  .map-overlay {
    font: 12px/20px 'Helvetica Neue', Arial, Helvetica, sans-serif;
    position: absolute;
    width: 25%;
    bottom: 0;
    left: 0;
    padding: 10px
  }

  .map-overlay .map-overlay-inner {
  background-color: #fff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  border-radius: 3px;
  padding: 10px;
  margin-bottom: 10px;
  }

  .map-overlay h2 {
  line-height: 24px;
  display: block;
  margin: 0 0 10px;
  }

  .map-overlay .legend .bar {
  height: 10px;
  width: 100%;
  /* background: linear-gradient(to right, #fca107, #7f3121); */
  background: linear-gradient(to right, #313695, #009966, #d73027, #A020F0);
  }

  .map-overlay input {
  background-color: transparent;
  display: inline-block;
  width: 100%;
  position: relative;
  margin: 0;
  cursor: ew-resize;
  }

</style>

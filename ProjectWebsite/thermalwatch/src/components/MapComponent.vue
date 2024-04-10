<template>
  <div id="map-container">
    <div id="map"></div>
  </div>
    <div class = 'cal'>
    <!-- <Datepicker 
    circle
    show-clear-button
    v-model= "selectedDate"
    :disabled-start-date="disabledStartDate"
    :disabled-end-date="disabledEndDate" 
    lang="en"
    position = "top"
    @change = "dateSelected"
    >
    </Datepicker> -->
    <datepicker
      v-model="selected"
      :locale="locale"
      :upperLimit="to"
      :lowerLimit="from"
      :disabled-dates="highlightedDates"
      @update:modelValue="dateSelected"
    />
    
  </div>
  <div class="map-overlay">

    <!-- <select id="dropdown" @change="updateDataList($event)"></select> -->
    <select id="dropdownYear" @change="updateYear($event)"></select>

    <div class="map-temp-info-container">
      <h2 class="temp-info" id="temp-info">55°F</h2>
    </div>

    <div class="map-overlay-inner">
    <h2 id="slider-text">Temperatures over 2019</h2>
    <label id="month"></label>
    <input id="slider" type="range" min="0" max="11" step="1" value="0" @change="updateDataListSlider($event)">
  </div>

  <div class="map-overlay-inner">
    <div id="legend" class="legend">
      <div class="bar"></div>
      <div> Fahrenheit (f)</div>
    </div>
  </div>


  </div>
</template>

<script>
import mapboxgl from 'mapbox-gl';
import Datepicker from 'vue3-datepicker';
import { enUS } from 'date-fns/locale';

export default {
  data() {
    return {
      locale: enUS, 
      to: new Date(), //present day 
      from: new Date(2019, 0, 1), // January 1st, 2019
      highlightedDates: [],
      disabledDates: {
        dates: [
          new Date(2019, 0, 2), // Disabling specific dates; Jan 2, 2019
          new Date(2019, 1, 3)  // Feb 3, 2019. Remember, months are 0-indexed in JavaScript Dates
        ]
      },
      preventDisableDateSelection: true,
      selected: new Date(2019,0,1),
      dataList: [],
      map: null,
      year: 2023,
      month: 1,
    };
  },
  components: {
    Datepicker
  },
  methods: {
    updateDataList(event) {
      const selectedIndex = event.target.selectedIndex;
      const selectedValue = event.target.options[selectedIndex].value;
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
      let averageFilename = ""
      if (this.month >=10 ){
        averageFilename = `${this.year}_${this.month}_average.geojson`;
      }
      else {
        averageFilename = `${this.year}_0${this.month}_average.geojson`;
      }
      this.fetchFile(averageFilename);
    },
    dateSelected(newDate) {
      if( newDate )
      {
        // get date in form -> yyyymmdd
        const year = newDate.getFullYear();
        const month = String(newDate.getMonth() + 1).padStart(2, '0'); // getMonth() is zero-indexed
        const day = String(newDate.getDate()).padStart(2, '0');
        const date = `${year}${month}${day}`;

        // Get date data
        let files = this.getFilesFromDate(date)
  
        for(let index = 0; index < files.length; index++)
        {
          this.fetchFile(files[index])
        }
      }
    },
    getFilesFromDate(date)
    {
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
    async fetchDataCsv() {
      try {
        // Update the target URL to the endpoint of your Node.js backend server
        const targetUrl = 'http://localhost:3000/api/data';
        const response = await fetch(targetUrl);
        if (!response.ok) throw new Error('Network response was not ok');
        this.fileContent = await response.text();

        const options = this.fileContent.split(',')

        // Populate dropdown with all files
        // const dropdown = document.getElementById("dropdown");
        // options.forEach(option => {
        //   const optionElement = document.createElement("option");
        //   optionElement.textContent = option;
        //   dropdown.appendChild(optionElement);
        // });


        // Populate yearly average dropdown
        const averages = options.filter( element => element.startsWith('20') )

        // Get averageYears from averages
        const averageYears = averages.map( element => element.split("_")[0] )
        const uniqueAverageYears = Array.from(new Set(averageYears));

        console.log(uniqueAverageYears);

        const dropdownYear = document.getElementById("dropdownYear");

        uniqueAverageYears.forEach(option => {
          const optionElement = document.createElement("option");
          optionElement.textContent = option;
          dropdownYear.appendChild(optionElement);
        });

        //fetch most recent file
        this.fetchFile(options[ options.length - 1 ])

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

  .cal {
    position: relative; /* Set the position of the container */
    top: 565px; /* Adjust the top position */
    left: 10px; /* Adjust the left position */
    
  }

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

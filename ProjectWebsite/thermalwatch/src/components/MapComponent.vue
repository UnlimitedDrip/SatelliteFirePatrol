<template>
  <div id="map-container">
    <div id="map"></div>
  </div>
  <div class="map-overlay">

    <div class="map-temp-info-container">
      <h2 class="temp-info" id="temp-info">55°F</h2>
    </div>

    <div class="map-overlay-inner">
      <h2>Temperatures over 2023</h2>
      <label id="month"></label>
      <input id="slider" type="range" min="0" max="11" step="1" value="0">
    </div>

    <div class="map-overlay-inner">
      <div id="legend" class="legend">
        <div class="bar"></div>
        <div>Celsius (c)</div>
      </div>
    </div>

  </div>
</template>

<script>
import mapboxgl from 'mapbox-gl';

export default {
  data() {
    return {
      dataList: [
      "data/2022_01_average.geojson"
      ]
    };
  },
  mounted() {
    mapboxgl.accessToken = 'pk.eyJ1IjoidW5saW1pdGVkZHJpcCIsImEiOiJjbHNqbDNyZHExbnhnMmttbmJzMGxnMHUyIn0._TP9MLLTlUfbizgm0jvYDw';

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



    map.on('load', () => {
      for (const [index, dataName] of this.dataList.entries()) {
        const data = dataName;
        console.log(data);
        map.addSource('lst' + index, {
          type: 'geojson',
          data: data
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
              0, '#0000FF',
              40, '#00FF00',
              75, '#FF0000',
            ],
            'circle-radius': [
              'interpolate',
              ['linear'],
              ['zoom'],
              5, .3,
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
          const coordinates = e.features[0].geometry.coordinates.slice();
          const temperature = e.features[0].properties.LST;
          console.log(coordinates)
          console.log(temperature)

          document.getElementById("temp-info").textContent = temperature.toFixed(2) + "°F";

          /*
          popup.setLngLat(coordinates)
            .setHTML(`Temperature: ${temperature}°C`)
            .addTo(map);
          */
        });

        // Mouse leave event




      }
    })
  }
}
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

  #map { position: absolute; top: 0; bottom: 0; width: 100%; }
  #map-container{
    position: fixed;
    width: 100%;
    height: 100%;
  }

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
  background: linear-gradient(to right, #fca107, #7f3121);
  }

  .map-overlay input {
  background-color: transparent;
  display: inline-block;
  width: 100%;
  position: relative;
  margin: 0;
  cursor: ew-resize;
  }

  .map-temp-info-container {
    background-color: #fff;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    border-radius: 3px;
    padding: 10px;
    margin-bottom: 10px;
  }

  .temp-info {
    font-size: 30px;
  }

</style>

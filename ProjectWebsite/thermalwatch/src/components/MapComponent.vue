<template>

  <header id="header">
    <div class="header-logo-container">
      <img src="data/Sateillite_Fire_Patrol-logos_white.png" alt="logo" class="header-logo-image">
    </div>

    <nav id="nav-bar" class="header-nav-container">

      <ul class="header-list">
        <li><a class="nav-link" href="">About Us</a></li>
        <li><a class="nav-link" href="">Account</a></li>
        <li><a class="nav-link" href="">Resources</a></li>
      </ul>

    </nav>

  </header>

  <div id="map"></div>
  <div class="map-overlay top">
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
        "data/ECOSTRESS_L2_LSTE_31734_012_20240210T031946_0601_01.geojson",
        "data/ECOSTRESS_L2_LSTE_31667_005_20240205T190358_0601_01.geojson"//,
        //"data/ECOSTRESS_L2_LSTE_31673_012_20240206T045454_0601_01.geojson"
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
              0, '#313695',
              75, '#009966',
              150, '#d73027'
            ],
            'circle-radius': [
              'interpolate',
              ['linear'],
              ['zoom'],
              5, 1,
              8, 2,
              10, 10,
              11, 20,
              15, 100
            ],
            'circle-opacity': 0.4
          }
        });
      }
    })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  body { margin: 0; padding: 0; }



  header {
    position: fixed;
    top: 0;
    width: 100vw;
    height: 15vh;
    display: flex;
    padding: 0px 25px;
    justify-content: space-around;
    align-items: center;
    background-color: #283618;
    color: #FEFAE0;
  }

  div {
    display: block;
  }

  footer {
    background-color: #283618;
    height: 10vh;
  }


  .header-logo-container{
    width: 50vw;
    display: flex;
    padding: 1rem 0rem 1rem 2rem;
  }

  .header-logo-image {
    display: inline-block;
    padding-right: 1rem;
    font-size: 1.5rem;
    text-rendering: auto;
    padding-top: .75rem;
    height: 100px;
    width: 200px;
  }

  .header-list {
    list-style: none;
    min-height: 75px;
    padding-top: .4rem;
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding-right: 2rem;
  }


  .header-nav-container {
    width: 50vw;
    padding: 1rem 0rem 1rem 2rem;
  }

  .nav-link {
    border: none;
    font-family: 'Helvetica Neue', Arial, Helvetica, sans-serif;
    font-size: 3rem;
    text-decoration: none;
    color: #FEFAE0;
  }

  .nav-link:hover {
    border: none;
    color: #000;
  }


  #map { position: absolute; top: 15vh; bottom: 0; width: 100%; }



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

</style>

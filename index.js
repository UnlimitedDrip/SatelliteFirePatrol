latitude = 35.2902
longitude = -111.6688
zoom = 10

$(document).ready(function () {
  // This function is executed when the document is fully loaded and ready to be manipulated with JavaScript.

  mapboxgl.accessToken = 'pk.eyJ1Ijoiem1oNDciLCJhIjoiY2xudDQ5Z2k3MDBhbTJqbzBtMGpzMDVkaSJ9.WnBcSLXLTOyVIiC4tc_IpQ';
  // Set your Mapbox access token, allowing you to access Mapbox's services and maps.

  // Initialize Mapbox
  var map = new mapboxgl.Map({
      container: 'map', // Container ID
      style: 'mapbox://styles/mapbox/satellite-v9',
      // style: 'mapbox://styles/mapbox/dark-v9',
      // Set the initial bounds to the bounding box
      bounds: [
          // [128.493896, 40.596863], // Southwest coordinates
          // [134.655624, 45.728336]  // Northeast coordinates
          // "boxes": ["16.994625 -159.567123 22.203054 -154.612488"],
          [-159.567123, 16.994625],  // Southwest coordinates: [longitude, latitude]
          [-154.612488, 22.203054]   // Northeast coordinates: [longitude, latitude]
      ],
      // center: [-111.6688, 35.2902],
      center: [-159, 16],
      zoom: 10
  });

  map.on('load', () => {

    dataList = ["ECOSTRESS_L2_LSTE_08603_010_20200111T171110_0601_01.geojson", "ECOSTRESS_L2_LSTE_08719_001_20200119T040945_0601_01.geojson", "ECOSTRESS_L2_LSTE_08780_001_20200123T023443_0601_01.geojson", "ECOSTRESS_L2_LSTE_08902_001_20200130T232741_0601_01.geojson", "ECOSTRESS_L2_LSTE_09024_001_20200207T202041_0601_01.geojson", "ECOSTRESS_L2_LSTE_09030_011_20200208T061207_0601_01.geojson", "ECOSTRESS_L2_LSTE_09045_008_20200209T052434_0601_01.geojson", "ECOSTRESS_L2_LSTE_09091_010_20200212T043833_0601_01.geojson", "ECOSTRESS_L2_LSTE_09106_013_20200213T035100_0601_01.geojson", "ECOSTRESS_L2_LSTE_09146_001_20200215T171336_0601_01.geojson"]

    count = -1;
    for(var dataName of dataList){
      count++;
      data = "ProcessedData/" + dataName
      map.addSource('lst'+count, {
        type: 'geojson',
        // Use a URL for the value for the `data` property.
        // data: 'https://docs.mapbox.com/mapbox-gl-js/assets/earthquakes.geojson'
        data: data
      });

      map.addLayer({
        'id': 'lst-heatmap'+count,
        'type': 'heatmap',
        'source': 'lst'+count,
        'maxzoom': 15,
        'paint': {
          // Increase the heatmap weight based on frequency and property magnitude
          'heatmap-weight': [
            'interpolate',
            ['linear'],
            ['get', 'LST'],
            7000, 0,
            19000, 1
          ],
          // Color ramp for the heatmap.
          // This example uses a heatmap color ramp to visualize the LST data
          'heatmap-color': [
            'interpolate',
            ['linear'],
            ['heatmap-density'],
            0, 'rgba(33,102,172,0)',
            0.2, '#ffffb2',
            0.4, '#fed976',
            0.6, '#feb24c',
            0.8, '#fd8d3c',
            1, '#fc4e2a'
          ],
          // Adjust the heatmap radius by zoom level
          'heatmap-radius': [
            'interpolate',
            ['linear'],
            ['zoom'],
            0, 2,
            15, 20
          ],
          // Transition from heatmap to circle layer by zoom level
          'heatmap-opacity': [
            'interpolate',
            ['linear'],
            ['zoom'],
            14, 1,
            15, 0
          ],
        }
      });
    }


  });


});

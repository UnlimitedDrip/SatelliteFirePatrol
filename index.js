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
          [-159.567123, 16.994625],  // Southwest coordinates: [longitude, latitude]
          [-154.612488, 22.203054]   // Northeast coordinates: [longitude, latitude]
      ],
      // center: [-111.6688, 35.2902],
      center: [-159, 16],
      zoom: 10
  });

  map.on('load', () => {

    console.log("AH")
    dataList = ["ECOSTRESS_L2_LSTE_08780_001_20200123T023443_0601_01.geojson"]
    // dataList = ["ECOSTRESS_L2_LSTE_08603_010_20200111T171110_0601_01.geojson", "ECOSTRESS_L2_LSTE_08719_001_20200119T040945_0601_01.geojson", "ECOSTRESS_L2_LSTE_08780_001_20200123T023443_0601_01.geojson", "ECOSTRESS_L2_LSTE_08902_001_20200130T232741_0601_01.geojson", "ECOSTRESS_L2_LSTE_09024_001_20200207T202041_0601_01.geojson", "ECOSTRESS_L2_LSTE_09030_011_20200208T061207_0601_01.geojson", "ECOSTRESS_L2_LSTE_09045_008_20200209T052434_0601_01.geojson", "ECOSTRESS_L2_LSTE_09091_010_20200212T043833_0601_01.geojson", "ECOSTRESS_L2_LSTE_09106_013_20200213T035100_0601_01.geojson", "ECOSTRESS_L2_LSTE_09146_001_20200215T171336_0601_01.geojson"]

    count = -1;
    for(var dataName of dataList){
      console.log("HI")
      count++;
      data = "ProcessedData/" + dataName
      console.log(data)
      map.addSource('lst'+count, {
        type: 'geojson',
        // Use a URL for the value for the `data` property.
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
            0, 0,
            100, 1
          ],
          // Color ramp for the heatmap.
          // This example uses a heatmap color ramp to visualize the LST data
          'heatmap-color': [
            'interpolate',
            ['linear'],
            ['heatmap-density'],
              0, 'rgba(33,102,172,0)',    // Transparent at the lowest density
              0.1, '#ade1f9',             // Light blue for very low density
              0.2, '#00ffcc',             // Aqua for low density
              0.3, '#00ff00',             // Bright green for low-mid density
              0.4, '#ccff00',             // Lime green for mid-low density
              0.5, '#ffff00',             // Yellow for mid density
              0.6, '#ffcc00',             // Gold for mid-high density
              0.7, '#ff8c00',             // Orange for high-mid density
              0.8, '#ff4500',             // Orange-red for high density
              0.9, '#ff0000',             // Red for very high density
              1, '#6e0229'                // Deep maroon for the highest density
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
            14, .5,
            15, 0
          ],
        }
      });
    }
  });
});

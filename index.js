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

    dataList = [ "ECOSTRESS_L2_LSTE_08719_001_20200119T040945_0601_01.geojson", "ECOSTRESS_L2_LSTE_08786_001_20200123T122449_0601_01.geojson"]
    // dataList = [ "ECOSTRESS_L2_LSTE_08506_001_20200105T103113_0601_01.geojson"]

    count = -1;
    for(var dataName of dataList){
      count++;
      data = "ProcessedData/" + dataName
      console.log(data)
      map.addSource('lst'+count, {
        type: 'geojson',
        // Use a URL for the value for the `data` property.
        data: data
      });

      map.addLayer({
        'id': 'temperature-circles' + count,
        'type': 'circle',
        'source': 'lst' + count,
        'paint': {
          // Use step expressions with three steps to color circles based on temperature property
          'circle-color': [
            'interpolate',
            ['linear'],
            ['get', 'LST'], // Replace 'temperature' with your data's temperature property
            0, '#313695',           // Deep blue for the lowest temperature (0)
            75, '#009966',          // Green for medium temperatures (75)
            150, '#d73027'          // Red for the highest temperatures (150)
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

      // end of temp layer function
      });

      // Create a new popup instance
      var popup = new mapboxgl.Popup({
        closeButton: false,
        closeOnClick: false
      });

      map.on('mousemove', 'temperature-circles'+count, function(e) {
        // Change the cursor style as a UI indicator.
        map.getCanvas().style.cursor = 'pointer';

        var coordinates = e.features[0].geometry.coordinates.slice();
        var temperature = e.features[0].properties.LST.toFixed(2); // Replace 'temperature' with the field name in your data

        // Populate the popup and set its coordinates based on the feature found.
        popup.setLngLat(coordinates)
          .setHTML('Temperature: ' + temperature + '°F') // Modify to match your content
          .addTo(map);
      });

      map.on('mouseleave', 'temperature-circles', function() {
        map.getCanvas().style.cursor = '';
        popup.remove();
      });


    // end of data for loop
    }

  // end of on load funciton
  });

// end of document ready function
});

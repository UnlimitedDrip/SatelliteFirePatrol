latitude = 35.2902
longitude = -111.6688
zoom = 10

$(document).ready(function () {
// This function is executed when the document is fully loaded and ready to be manipulated with JavaScript.

    mapboxgl.accessToken = 'pk.eyJ1IjoidW5saW1pdGVkZHJpcCIsImEiOiJjbHNqbDNyZHExbnhnMmttbmJzMGxnMHUyIn0._TP9MLLTlUfbizgm0jvYDw';
    // Set your Mapbox access token, allowing you to access Mapbox's services and maps.

    // Initialize Mapbox
    const map = new mapboxgl.Map({

    container: 'map', // Container ID
    style: 'mapbox://styles/unlimiteddrip/clsjl5pkn005b01r67tuvbga5',
    // style: 'mapbox://styles/unlimiteddrip/clsjl5pkn005b01r67tuvbga5'
    // style: 'mapbox://styles/mapbox/dark-v9',
    // Set the initial bounds to the bounding box
    bounds: [
        // [128.493896, 40.596863], // Southwest coordinates
        // [134.655624, 45.728336]  // Northeast coordinates
        // "boxes": ["16.994625 -159.567123 22.203054 -154.612488"],
        [-159.567123, 16.994625],  // Southwest coordinates: [longitude, latitude]
        [-154.612488, 22.203054]   // Northeast coordinates: [longitude, latitude]
    ],
    
    //restrict user to hawaii
    
    maxBounds: [
        // [128.493896, 40.596863], // Southwest coordinates
        // [134.655624, 45.728336]  // Northeast coordinates
        // "boxes": ["16.994625 -159.567123 22.203054 -154.612488"],
        [-170, 17],  // Southwest coordinates: [longitude, latitude]
        [-140, 25]   // Northeast coordinates: [longitude, latitude]
    ],
    
    // center: [-111.6688, 35.2902],
    center: [-159, 16],

    //max and min zooms
    maxZoom: 23,
    minZoom: 5,
    });

//controls
const nav = new mapboxgl.NavigationControl();
map.addControl(nav, "top-right");

});

map.on('style.load', () => {
    map.addSource('mapbox-dem', {
        'type': 'terrain',
        'url': 'mapbox://mapbox.mapbox-terrain-dem-v1',
        'tileSize': 512,
        'maxzoom': 14,
    });

    // add the DEM source as a terrain layer with exaggerated height
    map.setTerrain({ 'source': 'mapbox-dem', 'exaggeration': 2 });
});

const months = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
];

function filterBy(month) {
    const filters = ['==', 'month', month];
    map.setFilter('earthquake-circles', filters);
    map.setFilter('earthquake-labels', filters);

    // Set the label to the month
    document.getElementById('month').textContent = months[month];
}

map.on('load', () => {
    // Data courtesy of http://earthquake.usgs.gov/
    // Query for significant earthquakes in 2015 URL request looked like this:
    // http://earthquake.usgs.gov/fdsnws/event/1/query
    //    ?format=geojson
    //    &starttime=2015-01-01
    //    &endtime=2015-12-31
    //    &minmagnitude=6'
    //
    // Here we're using d3 to help us make the ajax request but you can use
    // Any request method (library or otherwise) you wish.
    d3.json(
        'https://docs.mapbox.com/mapbox-gl-js/assets/significant-earthquakes-2015.geojson',
        jsonCallback
    );
});

function jsonCallback(err, data) {
    if (err) {
        throw err;
    }

    // Create a month property value based on time
    // used to filter against.
    data.features = data.features.map((d) => {
        d.properties.month = new Date(d.properties.time).getMonth();
        return d;
    });

    map.addSource('earthquakes', {
        'type': 'geojson',
        data: data
    });

    map.addLayer({
        'id': 'earthquake-circles',
        'type': 'circle',
        'source': 'earthquakes',
        'paint': {
            'circle-color': [
                'interpolate',
                ['linear'],
                ['get', 'mag'],
                6,
                '#FCA107',
                8,
                '#7F3121'
            ],
            'circle-opacity': 0.75,
            'circle-radius': [
                'interpolate',
                ['linear'],
                ['get', 'mag'],
                6,
                20,
                8,
                40
            ]
        }
    });

    map.addLayer({
        'id': 'earthquake-labels',
        'type': 'symbol',
        'source': 'earthquakes',
        'layout': {
            'text-field': ['concat', ['to-string', ['get', 'mag']], 'm'],
            'text-font': ['Open Sans Bold', 'Arial Unicode MS Bold'],
            'text-size': 12
        },
        'paint': {
            'text-color': 'rgba(0,0,0,0.5)'
        }
    });

    // Set filter to first month of the year
    // 0 = January
    filterBy(0);

    document.getElementById('slider').addEventListener('input', (e) => {
        const month = parseInt(e.target.value, 10);
        filterBy(month);
    });
}

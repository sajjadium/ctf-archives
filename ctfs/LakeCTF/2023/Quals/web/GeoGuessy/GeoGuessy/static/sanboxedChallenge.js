function loadMap() {
    map = new OpenLayers.Map({
        div: "mapdiv"
      });
      var lonLat = new OpenLayers.LonLat( 0,0 )
      .transform(
        new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
        map.getProjectionObject() // to Spherical Mercator Projection
      );
      map.addLayer(new OpenLayers.Layer.OSM("OpenStreetMap", ['https://a.tile.openstreetmap.org/${z}/${x}/${y}.png','https://b.tile.openstreetmap.org/${z}/${x}/${y}.png','https://c.tile.openstreetmap.org/${z}/${x}/${y}.png'],null));
      map.setCenter (lonLat, 2);
      markers = new OpenLayers.Layer.Markers( "Markers" );
      map.addLayer(markers);
      markers.addMarker(new OpenLayers.Marker(lonLat));
      map.events.register('click', new OpenLayers.Feature(), function(e){
        var lonlat = map.getLonLatFromPixel(e.xy);
        markers.clearMarkers();
        markers.addMarker(new OpenLayers.Marker(lonlat));
        var toProjection = new OpenLayers.Projection("EPSG:4326");
        lonlat = lonlat.transform(map.getProjectionObject(), toProjection);
        window.top.postMessage({latitude:lonlat.lat,longitude:lonlat.lon},"*")
      })
}

function loadLib() {
var script = document.createElement("script");
const urlParams = new URLSearchParams(window.location.search);
const libVersion = urlParams.get('ver');
script.src = "/static/OpenLayers"+libVersion+".js";
script.onload = loadMap
document.head.appendChild(script);
}


//check is inside iframe of same domain
if (window.self !== window.top && location.origin == window.top.location.origin) {
    loadLib();
}
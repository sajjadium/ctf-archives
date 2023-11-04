function camerastart() {
    captureButton.className = "show"
    camerastartButton.className = ""
      // Check for getUserMedia support
      navigator.getUserMedia = (navigator.getUserMedia ||
                                navigator.webkitGetUserMedia ||
                                navigator.mozGetUserMedia ||
                                navigator.msGetUserMedia);
  
      if (navigator.getUserMedia) {
          // Request access to the webcam
          navigator.getUserMedia({ video: true },
              function(stream) {
                  // Display the webcam feed in the video element
                  var video = document.getElementById("video");
                  video.srcObject = stream;
  
                  // Enable the capture button
                  var captureButton = document.getElementById("captureButton");
                  captureButton.disabled = false;
  
                  // Handle the click event on the capture button
                  captureButton.addEventListener("click", function() {
                      // Capture a photo and display it on the canvas
                      var canvas = document.getElementById("canvas");
                      var context = canvas.getContext("2d");
                      context.drawImage(video, 0, 0, canvas.width, canvas.height);
                      confirmButton.className = "show"
                      window.img = canvas.toDataURL().split(',')[1]
                  });
              },
              function(error) {
                  console.error("Error accessing the webcam: ", error);
              }
          );
      } else {
          console.error("getUserMedia not supported");
      }
  }
  async function confirm() {
    takepicture.className = ""
    OpenLayersVersion = document.getElementById("OpenLayersVersion").value
    winText = document.getElementsByName("winText")[0].value
    body = {latitude,longitude,img,OpenLayersVersion,winText}
    await fetch("/createChallenge", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json"
              },
              body: JSON.stringify(body)
          }).then(res => res.json()).then(res => {
              if(res != "no"){
                  window.duelID = res
              } else {
                  alert("plz stop hakk")
              }
          })
    duel.className = "show"
  }

  function createNewChall(){
    createNewChallBut.className = ""
  if (document.getElementById("isPremium").innerText == "1") {
    challMetadata.className = "show"  
  } else {
    getGeolocation.className = "show"
  }
  }
  function endMetadata(){
    challMetadata.className = ""
    getGeolocation.className = "show"
  }

  function challengeUser(){
    username = document.getElementsByName("username")[0].value
    body = {username, duelID}
    fetch("/challengeUser", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    }).then(res => res.json()).then(res => {
        if(res == "yes ok"){
          x.innerHTML = "challenge sent"
        } else {
            x.innerHTML = "error: "+res
        }
    })
}

const x = document.getElementById("demo");

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition,(err) => console.error(err), {"enableHighAccuracy":true});
  } else { 
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function fakeLocation() {
    showPosition({coords:{latitude:Math.random()*180-90,longitude:Math.random()*360-180}},2)
}

function showPosition(position,zoom=16) {
    fakeBut.remove()
    realBut.remove()
    mapdiv.className = "show"
    takepicture.className = "show"
    window.latitude = position.coords.latitude
    window.longitude = position.coords.longitude
  x.innerHTML = "Latitude: " + position.coords.latitude + 
  "<br>Longitude: " + position.coords.longitude;
  map = new OpenLayers.Map({
    div: "mapdiv",
    controls: [new OpenLayers.Control.Attribution()] // removing controls in hope that it will reduce the load on OSM servers
  });
  map.addLayer(new OpenLayers.Layer.OSM("OpenStreetMap", ['https://a.tile.openstreetmap.org/${z}/${x}/${y}.png','https://b.tile.openstreetmap.org/${z}/${x}/${y}.png','https://c.tile.openstreetmap.org/${z}/${x}/${y}.png'],null));
  var lonLat = new OpenLayers.LonLat( position.coords.longitude, position.coords.latitude )
        .transform(
          new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
          map.getProjectionObject() // to Spherical Mercator Projection
        );
  var markers = new OpenLayers.Layer.Markers( "Markers" );
  map.addLayer(markers);
  markers.addMarker(new OpenLayers.Marker(lonLat));
  map.setCenter (lonLat, zoom);
}

window.onload = () => {
realBut.onclick = getLocation
fakeBut.onclick = fakeLocation
challengeUserButton.onclick = challengeUser
endMetadataButton.onclick = endMetadata
happycatButton.onclick = happycat
camerastartButton.onclick = camerastart
confirmButton.onclick = confirm
createNewChallBut.onclick = createNewChall
createNewChallBut.className = "show"
camerastartButton.className = "show"
}
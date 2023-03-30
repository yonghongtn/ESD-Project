let map, infoWindow;
function initMap() {
    const target = { lat: 1.2966159339244079, lng: 103.85023289853143 }
    // Initializes the map, and centers it at target location (parking location)
    map = new google.maps.Map(document.getElementById("map"), {
    zoom: 17,
    center: target,
    });
    // Retrieves the user's current location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude,
            };
            // Creates the first marker, positioned at at user's current location, if the user
            // allows location sharing
            const usermarker = new google.maps.Marker({
                position: pos,
                map: map,
                });
            // Centers the map at user's current location
            // If the user does not allow location sharing, the map will
            // remain centered at target location
            map.setCenter(pos);
          },
        );
      }
    // Creates the second marker, positioned at target location
    const image = "images/vehicle.png"
    const targetmarker = new google.maps.Marker({
    position: target,
    map: map,
    icon: image,
    });
}
window.initMap = initMap;

// this code is still incomplete, it should retrieve lat and lng from database/system memory
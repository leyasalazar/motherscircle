'use strict';

// We use a function declaration for initMap because we actually *do* need
// to rely on value-hoisting in this circumstance.

function initMap() {
  const map = new google.maps.Map(document.querySelector('#map'), {
    // center: {
    //   lat: 44.977753,
    //   lng: -93.2650108
    // },
    // zoom: 8,
  });
  // Get the location through the data.

  const address = document.querySelector('#address').textContent

  const geocoder = new google.maps.Geocoder();
  geocoder.geocode({ address: address }, (results, status) => {
    if (status === 'OK') {
      // Get the coordinates of the event's location
      const eventLocation = results[0].geometry.location;

      // Create a marker
      new google.maps.Marker({
        position: eventLocation,
        map,
      });

      // Zoom in on the geolocated location
      map.setCenter(eventLocation);
      map.setZoom(18);

    } else {
      alert(`Geocode was unsuccessful for the following reason: ${status}`);
    }
  })
}

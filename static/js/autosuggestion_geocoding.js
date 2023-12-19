document.addEventListener('DOMContentLoaded', function() {
    var startPosInput = document.getElementById('startPos');    // the user's starting position is obtained from the form
    var endPosInput = document.getElementById('endPos');        // the user's destination is obtained from the form
    var endLatInput = document.getElementById('endLat');        // the latitude of the user's destination is obtained from the form
    var endLngInput = document.getElementById('endLng');        // the longitude of the user's destination is obtained from the form

    // initializes the autocomplete service for the destination position input
    var autocomplete = new google.maps.places.Autocomplete(endPosInput);

    // callbanck call when the destination position is selected by the user
    autocomplete.addListener('place_changed', function() {

        var place = autocomplete.getPlace();    // the details of the place selected by the user are obtained

        // the coordinates of the destination place are obtained
        var endLat = place.geometry.location.lat();
        var endLng = place.geometry.location.lng();

        // updating hidden inputs with destination coordinates
        endLatInput.value = endLat;
        endLngInput.value = endLng;
    });

    // if the browser supports geolocation
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            
            // the user's location is recovered (latitude and longitude)
            var lat = position.coords.latitude;
            var lng = position.coords.longitude;

            var geocoder = new google.maps.Geocoder();        // creation of a geocoder object for converting coordinates into addresses
            var latLng = new google.maps.LatLng(lat, lng);    // initialization of a pair of the type (latitude, longitude)

            // reverse geocoding is then performed, coordinates -> address   
            geocoder.geocode({ 'location': latLng }, function(results, status) {
                if (status === 'OK') {  // if the geocoding request was successful
                    if (results[0]) {   // if there are any results in the answer
                        // updates the starting input field with the newly converted current address
                        startPosInput.value = results[0].formatted_address;

                        // hidden inputs are updated with the new coordinates just recovered 
                        document.getElementById('startLat').value = lat;
                        document.getElementById('startLng').value = lng;
                    } else {
                        // otherwise an error message is shown as there is no address found
                        console.error('Nessun risultato trovato per la geocodifica inversa.');
                    }
                } else {
                    // otherwise a geocoding error message is shown
                    console.error('Errore nella geocodifica inversa:', status);
                }
            });
        }, function(error) {
            // otherwise geolocation error message is shown
            console.error('Errore nella geolocalizzazione:', error.message);
        });
    } else {
        // otherwise an error message is shown because geolocation is not supported by the browser
        console.error('La geolocalizzazione non è supportata dal browser.');
    }
});
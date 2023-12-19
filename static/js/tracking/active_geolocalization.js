function getLocation() {
    // if the geolocalization in available
    if (navigator.geolocation) {
      // make a call to obtain the user's current geographical location through his device.
      navigator.geolocation.getCurrentPosition(showPosition);
    } else {
      // error message is shown
      alert("Geolocation is not supported by this browser.")
    }
  }

  // function to show the user's location
  function showPosition(position) {
    // the user's starting address is retrieved
    var startPosInput = document.getElementById('startPos');
    const idUtente = getUtenteID();  // the user ID is also retrieved

    const now = new Date(); // the Current Date object is retrieved

    // extraction of date and time information
    const year = now.getFullYear();     // the current year is retrieved
    const month = now.getMonth() + 1;   // the current month is retrieved
    const day = now.getDate();          // the current day is retrieved
    const hours = now.getHours();       // the current hour is retrieved
    const minutes = now.getMinutes();   // the current minute is retrieved
    const seconds = now.getSeconds();   // the current second is retrieved

    // the date and time are then formatted as a string
    const formattedDateTime = `${year}-${month < 10 ? '0' + month : month}-${day < 10 ? '0' + day : day} ${hours < 10 ? '0' + hours : hours}:${minutes < 10 ? '0' + minutes : minutes}:${seconds < 10 ? '0' + seconds : seconds}`;

    console.log(formattedDateTime); // debug

    // data structure to return with some information such as
    let myPosition = {
      "idUtente": idUtente,             // idUtente
      "lat": position.coords.latitude,  // latitude
      "lon": position.coords.longitude, // longitude
      "timestamp": formattedDateTime    // timestamp of the sampling
    }

    // the user's location is recovered (latitude and longitude)
    var lat = position.coords.latitude;
    var lng = position.coords.longitude;

    // hidden inputs are updated with the new coordinates just recovered 
    document.getElementById('startLat').value = lat;
    document.getElementById('startLng').value = lng;

    var geocoder = new google.maps.Geocoder();        // creation of a geocoder object for converting coordinates into addresses
    var latLng = new google.maps.LatLng(lat, lng);    // initialization of a pair of the type (latitude, longitude)

    // reverse geocoding is then performed, coordinates -> address
    geocoder.geocode({ 'location': latLng }, function(results, status) {
        if (status === 'OK') {  // if the geocoding request was successful
            if (results[0]) {   // if there are any results in the answer
                // updates the starting input field with the newly converted current address
                startPosInput.value = results[0].formatted_address;
            } else {
                // otherwise an error message is shown as there is no address found
                console.error('Nessun risultato trovato per la geocodifica inversa.');
            }
        } else {
            // otherwise a geocoding error message is shown
            console.error('Errore nella geocodifica inversa:', status);
        }
    });

    ws.send(JSON.stringify(myPosition)) // the object with the user's location is sent to the websocket
    console.log(myPosition) // debug
  }

  // function to keep the websocket active
  function beAlive() {
    const idUtente = getUtenteID(); // the user ID is obtained
    // a dummy object is sent to keep the websocket active
    ws.send(JSON.stringify({ "wakeup": 1, "idUtente": idUtente }));
  }

  // function to get user ID from frontend via saved cookie
  function getUtenteID() {
    // the user ID is retrieved from the frontend through the corresponding cookie, called 'idUtente'
    const idUtente = document.cookie              // returns the string containing all the cookies associated with the document
      .split('; ')                                // splits the cookie string into an array of strings separated by ";", so that each element of the array represents a cookie.
      .find(row => row.startsWith('idUtente='))   // searches for the element in the cookie array that begins with the string 'idUtente='
      ?.split('=')[1];                            // if a cookie starting with 'idUtente=' is found, splits the cookie into two parts using '=' as a delimiter and returns the second part (i.e. the user ID)
  
    // returns the user's ID, or a default value if it is not present
    return idUtente || 'NULL';
  }

  let myTimer //  variable timer to get the location periodically
  let hb      //  variable to keep the websocket active
  let ws      //  variable to use the websocket
  
  function init_tracking() {

    // initialization and connection to the websocket
    ws = new WebSocket("ws://localhost:9001/");

    /* event handlers definitions */

    // event handler for opening the websocket
    ws.onopen = function() {
      console.log("onopen") // debug
      getLocation();                            // initial capture of the user's location
      myTimer=setInterval(getLocation, 5000);   // interval definition to get the user's location periodically
      hb=setInterval(beAlive, 1000);            // interval definition to keep the websocket active
    };
    
    // event handler for receiving websocket messages
    ws.onmessage = function(e) {
      // message sent at the websocket
      console.log("onmessage: " + e.data)
    };
    
    // event handler for closing the websocket
    ws.onclose = function() {
      console.log("onclose")  // closing message of the websocket
    };

    // event handler for receiving errors from the websocket
    ws.onerror = function(e) {
      console.log(e)
    };   
  }

  // function to close the connection to the websocket
  function onCloseClick() {
    myTimer.stop()  // stop the timer to periodically send the location
    hb.stop()       // stop the timer to send keep the websocket active
    ws.close()      // close the websocket
  }
  
  
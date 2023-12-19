
// function to check the trip status and show/hide the button to end the trip
function controllaStatoViaggio(tripId) {
    // ======================== TRIPS ==================================
    
    var pulsanteId = 'ending_' + tripId;  // constructs the button's unique ID

    // select the element with the class "badge" specific to this trip
    var elementoStato = document.querySelector('#viaggio_' + tripId + ' .badge');

    // if the item is present and the status is 'Concluso'
    if (elementoStato && elementoStato.innerText.trim() === 'Concluso') {
      // retrieve the item by id
      var elementoPulsante = document.getElementById(pulsanteId);
      if (elementoPulsante) { // if found
        // hides the specific button for this trip
        elementoPulsante.classList.add('hide-button');
      }
    } else { 
      // retrieve the item by id
      var elementoPulsante = document.getElementById(pulsanteId);
      if (elementoPulsante) { // if found
        // show the specific button for this trip
        elementoPulsante.classList.remove('hide-button');
      }
    }
    // ====================================================================
}


// function to check the ride status and show/hide the step removal button
function controllaStatoPassaggio(rideId) {
    // ========================= PASSAGGI =================================

    var pulsanteId = 'delRide_' + rideId; // constructs the button's unique ID

    // select the element with the class "badge" specific to this ride
    var elementoStato = document.querySelector('#ride_' + rideId + ' .badge');

    //console.log('pulsanteId:', pulsanteId);
    //console.log('elementoStato:', elementoStato);

    // if the item is present and the status is 'Accettato'
    if (elementoStato && elementoStato.innerText.trim() === 'Accettato') {
        // nasconde il pulsante specifico per questo ride, se trovato
        // console.log("Il passaggio NON può essere eliminato");

        // retrieve the item by id
        var elementoPulsante = document.getElementById(pulsanteId);

        // console.log('elementoPulsante:', elementoPulsante);

        if (elementoPulsante) { // if found
            // hides the specific button for this ride
            elementoPulsante.classList.add('hide-button');
        }
    } else {
        // console.log("Il passaggio può essere eliminato");

        // retrieve the item by id
        var elementoPulsante = document.getElementById(pulsanteId);

        // console.log('elementoPulsante:', elementoPulsante);

        if (elementoPulsante) { // if found
            // show the specific button for this ride
            elementoPulsante.classList.remove('hide-button');
        }
    }
    // ====================================================================
}
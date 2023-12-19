// asynchronous call to make a ride request
function requestRide(idViaggio) {
    if (confirm("Sei sicuro di voler richiedere un passaggio per questo viaggio?")) {
      // make the AJAX call to request the ride
      $.ajax({
        url: "/request_ride/" + idViaggio,    // url to which to make the request
        method: "POST",                       // request method, in this case POST
        data: { idViaggio: idViaggio },       // request data
        success: function(response) {
          // if the book request was successful, the user interface is updated
          console.log("Viaggio prenotato con successo!");
        },
        error: function(error) {    // in case of an error during the request
          // an alert containing the error is displayed and displayed in the console
          console.error("Errore durante la prenotazione del viaggio:", error);
          alert("Si è verificato un errore durante la prenotazione del viaggio.");
        }
      });
    }
  }
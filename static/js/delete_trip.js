// asynchronous call to remove the trip
function deleteTrip(idViaggio) {
    if (confirm("Are you sure you want to cancel this trip?")) {
      // makes the AJAX call to remove the trip
      $.ajax({
        url: "/delete_trip/" + idViaggio,   // url to which to make the request
        method: "POST",                     // request method, in this case POST
        data: { idViaggio: idViaggio },     // request data
        success: function(response) {
          // if the request was successful, the user interface is updated
          $("#viaggio_" + idViaggio).remove();
          createToast('success', 'Trip deleted successfully');

          setTimeout(function() {
              location.reload();
          }, 5000); 
        },
        error: function(error) {    // in case of an error during the request
          // an alert containing the error is displayed and displayed in the console
          console.error("Errore durante la cancellazione del viaggio:", error);
          alert("Si è verificato un errore durante l'eliminazione del viaggio.");
        }
      });
    }
  }
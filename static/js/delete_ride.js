// asynchronous call to remove the switch request
function cancelRide(idViaggio) {
    if (confirm("Sei sicuro di voler cancellare questa richiesta di passaggio?")) {
        // make the AJAX call to cancel the pass request
        $.ajax({
            url: "/delete_ride/" + idViaggio,   // url to which to make the request
            method: "POST",                     // request method, in this case POST
            data: { idViaggio: idViaggio },     // request data
            success: function(response) {
                // if the request was successful, the user interface is updated
                controllaStatoPassaggio(idViaggio);
                $("#ride_" + idViaggio).remove();
                createToast('success', 'Ride request deleted successfully');

                setTimeout(function() {
                    location.reload();
                }, 5000);               
            },
            error: function(error) {   // in case of an error during the request
                // an alert containing the error is displayed and displayed in the console
                console.error("Errore durante la cancellazione della richiesta di passaggio:", error);
                alert("Si è verificato un errore durante l'eliminazione della richiesta di passaggio.");
            }
        });
    }
}
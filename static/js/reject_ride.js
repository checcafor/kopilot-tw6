// asynchronous call to reject the pass request
function rejectRide(idRichiestaPassaggio) {
    if (confirm("Sei sicuro di voler rifiutare questa richiesta di passaggio?")) {
        // make the AJAX call to reject the pass request
        $.ajax({
            url: "/reject_ride/" + idRichiestaPassaggio,                // url to which to make the request
            method: "POST",                                             // request method, in this case POST
            data: { idRichiestaPassaggio: idRichiestaPassaggio },       // request data
            success: function(response) {
                // if the request was successful, the user interface is updated
                $("#richiesta_" + idRichiestaPassaggio).remove();
            },
            error: function(error) {    // in case of an error during the request
                // an alert containing the error is displayed and displayed in the console
                console.error("Errore durante il rifiuto della richiesta di passaggio:", error);
                alert("Si è verificato un errore durante il rifiuto della richiesta di passaggio.");
            }
        });
    }
}
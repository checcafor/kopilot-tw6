// asynchronous call to accept the handover request
function acceptRide(idRichiestaPassaggio) {
    if (confirm("Sei sicuro di voler accettare questa richiesta di passaggio?")) {
        // makes the AJAX call to accept the handover request
        $.ajax({
            url: "/accept_ride/" + idRichiestaPassaggio,            // url to which to make the request
            method: "POST",                                         // request method, in this case POST
            data: { idRichiestaPassaggio: idRichiestaPassaggio },   // request data
            success: function(response) {
                // if the request was successful, the user interface is updated
                $("#richiesta_" + idRichiestaPassaggio).remove();
                createToast('success', 'Trip request acceppted with success');

                setTimeout(function() {
                    location.reload();
                }, 5000); 
            },
            error: function(error) {    // in case of an error during the request
                // an alert containing the error is displayed and displayed in the console
                console.error("Errore durante l'accettazione della richiesta di passaggio:", error);
                alert("Si è verificato un errore durante l'accettazione della richiesta di passaggio.");
            }
        });
    }
}
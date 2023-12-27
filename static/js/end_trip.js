// asynchronous call to end the trip "mark it as finished"
function endTrip(idEnd) {
    if (confirm("Are you sure you want to end this trip?")) {
        // makes the AJAX call to mark the trip as finished
        $.ajax({
            url: "/end_trip/" + idEnd,  // url to which to make the request
            method: "POST",             // request method, in this case POST
            data: { idEnd: idEnd },     // request data
            success: function(response) {
                // if the request was successful, the user interface is updated in the block of the corresponding trip
                var cardElement = $("#viaggio_" + idEnd); // find the travel card block
                var badgeElement = cardElement.find('.badge.text-bg-warning'); // find the element with the correct class

                // verifica se l'elemento è stato trovato
                if (badgeElement.length > 0) {
                    // change the content and classes of the element
                    badgeElement.text('Finished').removeClass('text-bg-warning').addClass('text-bg-success');
                } else {
                    // an error is shown in the console
                    console.error('Elemento non trovato');
                }
                // this function is invoked to check that the entire interface is updated correctly
                controllaStatoViaggio(idEnd);

                createToast('success', 'Trip ended successfully');

            },
            error: function(error) {    // in case of an error during the request
                // an alert containing the error is displayed and displayed in the console
                console.error("Errore durante la terminazione del viaggio:", error);
                alert("Si è verificato un errore durante la terminazione del viaggio.");
            }
        });
    }
}
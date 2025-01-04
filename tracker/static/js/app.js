function openTransactionPopup(type) {
    $.ajax({
        url: `/tracker/transaction-popup/${type}/`,
        type: "GET",
        success: function(data) {
            if (data.html_form) {
                // Add overlay and popupto the DOM
                $('body').append('<div id="popup-modal">' + data.html_form + '</div>');
                $('#popup-modal').show();

                // Submit the form
                $('#transaction-form').on('submit', function(event) {
                    event.preventDefault();
                    $.ajax({
                        url: `/tracker/transaction-popup/${type}/`,
                        type: "POST",
                        data: $(this).serialize(),
                        success: function(data) {
                            if (data.success) {
                                location.reload(); // Refresh the page
                            } else {
                                alert('Error: ' + JSON.stringify(data.errors));
                            }
                        }
                    });
                });
            }
        }
    });
}

function closePopup(){
    $('#popup-modal').fadeOut(200, function (){
        $(this).remove();
    });
}

$(document).ready(function() {
    $('#deposit-btn').on('click', function() {
        openTransactionPopup('deposit');
    });

    $('#withdraw-btn').on('click', function() {
        openTransactionPopup('withdrawal');
    });

    // Close the modal (basic implementation)
    $(document).on('click', '#popup-modal', function(e) {
        if (e.target.id === 'popup-modal') {
            $('#popup-modal').remove();
        }
    });
});

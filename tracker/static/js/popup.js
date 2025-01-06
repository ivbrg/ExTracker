// Function to open the transaction popup
function openTransactionPopup(type) {
    $.ajax({
        url: `/tracker/transaction-popup/${type}/`, // Endpoint for the popup content
        type: "GET",
        success: function (data) {
            if (data.html_form) {
                // Add overlay and popup content to the DOM
                $('body').append('<div class="popup-overlay"></div>');
                $('body').append('<div id="popup-modal">' + data.html_form + '</div>');

                // Show the popup and overlay
                $('.popup-overlay').fadeIn(200);
                $('#popup-modal').fadeIn(200);
            }
        }
    });
}

// Function to close the popup
function closePopup() {
    $('.popup-overlay').fadeOut(200, function () {
        $(this).remove();
    });
    $('#popup-modal').fadeOut(200, function () {
        $(this).remove();
    });
}
function openTransactionPopup(type) {
    $.ajax({
        url: `/tracker/transaction-popup/${type}/`,
        type: "GET",
        success: function(data) {
            if (data.html_form) {     
                
                // Add overlay and popup to the DOM

                $('body').append('<div class="popup-overlay"></div>');
                $('body').append('<div id="popup-modal">' + data.html_form + '</div>');

                $('#popup-modal').show();

                // Show the overlay and popup
                $('.popup-overlay').fadeIn(200);
                $('#popup-modal').fadeIn(200);

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
    $('.popup-overlay').fadeOut(200, function(){
        $(this).remove();
    })
    $('#popup-modal').fadeOut(200, function (){
        $(this).remove();
    });
}

function changePerPage(select) {
    const perPage = select.value;
    const currentUrl = new URL(window.location.href);

    // Update the "per_page" query parameter
    currentUrl.searchParams.set('per_page', perPage);
    currentUrl.searchParams.set('page', 1); // Reset to the first page

    // Reload the page with the updated URL
    window.location.href = currentUrl.toString();
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

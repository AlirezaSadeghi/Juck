$(document).ready(function () {

    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    $('body').on('click', '.view-details', function () {
        var req_id = $(this).attr('data-req');
        var resp_id = $(this).attr('data-resp');

        if (req_id)
            window.location = '/requests/conversation/@/#/'.replace('@', req_id).replace('#', resp_id);
        else
            window.location = '/requests/conversation/@/'.replace('@', req_id);
    });

});
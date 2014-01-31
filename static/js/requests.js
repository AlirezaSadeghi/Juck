$(document).ready(function () {

    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    $('body').on('click', '.view-details', function () {
        var req_id = $(this).attr('data-req');
        var usr_id = $(this).attr('data-user');

        if (usr_id)
            window.location = '/requests/conversation/@/#/'.replace('@', req_id).replace('#', usr_id);
        else
            window.location = '/requests/conversation/@/'.replace('@', req_id);
    });

});
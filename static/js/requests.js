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


    $("#send-response").click(function () {
        content = $("#response-content").val();
        dt_id = $("#dt_id").val();
        $.post('/requests/respond/', {csrfmiddlewaretoken: csrfToken, dt_id: dt_id, content: content}, function (data) {
            if (data.op_status == 'success') {
                var cmtElem = $(".tmp").clone(true);
                cmtElem.find('.author').append(data.author);
                cmtElem.find('.text').append(content);
                message('پاسخ شما با موفقیت ثبت شد.', 'Success');
                $(".my-container").append(cmtElem.html());
            }
            else {
                message(data.message, 'Warning');
            }
        })
    });

    $('.approve-req').click(function () {
        var pk = $(this).attr('data-id');

        $.post('/requests/approve/', {csrfmiddlewaretoken: csrfToken, pk: pk}, function (data) {
            if (data.op_status == 'success') {
                message('درخواست مورد نظر با موفقیت تایید شد.', 'Success');
            }
            else {
                message('شما اجازه این عمل را ندارید.', 'Warning');
            }
        });
    });

    $('#reject').click(function () {
        var pk = $(this).attr('data-id');

        $.post('/requests/reject/', {csrfmiddlewaretoken: csrfToken, pk: pk}, function (data) {
            if (data.op_status == 'success') {
                message('درخواست مورد نظر با موفقیت رد شد.', 'Success');
            }
            else {
                message('شما اجازه این عمل را ندارید.', 'Warning');
            }
        });
    });

});
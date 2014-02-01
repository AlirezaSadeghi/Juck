$(document).ready(function () {
    csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    $('.advanced_search_panel').hide();
    $('.advanced_search').click(function () {
        $('.advanced_search_panel').slideToggle('slow');
    });
    $('.ui.rating').rating({
        initialRating: 3, interactive: false
    });


//    ('input[value="both"]')
//        .checkbox('enable');
//    $('.ui.checkbox[value="ignore"]')
//        .checkbox('enable');

    $('.ui.redio.checkbox')
        .checkbox();


    $('.answer_box').each(function () {
        $(this).hide();
    });
    $('.javab_box').each(function () {
        $(this).hide();
    });

    $('.single_question .slide').click(function () {
        $(this).parent().parent().parent().find('.javab_box').slideToggle('slow');

        $(this).parent().parent().parent().find('.answer_box').slideToggle('slow');
        var a = $(this).find("i")
        if (a.hasClass('up')) {
            a.removeClass('up').addClass('down');
        }
        else {
            a.removeClass('down').addClass('up');
        }
    });

//    $('.single_question .slide').click(function () {
//
//    });


    $('.ui.accordion').accordion();

    $('.tabular.menu a').click(function () {
        $('.tabular.menu a').removeClass('active').removeClass('fj_green')
        $(this).addClass('active').addClass('fj_green')

        if ($(this).hasClass('faq_add_tab')) {
            $('.faq_list').addClass('display_none');
            $('.faq_add').removeClass('display_none');
            update_usr_ask_q();
            update_mngr_ans_common_q();
        }
        else {
            console.log('are!');
            $('.faq_add').addClass('display_none');
            $('.faq_list').removeClass('display_none');

        }
    });

    $(".ui.section.divider").last().remove();


    var query = window.location.search;

// downloading articles in articles_list page
    $('.news_list .small.blue.button.dl_a').click(function () {
        window.location.href = window.location.origin + window.location.pathname + '?a_pk=' + $(this).attr('id').replace('a', '');
    });

    $('.attached.message .dl_btn .article').click(function () {
        window.location.href = window.location.origin + window.location.pathname + query + '&dl=true';
    });
});


function send_ajax(data, type, url) { //, callback){
    $.ajax({ // create an AJAX call...
        data: data,
        type: type,
        url: url,
        dataType: dataType,
        success: function (response) { // on success..
            console.log(response)
            //callback();
        },
        error: function (jqXHR) {
            alert("error" + jqXHR.status)
        },
        crossDomain: false
    });
    return false;
}


function submit_jobseeker_list(event) {
//    alert(event.keyCode);
    if (event.keyCode == 13) {
        $('#job_seeker_list_form').submit();
    }
}

function submit_employer_list(event) {
    if (event.keyCode == 13) {
        $('#employer_list_form').submit();
    }
}

function disapprove_user(id, user_type) {
    $.post('/accounts/users/approve/', {'csrfmiddlewaretoken': csrfToken, 'function': 'disapprove', 'id': id, 'user_type': user_type}, function (response) {
        if (response.op_status == 'success') {
            $('#job_seeker' + id).css('background-color', '#DB4D4D');
            $('#job_seeker' + id + ' .rf-user-info div span').css('color', '#C3B8B8');
            message(response.message, 'Success');
        } else {
            message(response.message, 'Error');
        }
    });
}


function approve_user(id, user_type) {
    $.post('/accounts/users/approve/', {'csrfmiddlewaretoken': csrfToken, 'function': 'approve', 'id': id, 'user_type': user_type}, function (response) {
        if (response.op_status == 'success') {
            $('#job_seeker' + id).css('background-color', '#00cc66');
            message(response.message, 'Success');
        } else {
            message(response.message, 'Error');
        }
    });
}

function remove_user(id, user_type) {
    $.post('/accounts/users/approve/', {'csrfmiddlewaretoken': csrfToken, 'function': 'remove', 'id': id, 'user_type': user_type}, function (response) {
        if (response.op_status == 'success') {
            $('#job_seeker' + id).css('background-color', '#DB4D4D');
            $('#job_seeker' + id + ' .rf-user-info div span').css('color', '#C3B8B8');
            message(response.message, 'Success');
        } else {
            message(response.message, 'Error');
        }
    });
}

function update_usr_ask_q() {
    $('.usr_ask_q').click(function () {
        var title = $('.field input[name="title"]').val();
        var content = $('.field textarea[name="content"]').val();
        send_ajax({title: title, content: content, csrfmiddlewaretoken: csrfToken}, '/question/ask_question/', redirect);
    });
}

function update_mngr_ans_common_q() {
    $('.usr_mngr_ans_q').click(function () {
        var title = $('.faq_add #id_title').val();
        var content = $('.field textarea[name="content"]').val();
        alert(title + 'sdfsd' + content);
        if (!title || !content) {
            message('هر دو فیلد باید پر شوند.', 'Error');
        }
        else {
            send_ajax({title: title, content: content, csrfmiddlewaretoken: csrfToken}, '/question/add_common_question/', redirect);
        }
    });
}


function send_ajax(data, url, callback) {
    $.post(url, data, function (response) {
        if (response.op_status == 'success') {
            callback(response);
        }
        else {
            alert("err");
        }
    });
}


function redirect(resposnse) {
    window.location.href = resposnse['redirect'];
}
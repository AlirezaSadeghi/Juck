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
            a.removeClass('up').addClass('down')
        }
        else {
            a.removeClass('down').addClass('up');
        }
    });

//    $('.single_question .slide').click(function () {
//
//    });

    $('.single_question .edit_q').click(function () {

        if ($(this).hasClass('fj_pressed')) {
            $(this).removeClass('fj_pressed');
            var txt = $(this).siblings('.ui.form').find('textarea').val();
            $(this).siblings('.ui.form').replaceWith('<div class="ui message"><p>' + txt + '</p></div>')
            $(this).contents().first()[0].textContent = 'ویرایش'
        }
        else {
            $(this).addClass('fj_pressed');
            var answer = $(this).siblings('.ui.message').find("p").text().trim();
            $(this).siblings('.message').replaceWith('<div class="ui form"><div class="field"><textarea cols="70" rows="6" placeholder="ویرایش پاسخ">' + answer + '</textarea></div></div>')
            $(this).contents().first()[0].textContent = 'تایید'
        }
        $(this).find('.icon').toggleClass('edit').toggleClass('checkmark')

    });

    $('.ui.accordion').accordion();

    $('.tabular.menu a').click(function () {
        $('.tabular.menu a').removeClass('active').removeClass('fj_green')
        $(this).addClass('active').addClass('fj_green')

        if ($(this).hasClass('faq_add_tab')) {
            $('.faq_list').addClass('display_none')
            $('.faq_add').removeClass('display_none')
        }
        else {
            console.log('are!');
            $('.faq_add').addClass('display_none')
            $('.faq_list').removeClass('display_none')
        }
    });

    $(".ui.section.divider").last().remove()

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

    var query = window.location.search;

    // downloading articles in articles_list page
    $('.news_list .small.blue.button.dl_a').click(function () {
        window.location.href = window.location.origin + window.location.pathname + '?a_pk=' + $(this).attr('id').replace('a', '');
    })

    $('.attached.message .dl_btn .article').click(function () {
        window.location.href = window.location.origin + window.location.pathname + query + '&dl=true';
    })
});


function submit_jobseeker_list(event) {
//    alert(event.keyCode);
    if (event.keyCode == 13) {
        $('#job_seeker_list_form').submit();
    }
}

function submit_employer_list(event) {
//    alert(event.keyCode);
    if (event.keyCode == 13) {
        $('#employer_list_form').submit();
    }
}


function approve_user(id, user_type) {
    $.post('/accounts/users/approve/', {'csrfmiddlewaretoken': csrfToken, 'function': 'approve', 'id': id, 'user_type': user_type}, function (response) {
        if (response.op_status == 'success') {
            $('#job_seeker'+id).css('background-color','#00cc66');

//            alert(response.message);
        } else {
//            alert(response.message);
        }
    });
}

function remove_user(id, user_type) {
    $.post('/accounts/users/approve/', {'csrfmiddlewaretoken': csrfToken, 'function': 'remove', 'id': id, 'user_type': user_type}, function (response) {
        if (response.op_status == 'success') {
            $('#job_seeker'+id).css('background-color','#DB4D4D');
            $('#job_seeker'+id+' .rf-user-info div span').css('color','#C3B8B8');

//            alert(response.message);
        } else {
//            alert(response.message);
        }
    });
}


function disapprove_user(id, user_type) {
    $.post('/accounts/users/approve/', {'csrfmiddlewaretoken': csrfToken, 'function': 'disapprove', 'id': id, 'user_type': user_type}, function (response) {
        if (response.op_status == 'success') {
            $('#job_seeker'+id).css('background-color','#DB4D4D');
            $('#job_seeker'+id+' .rf-user-info div span').css('color','#C3B8B8');

//            alert(response.message);
        } else {
//            alert(response.message);
        }
    });
}
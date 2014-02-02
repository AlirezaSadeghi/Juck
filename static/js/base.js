$(document).ready(function () {

    $('a[href*=#]:not([href=#])').click(function () {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                $('html,body').animate({
                    scrollTop: target.offset().top
                }, 1000);

                return false;
            }
        }
    });

    $('body').on('click', '.rf-show-modal', function () {
        var type = $(this).attr('id');
        $("#reg_type").val(type);
    });

    $('#captcha-modal')
        .modal('setting', {
            closable: false,
            onDeny: function () {
            },
            onApprove: function () {
                startLoginProc();
                return false
            }
        })

        .modal('attach events', '.rf-show-modal', 'show');


    csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    $().toastmessage({sticky: false});
    $('.ui.dropdown').dropdown();

    $('.index-column').hover(function () {
        $(this).find('.ui.button.small:eq(0)').toggleClass('elem-hidden');
    });

    $("#sign-in").click(function (e) {
        $("#login-div").fadeToggle('slow');
        e.stopPropagation();
    });

    $("#login-div").click(function (e) {
        e.stopPropagation();
    });

    $('body').click(function (e) {
        $("#login-div").fadeOut();
    });

    $('#login-btn').click(function () {
        dict = {
            csrfmiddlewaretoken: csrfToken,
            username: $('#login-username').val().trim(),
            password: $('#login-password').val()
        };

        $.post('/accounts/ajax_login/', dict, function (data) {
            if (data.op_status == "success") {
                window.location = data.redirect_url;
            }
            else {
                message(data.message, 'Error');
            }
        });
    });

    var onload = true;
    $(window).scroll(function () {
        if (onload) {
            onload = false;
            return;
        }
        var pos = $(window).scrollTop();

        var list = ['#hm', '#ji', '#jsi', '#ei'];

        if (pos < 450) {
            $("#hm").parent().addClass('active');
            list = ['#hm', '#ji', '#jsi', '#ei'];
            list.splice(0, 1);
        }
        else if (pos > 450 && pos < 1290) {
            $("#ji").parent().addClass('active');
            list = ['#hm', '#ji', '#jsi', '#ei'];
            list.splice(1, 1);
        }
        else if (pos > 1290 && pos < 1990) {
            $("#jsi").parent().addClass('active');
            list = ['#hm', '#ji', '#jsi', '#ei'];
            list.splice(2, 1);
        }
        else if (pos >= 1990) {
            $("#ei").parent().addClass('active');
            list = ['#hm', '#ji', '#jsi', '#ei'];
            list.splice(3, 1);
        }

        for (var item in list) {
            $(list[item]).parent().removeClass('active');
        }
    });

    $('.thumbs.icon').click(function () {
        if ($(this).hasClass('outline') && $(this).hasClass('down')) {
            sadeghi('dislike', 'enable');
        }
        if ($(this).hasClass('outline') && $(this).hasClass('up')) {
            sadeghi('like', 'enable');
        }
        if (!$(this).hasClass('outline') && $(this).hasClass('down')) {
            sadeghi('dislike', 'disable');
        }
        if (!$(this).hasClass('outline') && $(this).hasClass('down')) {
            sadeghi('dislike', 'disable');
        }
        $(this).toggleClass('outline');
    });

    function sadeghi(type, action) {
        $('.thumbs.icon').click(function () {
            if ($(this).hasClass('outline') && $(this).hasClass('down')) {
                sadeghi('dislike', 'enable');
            }
            if ($(this).hasClass('outline') && $(this).hasClass('up')) {
                sadeghi('like', 'enable');
            }
            if (!$(this).hasClass('outline') && $(this).hasClass('down')) {
                sadeghi('dislike', 'disable');
            }
            if (!$(this).hasClass('outline') && $(this).hasClass('down')) {
                sadeghi('dislike', 'disable');
            }
            $(this).toggleClass('outline');
        });
    }

    function sadeghi(type, action) {
//        alert(type + "    " + action);
    }


});

function doAjaxLogin(e) {
    if (e.keyCode == 13) {
        $("#login-btn").trigger('click');
    }
}

function refreshCaptchaCrap() {

    $.getJSON('/accounts/refresh_captcha/', function (data) {
        $("#id_captcha_0").val(data.key);
        $("img.captcha").attr('src', data.url + '?' + new Date().getTime());
    });

    return false;
}

function startLoginProc() {

    $.post('/accounts/check_catpcha/', $("#captcha-shit").serialize(), function (data) {
        if (data.op_status == 'success') {
            window.location = data.url;
        }
        else {
            message('کد امنیتی صحیح وارد نشده است. لطفا دوباره سعی کنید.', 'Error');
        }
    });
    return false;
}

function message(msg, type) {
    var stuff = 'show' + type + 'Toast'
    $().toastmessage(stuff, msg);
}

function handleKeyPress(event) {
    if (event.keyCode == 13) {
        startLoginProc();
        return false;
    }
}

function fetchComments(obj_type, obj_id, page, div) {
    $.post('/comments/show/', {csrfmiddlewaretoken: csrfToken, 'type': obj_type, 'id': obj_id, 'page_size': 4, 'page': page, 'obj_div': div}, function (data) {
        if (data.op_status == 'success') {
            $(div).html(data.html);
        }
        else {
            message(data.message, 'Error');
        }
    });
}

function addComment(obj_type, obj_id, div, comment) {
    var dict = {
        csrfmiddlewaretoken: csrfToken,
        'comment': comment,
        'type': obj_type,
        'id': obj_id
    }

    $.post('/comments/add/', dict, function (data) {
        if (data.op_status == 'success') {

            fetchComments(obj_type, obj_id, 1, div);
            message(data.message, 'Success');

        }
        else {
            message(data.message, 'Error');
        }
    });
}


function addRate(obj_type, obj_id, rate) {
    console.log('adding rate...');
    var dict = {
        csrfmiddlewaretoken: csrfToken,
        'rate': rate,
        'obj_type': obj_type,
        'obj_id': obj_id
    }

    $.post('/rating/add/', dict, function (data) {
        if (data.op_status == 'success') {
            console.log('success...');
            location.reload();

        }
        else {
            message(data.message, 'Error');
            if (obj_type == 'job_seeker' || obj_type == 'employer') {
//                console.log('errorrr...');
                location.reload();
            }

        }
    });

}

function deletItem(item_type, item_id) {
//    console.log('deleteing ');
    if (item_type == 'article') {

        $.post('/article/remove/', {'id': item_id, csrfmiddlewaretoken: csrfToken}, function (data) {
            if (data.op_status == 'success') {
                console.log('here');
                window.location = '/article/articles_list/';
            }
            else {
                message(data.message, 'Error');
            }
        });

    } else if (item_type == 'news') {
        $.post('/news/remove/', {'id': item_id, csrfmiddlewaretoken: csrfToken }, function (data) {
            if (data.op_status == 'success') {
                console.log('here');
                window.location = '/news/news_list/';
            }
            else {
                message(data.message, 'Error');
            }
        });

    } else {
       message('چنین نوعی وجود ندارد.', 'Error');
    }
}

function reveiew_sub_article(funct, item_id){
    $.post('/article/submitted_article/review/', {'review': funct, 'id': item_id, csrfmiddlewaretoken: csrfToken }, function (data) {
        if (data.op_status == 'success') {
//            console.log('here');
            window.location = '/article/articles_list/';
        }
        else {
            message(data.message, 'Error');
        }
    });
}
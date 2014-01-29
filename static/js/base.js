$(document).ready(function () {

    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

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
                message(data.message, 'alert-warning');
            }
        });
    });

    var onload = true;
    $(window).scroll(function () {
        if(onload){
            onload = false;
            return;
        }
        var pos = $(window).scrollTop();

        var list = ['#hm', '#ji', '#jsi', '#ei'];

        if(pos < 450){
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
        else if (pos >= 1990){
            $("#ei").parent().addClass('active');
            list = ['#hm', '#ji', '#jsi', '#ei'];
            list.splice(3, 1);
        }

        for(var item in list){
            $(list[item]).parent().removeClass('active');
        }
    });

});

function doAjaxLogin(e){
    if(e.keyCode == 13){
        $("#login-btn").trigger('click');
    }
}

function message(text, style) {
    $('<div class="ctn-field-page-alert ' + style + '">' + text + '</div>').prependTo($('.hdr'));
    $('.ctn-field-page-alert').animate({'top': '-1px'}, 'fast', function () {
        $(this).delay(2000).fadeOut(function () {
            $(this).remove();
        });
    });
}
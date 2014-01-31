$(document).ready(function () {

    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    $().toastmessage({sticky:true});
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

    $('.thumbs.icon').click(function(){
        if($(this).hasClass('outline') && $(this).hasClass('down')){
            sadeghi('dislike', 'enable');
        }
        if($(this).hasClass('outline') && $(this).hasClass('up')){
            sadeghi('like', 'enable');
        }
        if(!$(this).hasClass('outline') && $(this).hasClass('down')){
            sadeghi('dislike', 'disable');
        }
        if(!$(this).hasClass('outline') && $(this).hasClass('down')){
            sadeghi('dislike', 'disable');
        }
	    $(this).toggleClass('outline');
    });

    function sadeghi(type, action){
//        alert(type + "    " + action);
    }


});

function doAjaxLogin(e){
    if(e.keyCode == 13){
        $("#login-btn").trigger('click');
    }
}

function message(msg, type ){
    var stuff = 'show' + type  + 'Toast'
    $().toastmessage(stuff, msg);
}
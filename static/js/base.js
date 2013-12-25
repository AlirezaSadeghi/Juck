$(document).ready(function () {

    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    $('.index-column').hover(function () {
        $(this).find('.ui.button.small:eq(0)').toggleClass('elem-hidden');
    });

    $("#sign-in").click(function(e){
        $("#login-div").fadeToggle('slow');
        e.stopPropagation();
    });

    $("#login-div").click(function(e){
        e.stopPropagation();
    });

    $('body').click(function(e){
         $("#login-div").fadeOut();
    });

    $('#login-btn').click(function(){
        dict = {
            csrfmiddlewaretoken:csrfToken,
            username:$('#login-username').val().trim(),
            password:$('#login-password').val()
        };

        $.post('/accounts/ajax_login/', dict, function(data){
            if(data.op_status == "success"){
                window.location = data.redirect_url;
            }
            else{
                alert(data.message);
            }
        });
    });

});
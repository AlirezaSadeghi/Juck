$(document).ready(function () {
    $('.index-column').hover(function () {
        $(this).find('.ui.button.small:eq(0)').toggleClass('elem-hidden');
    });

    $("#sign-in").click(function(){
        $("#login-div").fadeToggle('slow');
    });
});
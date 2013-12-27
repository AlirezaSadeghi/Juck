$(document).ready(function () {
	$('.advanced_search_panel').hide();
	$('.advanced_search').click(function(){
		$('.advanced_search_panel').slideToggle('slow');
	});
	$('.ui.rating').rating({
		initialRating: 3,interactive: false
	});



//    ('input[value="both"]')
//        .checkbox('enable');
//    $('.ui.checkbox[value="ignore"]')
//        .checkbox('enable');

    $('.ui.redio.checkbox')
        .checkbox();

    $('.answer_box').each(function(){
        $(this).hide();
    });
    $('.javab_box').each(function(){
        $(this).hide();
    });

    $('.single_question .slide').click(function(){
        $(this).parent().parent().parent().find('.answer_box').slideToggle('slow');
//        var a = $(this).find("i")
//        if (a.hasClass('up')){
//            a.removeClass('up').addClass('down')
//        }
//        else{
//            a.removeClass('down').addClass('up');
//            alert("avazi");
//        }
    });

    $('.single_question .slide').click(function(){
        $(this).parent().parent().parent().find('.javab_box').slideToggle('slow');
    });

    $('.single_question .edit_q').click(function(){

        if ($(this).hasClass('fj_pressed')){
            $(this).removeClass('fj_pressed');
            var txt = $(this).siblings('.ui.form').find('textarea').val();
            $(this).siblings('.ui.form').replaceWith('<div class="ui message"><p>'+ txt +'</p></div>')
        }
        else{
            $(this).addClass('fj_pressed');
            var answer = $(this).siblings('.ui.message').find("p").text().trim();
            $(this).siblings('.message').replaceWith('<div class="ui form"><div class="field"><textarea cols="70" rows="6" placeholder="ویرایش پاسخ">'+ answer +'</textarea></div></div>')
        }
    });

    $('.ui.accordion').accordion();

    $('.tabular.menu a').click(function(){
        $('.tabular.menu a').removeClass('active').removeClass('fj_green')
        $(this).addClass('active').addClass('fj_green')

        if ($(this).hasClass('faq_add_tab')){
            $('.faq_list').addClass('display_none')
            $('.faq_add').removeClass('display_none')
        }
        else{
            console.log('are!');
            $('.faq_add').addClass('display_none')
            $('.faq_list').removeClass('display_none')
        }
    });

    $(".ui.section.divider").last().remove()
});

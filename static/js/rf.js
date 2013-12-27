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
    $('.answer_btn').click(function(){
        $(this).parent().next().slideToggle('slow');
    });
});

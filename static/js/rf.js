$(document).ready(function () {
	$('.advanced_search_panel').hide();
	$('.advanced_search').click(function(){
		$('.advanced_search_panel').slideToggle('slow');
	});
	$('.ui.rating').rating({
		initialRating: 3,interactive: false,
	});
});

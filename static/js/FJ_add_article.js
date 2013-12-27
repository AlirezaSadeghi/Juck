/**
 * Created by Sina on 12/13/13.
 */
 function addTagsAndAuthors(){
    var authors_inputs = $(".clr input.author");
    var tags_inputs = $(".clr input.tag");
    var authors = "";
    var tags = "";

    authors_inputs.each(function(index){
        authors += $(this).val() + ',';
    })

    tags_inputs.each(function(index){
        tags += $(this).val() + ',';
    })

    $("#id_authors").val(authors);
    $("#id_tags").val(tags);
}
$(document).ready(function () {
    $("#upfile1").click(function () {
        $("#news_image").trigger('click');
    });

    $("#pic-button").click(function () {
        $("#news_image").trigger('click');
    });

     //ezafe kardane field ba click ruye dokme ha



    $("#add_author").click(function(){
        if($(".author").size()<3)
        {
            $(this).prev().append("<input placeholder='نویسنده' type='text' class='author newfield'>");
            setTimeout(function(){
                $(".newfield").removeClass("newfield");
            },0);
        }
    });

    $("#add_tag").click(function(){
        if($(".tag").size()<5)
            $(this).prev().append("<input placeholder='برچسب' type='text' class='tag'>");
            setTimeout(function(){
                $(".newfield").removeClass("newfield");
            },0);
    });


});



/**
 * Created by Sina on 12/13/13.
 */

$(document).ready(function () {
    $("#upfile1").click(function () {
        $("#news_image").trigger('click');
    });

    $("#pic-button").click(function () {
        $("#news_image").trigger('click');
    });

});


function final_submit2() {
    var title = $("#news_title")[0];
    title = title.value;

    var description = $("#news_des")[0];
    description = description.value;

    var tk = $('input[name="csrfmiddlewaretoken"]').val();

    var ajaxData = {
        title: title,
        description: description,
        csrfmiddlewaretoken: tk
    };
    $("#sinaForm").ajaxSubmit({
        url: "/news/submit_news/",
        type: 'POST',
        data: ajaxData,
        success: function (data, err, xhr, tk) {
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert(" Status: " + textStatus + "Error: " + errorThrown);
        }
    })
}


function final_submit() {
    var title = $("#news_title")[0];
    title = title.value;

    var description = $("#news_des")[0];
    description = description.value;

    var tk = $('input[name="csrfmiddlewaretoken"]').val();

    var ajaxData = {
        title: title,
        description: description,
        csrfmiddlewaretoken: tk
    };

    $.ajax({
        url: "/news/submit_news/",
        type: 'POST',
        data: ajaxData,
        success: function (data, status, xhr) {
            alert("News submitted successfully!");
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert(" Status: " + textStatus + "Error: " + errorThrown);
        }
        // ...
    });

}

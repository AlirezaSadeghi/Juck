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

function submit_news_pic() {

    var tk = $('input[name="csrfmiddlewaretoken"]').val();
    var ajaxData = {
        csrfmiddlewaretoken: tk
    };
    $("#sinaForm").ajaxSubmit({
        url: "/news/upload_image/",
        type: "POST",
        data: ajaxData,
        success: function (data, err, xhr, tk) {
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert(" Status: " + textStatus + "Error: " + errorThrown);
        }
    })
}


function final_submit2() {
    var title = $("#news_title")[0];
    title = title.value;

    var description = $("#news_des")[0];
    description = description.value;

    var name2 = $("#news_image");
    name2 = name2[0];
    if (name2.files.length != 0)
        name2 = name2.files[0].name;

    console.log(name2);

    var tk = $('input[name="csrfmiddlewaretoken"]').val();

    var ajaxData = {
        title: title,
        description: description,
        name: name2,
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

    var image_url = $("#news_image")[0];
    image_url = image_url.getAttribute('src');

    console.log("ss");
    console.log(image_url);
    console.log("ss");
    if (image_url == null)
        image_url = 'empty'

    var tk = $('input[name="csrfmiddlewaretoken"]').val();

    var ajaxData = {
        title: title,
        description: description,
        image_url :image_url,
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
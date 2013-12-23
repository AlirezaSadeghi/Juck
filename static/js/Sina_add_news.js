/**
 * Created by Sina on 12/13/13.
 */

$(document).ready(function () {
    $("#upImage").click(function () {
        $("#news_image").trigger('click');
    });

    $("#files").click(function () {
        $("#news_image").trigger('click');
    });
});

function submit_news_pic() {
    console.log("sssssssssssssssssssss")
    var tk = $('input[name="csrfmiddlewaretoken"]').val();
    var file = $("#news_image")[0];
    var ajaxData = {
        csrfmiddlewaretoken: tk
    };
    $.ajax({
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

////////////////////////////////////////////////
$(function () {
    'use strict';
    // Change this to the location of your server-side upload handler:
    var url = '/news/upload_image/',
        uploadButton = $('<button/>')
            .addClass('btn btn-primary')
            .prop('disabled', true)
            .text('Processing...')
            .on('click', function () {
                var $this = $(this),
                    data = $this.data();
                $this
                    .off('click')
                    .text('Abort')
                    .on('click', function () {
                        $this.remove();
                        data.abort();
                    });
                data.submit().always(function () {
                    $this.remove();
                });
            });
    $('#news_image').fileupload({
        url: url,
        dataType: 'POST',
        autoUpload: false,
        acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
        maxFileSize: 5000000, // 5 MB
        // Enable image resizing, except for Android and Opera,
        // which actually support image resizing, but fail to
        // send Blob objects via XHR requests:
        disableImageResize: /Android(?!.*Chrome)|Opera/
            .test(window.navigator.userAgent),
        previewMaxWidth: 250,
        previewMaxHeight: 250,
        previewCrop: true
    }).on('fileuploadadd', function (e, data) {
//            $("#image_place").innerHTML = "";
            var x = $("#files")[0];
            var first = x.children[0];
            if (first != undefined)
                x.removeChild(first);
            data.context = $('<div/>').appendTo('#files');
        $.each(data.files, function (index, file) {
            var node = $('<p/>');
//                    .append($('<span/>').text(file.name));
            if (!index) {
                node
                    .append('<br>');
//                    .append(uploadButton.clone(true).data(data));
            }
            $("#image_place").innerHTML = "";
            node.appendTo(data.context);
        });
    }).on('fileuploadprocessalways', function (e, data) {
        var index = data.index,
            file = data.files[index],
            node = $(data.context.children()[index]);
        if (file.preview) {
            node
                .prepend('<br>')
                .prepend(file.preview);
        }
        if (file.error) {
            node
                .append('<br>')
                .append($('<span class="text-danger"/>').text(file.error));
        }
        if (index + 1 === data.files.length) {
            data.context.find('button')
                .text('Upload')
                .prop('disabled', !!data.files.error);
        }
    }).on('fileuploadprogressall', function (e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        $('#progress .progress-bar').css(
            'width',
            progress + '%'
        );
    }).on('fileuploaddone', function (e, data) {
        $.each(data.result.files, function (index, file) {
            if (file.url) {
                var link = $('<a>')
                    .attr('target', '_blank')
                    .prop('href', file.url);
                $(data.context.children()[index])
                    .wrap(link);
            } else if (file.error) {
                var error = $('<span class="text-danger"/>').text(file.error);
                $(data.context.children()[index])
                    .append('<br>')
                    .append(error);
            }
        });
    }).on('fileuploadfail', function (e, data) {
        $.each(data.files, function (index, file) {
            var error = $('<span class="text-danger"/>').text('File upload failed.');
            $(data.context.children()[index])
                .append('<br>')
                .append(error);
        });
    }).prop('disabled', !$.support.fileInput)
        .parent().addClass($.support.fileInput ? undefined : 'disabled');
});

////////////////////////////////////////////////
function final_submit2() {
    var title = $("#news_title")[0];
    title = title.value;

    var description = $("#news_des")[0];
    description = description.value;

    var name2 = $("#news_image");
    name2 = name2[0];
    if (name2.files.length != 0)
        name2 = name2.files[0].name;
    else {
        name2 = ""
    }
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
            window.location.assign("/news/news_list");

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
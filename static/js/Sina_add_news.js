/**
 * Created by Sina on 12/13/13.
 */

var scale = 0.3;

var cnv;
var ctx;

var inp;

$(document).ready(function () {

    $("#upImage").click(function () {
        $("#news_image").trigger('click');
    });

    $("#files").click(function () {
        $("#news_image").trigger('click');
    });

    cnv = document.querySelector("canvas");
    ctx = cnv.getContext("2d");

    ctx.fillStyle = "#feb";
    ctx.fillRect(0, 0, cnv.width, cnv.height);

    var pimg = new Image();
    pimg.src = "../../static/images/pic-before-load.gif";
    pimg.onload = function() {
        ctx.drawImage(pimg,0,0,cnv.width, cnv.height);
    };
//    inp = document.querySelector("#news_image");
    inp = $("#news_image")[0];
    inp.onchange = function (e) {
        var file = e.target.files[0];
        var reader = new FileReader();
        reader.onload = function (ev) {
            ctx.clearRect(0,0, 300, 150);
            var img = new Image();
            img.onload = function () {
                ctx.save();
                ctx.drawImage(img, 0, 0, 300, 150);

                ctx.restore();
            };
            img.src = ev.target.result;
        };
        reader.readAsDataURL(file);
    };

});

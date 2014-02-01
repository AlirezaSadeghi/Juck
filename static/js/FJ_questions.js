/**
 * Created with PyCharm.
 * User: alireza
 * Date: 1/29/14
 * Time: 11:11 AM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function () {
    update_usr_ask_q();
    csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    $('.answer_q').click(function () {
        var id = $(this).parents('.ui.single_question').attr('qid');
        var txt = $(this).siblings('.ui.form').find('textarea').val()
        send_ajax({csrfmiddlewaretoken: csrfToken, pk: id, answer: txt}, '/question/answer_question/');
    });


    $('.del_q').click(function () {
        var id = $(this).parents('.ui.single_question').attr('qid');
        send_ajax({csrfmiddlewaretoken: csrfToken, pk: id, del: 'True'}, '/question/answer_question/');
    });

    $('.del_common_q').click(function(){
        var id = $(this).parents('.ui.single_question').attr('qid');
        send_ajax({csrfmiddlewaretoken: csrfToken, pk: id, del: 'True'}, '/question/remove_common_question/');
        location.reload();
    });

    $('.edit_q').click(function () {

        if ($(this).hasClass('fj_pressed')) {
            var id = $(this).parents('.ui.single_question').attr('qid');

            var txt = $(this).siblings('.ui.form').find('textarea').val();
            send_ajax({csrfmiddlewaretoken: csrfToken, pk: id, answer:txt}, '/question/answer_question/');

            $(this).removeClass('fj_pressed');
            $(this).siblings('.ui.form').replaceWith('<div class="ui message"><p>' + txt + '</p></div>')
            $(this).contents().first()[0].textContent = 'ویرایش'
        }
        else {
            $(this).addClass('fj_pressed');
            var answer = $(this).siblings('.ui.message').find("p").text().trim();
            $(this).siblings('.message').replaceWith('<div class="ui form"><div class="field"><textarea cols="70" rows="6" name="answer" placeholder="ویرایش پاسخ">' + answer + '</textarea></div></div>')
            $(this).contents().first()[0].textContent = 'تایید'
        }
        $(this).find('.icon').toggleClass('edit').toggleClass('checkmark')

    });

    $('.edit_common_q').click(function(){
        if ($(this).hasClass('fj_pressed')) {
            // moghe edit
            var id = $(this).parents('.ui.single_question').attr('qid');
            var txt = $(this).parents('.javab_box').find('.ui.form').find('textarea').val();
            var edit_title = $(this).parents('.single_question').find('input[name="common_q_title"]').val();

            send_ajax({csrfmiddlewaretoken: csrfToken, pk: id, answer: txt, title: edit_title}, '/question/edit_common_question/');
            $(this).removeClass('fj_pressed');
            $(this).parents('.single_question').find('.question_info1 .ui.form').replaceWith('<span class="question_title">'+edit_title+'</span>')
            $(this).parents('.single_question').find('.javab_box .ui.form').replaceWith('<div class="ui message"><p>' + txt + '</p></div>');
            $(this).contents(2).textContent = 'ویرایش'
        }
        else {
            $(this).addClass('fj_pressed');
            var answer = $(this).parents('.javab_box').find('.ui.message').find("p").text().trim();
            var title = $(this).parents('.single_question').find('span.question_title').text();
            $(this).parents('.javab_box').find('.message').replaceWith('<div class="ui form"><div class="field"><textarea cols="70" rows="6" name="answer">' + answer + '</textarea></div></div>')
            $(this).parents('.single_question').find('span.question_title').replaceWith('<div class="ui form" style="display:inline-block"><input type="text" name="common_q_title" value="@"/></div>'.replace('@', title));
            $(this).contents(2).textContent = 'تایید'
        }
        $(this).find('.icon').toggleClass('edit').toggleClass('checkmark')
    });

});


function send_ajax(data, url, callback) {
    $.post(url, data, function (response) {
        if (response.op_status == 'success') {
            callback(response);
        }
    });
}

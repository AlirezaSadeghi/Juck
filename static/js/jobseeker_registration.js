$(document).ready(function () {
    var number_of_edu_forms = 0;
    var number_of_skill_forms =0;
    var number_of_work_forms =0;

    var divider = '<div class=\"ui section divider\" style=\"margin-top:1rem !important;margin-bottom:1rem !important\"></div>'

    $('#add-edu').click(function(){
       $('.reg_form .edu-info-form'+number_of_edu_forms).after(divider);
       var a =$('.reg_form .edu-info-form'+number_of_edu_forms).clone();
       a.find('input[type=text]').attr('value', '')
       a.attr('class', 'edu-info-form'+(number_of_edu_forms+1));
       $('.edu-info-form'+number_of_edu_forms).next().after(a);
       number_of_edu_forms++;
   });

    $('#add-skill').click(function(){
        $('.reg_form .skill-info-form'+number_of_skill_forms).after(divider);
        var a =$('.reg_form .skill-info-form'+number_of_skill_forms).clone();
        a.attr('class', 'skill-info-form'+(number_of_skill_forms+1));
        a.find('input[type=text]').attr('value', '');
        $('.skill-info-form'+number_of_skill_forms).next().after(a);
        number_of_skill_forms++;
    });

    $('#add-work').click(function(){
        $('.reg_form .work-info-form'+number_of_work_forms).after(divider);
        var a =$('.reg_form .work-info-form'+number_of_work_forms).clone();
        a.find('input[type=text]').attr('value', '')
        a.attr('class', 'work-info-form'+(number_of_work_forms+1));
        $('.work-info-form'+number_of_work_forms).next().after(a);
        number_of_work_forms++;
    });


});
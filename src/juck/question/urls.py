# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('juck.question.views',
    url(r'^ask_question/$', 'ask_question', {}, name='ask_question'),
    url(r'^common/$', 'common_questions', {}, name='common_questions'),
    url(r'^asked_questions/$', 'asked_questions', {}, name='asked_questions'),

    url(r'^answer_question/$', 'answer_question', {}, name='answer_question'),
    url(r'^your_questions/$',   'your_questions', {}, name='your_questions'),


    url(r'^add_common_question/$', 'add_common_question', {}, name='add_common_question'),
    url(r'^edit_common_question/$', 'edit_common_question', {}, name='edit_common_question'),
    url(r'^remove_common_question/$', 'remove_common_question', {}, name='remove_common_question'),

    url(r'^test/$', 'test', {}, name='test'),

)



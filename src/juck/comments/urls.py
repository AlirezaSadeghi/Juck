# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url


urlpatterns = patterns('juck.comments.views',
                       url(r'^show/$', 'get_comments', name='fetch_comments'),
                       url(r'^add/$', 'add_comment', name='add_comment'),


)
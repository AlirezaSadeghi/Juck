# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('juck.log.views',
    url(r'^view_user_logs/$', 'show_logs_for_user', {}, name='user_logs'),
    url(r'^view_logs/$', 'show_self_log', {}, name='self_logs'),
    url(r'^remove_self_log/$', 'remove_self_log', {}, name='remove_self_log'),
)
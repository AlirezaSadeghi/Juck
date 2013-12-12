
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('juck.news.views',
    url(r'^news_list/$', 'show_news_list', {}, name='news_list'),
    url(r'^news_description/', 'show_news_description', {}, name='show_news_description'),

)
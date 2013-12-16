# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('juck.articles.views',
    url(r'^articles_list/$', 'show_articles_list', {}, name='articles_list'),
    url(r'^article_description', 'show_article_description', {}, name='show_article_description'),
    url(r'^add_article/$', 'add_article', {}, name='add_article')

)

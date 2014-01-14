# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('juck.articles.views',
    url(r'^articles_list/$', 'show_articles_list', {}, name='articles_list'),
    url(r'^article_description', 'show_article_description', {}, name='show_article_description'),
    url(r'^add_article/$', 'add_article', {}, name='add_article'),
    url(r'^recommendations/$', 'show_article_recommendations_list', {}, name='show_article_recommendations_list'),
    url(r'submit_article/', 'submit_article', {}, name='article_submission'),
    url(r'^submitted_article', 'submitted_article_description', {}, name='sub_article_description'),
)

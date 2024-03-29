
from django.conf.urls import patterns, include, url

urlpatterns = patterns('juck.news.views',

    url(r'^news_list/$', 'show_news_list', {}, name='news_list'),
    url(r'^news_description/', 'show_news_description', {}, name='show_news_description'),
    url(r'^add_news/$', 'add_news', {}, name='add_news'),
    url(r'^upload_image/$', 'upload_news_pic', {}, name='upload_news_pic'),
    url(r'^unreachable/$', 'unreachable', {}, name='unreachable'),
    url(r'^remove/$','remove_news',{},name='remove_news'),

)

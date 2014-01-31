# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url


urlpatterns = patterns('juck.rating.views',
                       url(r'^add/$', 'add_rate', name='add_rate'),


)
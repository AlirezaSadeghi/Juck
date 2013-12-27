__author__ = 'Sina'


from django.conf.urls import patterns, include, url

urlpatterns = patterns('juck.requests.views',
    url(r'^dashboard/$', 'dashboard', {}, name='dashboard'),
    url(r'^conversation/$', 'conversation', {}, name='conversation'),

)

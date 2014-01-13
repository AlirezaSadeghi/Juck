__author__ = 'Sina'


from django.conf.urls import patterns, include, url

urlpatterns = patterns('juck.requests.views',
    url(r'^dashboard/$', 'dashboard', {}, name='dashboard'),
    url(r'^conversation/$', 'conversation', {}, name='conversation'),
    url(r'^advertisements/$', 'advertisements', {}, name='advertisements'),
    url(r'^jobseeker_requests/$', 'show_js_requests', {}, name='js_requests'),
    url(r'^employer_requests/$', 'show_em_requests', {}, name='em_requests'),

)

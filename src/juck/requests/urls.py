__author__ = 'Sina'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('juck.requests.views',
                       url(r'^dashboard/$', 'dashboard', {}, name='dashboard'),
                       url(r'^conversation/(?P<req_id>\d+)/$', 'offer_conversation', {}, name='offer_conversation'),
                       url(r'^conversation/(?P<req_id>\w+)/(?P<user_id>\d+)/$', 'request_conversation', {},
                           name='request_conversation'),
                       url(r'^advertisements/$', 'advertisements', {}, name='advertisements'),
                       url(r'^my_needs/$', 'my_needs', {}, name='my_needs'),
                       url(r'^jobseeker_requests/$', 'show_js_requests', {}, name='js_requests'),
                       url(r'^employer_requests/$', 'show_em_requests', {}, name='em_requests'),
                       url(r'^add/(?P<request_type>\w+)/$', 'add_request', {}, name='add_request'),

                       url(r'^apply_for_job_opportunity/(?P<item_pk>\d+)/$', 'apply_for_job_opportunity', {},
                           name='apply_for_job_opportunity'),
                       url(r'^req_status/(?P<request_type>\w+)/(?P<item_pk>\d+)/$', 'view_request_status', {},
                           name='request_status'),
)

# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout
#from django.contrib.auth.views import  password_change, password_change_done
from juck.accounts.views import JobSeekerWizard, EMPLOYER_FORMS, JOB_SEEKER_FORMS, EmployerWizard, passed_captcha
from django.contrib.auth.views import password_reset_done, password_reset, password_reset_confirm, password_reset_complete

urlpatterns = patterns('juck.accounts.views',
                       url(r'^about/$', 'about_us', {}, name='about'),
                       url(r'^contact-us/$', 'contact_us', {}, name='contact_us'),
                       url(r'^login/$', 'login', {}, name='login'),
                       url(r'^ajax_login/$', 'ajax_login', {}, name='ajax_login'),
                       url(r'^logout/$', logout, {'template_name': 'accounts/logout.html', 'extra_context': {
                           'message': u'شما با موفقیت از سامانه جاک خارج شدید. از زمانی که در سامانه جاک گذاشتید،‌متشکریم.'}},
                           name='logout'),
                       url(r'password_recover/$', 'password_recover', name='password_recover'),

                       url(r'register/(?P<u_type>\w+)/$', 'captcha_view', name='captcha_view'),
                       url(r'js_edit_profile/$', 'edit_js_profile', {}, name='js_edit_profile'),
                       url(r'jobseeker_registration/$',
                           passed_captcha(JobSeekerWizard.as_view(JOB_SEEKER_FORMS, )), {},
                           name='jobseeker_registration'),

                       url(r'employer_registration/$', passed_captcha(EmployerWizard.as_view(EMPLOYER_FORMS, )), {},
                           name='employer_registration'),

                       url(r'confirm/(?P<user_type>\w+)/(?P<key>[\w\-]+)/$', 'confirm_registration', {},
                           name='confirm_registration'),


                       url(r'show_profile/emp/edit/$', 'employer_edit_profile', {}, name='employer_edit_profile'),
                       url(r'show_profile/js/edit/$', 'jobseeker_edit_profile', {}, name='jobseeker_edit_profile'),


                       url(r'check_catpcha/$', 'check_catpcha', {}, name='check_catpcha'),

                       url(r'jobseeker_addedu/$', 'jobseeker_addedu'),
                       url(r'jobseeker_addskill/$', 'jobseeker_addskill'),
                       url(r'jobseeker_addexp/$', 'jobseeker_addexp'),
                       url(r'jobseeker_remove/(?P<what>(edu|skill|work))/$', 'jobseeker_remove'),

                       url(r'^profile/', 'show_profile', {}, name='show_profile'),
                       #url(r'^upload_profile_picture/$', 'upload_profile_picture', {}, name='upload_profile_picture'),
                       url(r'^refresh_captcha', 'refresh_captcha', {}, name='refresh_captcha'),
                       url(r'^dos_prevention', 'dos_prevention', {}, name='dos_prevention'),
                       url(r'^user_panel/', 'user_panel'),

                       # Sina vared mishavad
                       url(r'^password_reset/$', password_reset,
                           {'post_reset_redirect': '/password_reset_done/',
                            'template_name': 'accounts/password_reset_form.html',
                            'email_template_name': 'accounts/password_reset_email.html'}, name="password_reset"),

                       url(r'^password_reset_done/$',
                           password_reset_done, {'template_name': 'accounts/password_reset_done.html'}),

                       url(r'^password_reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           password_reset_confirm,
                           {'post_reset_redirect': '/password_done/',
                            'template_name': 'accounts/password_reset_confirm.html'}),

                       url(r'^password_done/$',
                           password_reset_complete, {'template_name': 'accounts/password_reset_complete.html'}),
                       #Sina kharej mishavad

                       url(r'^job_seeker_list/(?P<approved_status>[\w\-]+)/$', 'job_seeker_list', {},
                           name='job_seeker_list'),
                       url(r'^employer_list/(?P<approved_status>[\w\-]+)/$', 'employer_list', {}, name='employer_list'),

                       url(r'^show_profile/', 'show_profile', {}, name='show_profile'),

                       url(r'^users/approve/$', 'ajax_remove_or_approve_user', {}, name='approve_user')
)
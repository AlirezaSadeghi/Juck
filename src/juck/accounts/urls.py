# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout
#from django.contrib.auth.views import  password_change, password_change_done
from juck.accounts.views import JobSeekerWizard, EMPLOYER_FORMS, JOB_SEEKER_FORMS, EmployerWizard
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

                       url(r'jobseeker_registration/$',
                           JobSeekerWizard.as_view(JOB_SEEKER_FORMS, ), {},
                           name='jobseeker_registration'),

                       url(r'employer_registration/$', EmployerWizard.as_view(EMPLOYER_FORMS, ), {},
                           name='employer_registration'),
                           
                       url(r'jobseeker_addedu/$', 'jobseeker_addedu'),
                       url(r'jobseeker_addskill/$', 'jobseeker_addskill'),
                       url(r'jobseeker_addexp/$', 'jobseeker_addexp'),
                       url(r'jobseeker_remove/(?P<what>(edu|skill|work))/$', 'jobseeker_remove'),

                       #url(r'^confirm_registration/(?P<hash_value>\w+)$', 'confirm_registration' , {} , name='confirm-registration'),
                       #url(r'^change_password/$', 'change_password', {}, name='change_password'),
                       #url(r'^password_change/$', password_change, {'template_name':'accounts/change_password.html', 'post_change_redirect':'/accounts/profile?pwd=true'}, name='password_change'),
                       #url(r'^password_recover/$', 'password_recover', name='password_recover'),
                       #url(r'^password_change_recover/(?P<hash_value>\w+)$', 'password_change_recover', name='password_change_recover'),
                       #url(r'^reset_forgotten_password/$', 'reset_forgotten_password', name='reset_forgotten_password'),
                       #url(r'^profile/', 'show_profile', {}, name='show_profile'),
                       #url(r'^upload_profile_picture/$', 'upload_profile_picture', {}, name='upload_profile_picture'),
                       url(r'^refresh_captcha', 'refresh_captcha', {}, name='refresh_captcha'),
                       url(r'^dos_prevention', 'dos_prevention', {}, name='dos_prevention'),
                       url(r'^user_panel/', 'user_panel'),

                       # Sina vared mishavad
                       url(r'^password_reset/$', password_reset,
                           {'post_reset_redirect': '/password_reset_done/',
                            'template_name': 'accounts/password_reset_form.html',
                            'email_template_name': 'accounts/password_reset_email.html'}, name="password_reset"),

                       #url(r'^password_reset/$', password_reset,
                        #   {'post_reset_redirect': '/password_reset_done/',
                         #   'template_name': 'accounts/password_reset_form.html',
                          #  }, name="password_reset"),

                       url(r'^password_reset_done/$',
                           password_reset_done, {'template_name': 'accounts/password_reset_done.html'}),

                       url(r'^password_reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           password_reset_confirm,
                           {'post_reset_redirect': '/password_done/',
                            'template_name': 'accounts/password_reset_confirm.html'}),

                       url(r'^password_done/$',
                           password_reset_complete, {'template_name': 'accounts/password_reset_complete.html'}),
                       #Sina kharej mishavad

                       # kas khal chera url o akhe neveshti balash FJ :)))))))))
                       #                      FJ
                       url(r'^job_seeker_list/$', 'job_seeker_list', {}, name='job_seeker_list'),
                       url(r'^employer_list/$', 'employer_list', {}, name='employer_list'),

                    url(r'^pending_employers_list/$', 'pending_employers_list', {}, name='pending_employers_list'),
                    url(r'^pending_jobseekers_list/$', 'pending_jobseekers_list', {}, name='pending_jobseekers_list'),
                    url(r'^show_profile/', 'show_profile', {}, name='show_profile'),
)
# -*- coding: utf-8 -*-
from django.contrib.formtools.wizard.views import SessionWizardView
from django.shortcuts import render_to_response

from juck.accounts.forms import *


JOB_SEEKER_FORMS = [
    ("Phase_1", JobSeekerRegisterForm1),
    ("Phase_2", JobSeekerRegisterForm2),
    ("Phase_3", JobSeekerRegisterForm3),
    ("Phase_4", JobSeekerRegisterForm4),
]

EMPLOYER_FORMS = [
    ("Phase_1", EmployerRegisterForm1),
    ("Phase_2", EmployerRegisterForm2),
    ("Phase_3", EmployerRegisterForm3),
]


class JobSeekerWizard(SessionWizardView):
    template_name = 'accounts/job_seeker_registration.html'

    def done(self, form_list, **kwargs):
        return render_to_response('messages.html', {
            'message': u'خب الان باید تموم شده باشه ! :دی'
        })


class EmployerWizard(SessionWizardView):
    template_name = 'accounts/employer_registration'

    def done(self, form_list, **kwargs):
        return render_to_response('messages.html', {
            'message': u'خب الان باید تموم شده باشه ! :دی'
        })
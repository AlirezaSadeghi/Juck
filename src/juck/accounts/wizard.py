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

JOB_SEEKER_TEMPLATES = {
    "Phase_1": "accounts/job_seeker_reg_p1.html",
    "Phase_2": "accounts/job_seeker_reg_p2.html",
    "Phase_3": "accounts/job_seeker_reg_p3.html",
    "Phase_4": "accounts/job_seeker_reg_p4.html",
}

EMPLOYER_FORMS = [
    ("Phase_1", EmployerRegisterForm1),
    ("Phase_2", EmployerRegisterForm2),
    ("Phase_3", EmployerRegisterForm3),
]

EMPLOYER_TEMPLATES = {
    "Phase_1": "accounts/employer_reg_p1.html",
    "Phase_2": "accounts/employer_reg_p2.html",
    "Phase_3": "accounts/employer_reg_p3.html",
}


class JobSeekerWizard(SessionWizardView):
    def get_template_names(self):
        return [JOB_SEEKER_TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        return render_to_response('messages.html', {
            'message': u'خب الان باید تموم شده باشه ! :دی'
        })

#def done(self, form_list, **kwargs):
#    return render_to_response('done.html', {
#        'form_data': [form.cleaned_data for form in form_list],
#    })


class EmployerWizard(SessionWizardView):
    def get_template_names(self):
        return [EMPLOYER_TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        print 'test'
        return render_to_response('messages.html', {
            'message': u'خب الان باید تموم شده باشه ! :دی'
        })
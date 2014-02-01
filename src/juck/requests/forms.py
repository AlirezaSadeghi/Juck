# -*- coding: utf-8 -*-

from django import forms
from juck.requests.models import Request, JobOpportunity, EmployerJobOffer, JobseekerJobOffer


class RequestForm(forms.Form):
    title = forms.CharField(max_length=250, required=True, label=u'عنوان')
    content = forms.CharField(required=True, label=u'متن درخواست', widget=forms.Textarea())


    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label



class JobOpportunityForm(forms.ModelForm):
    class Meta:
        model = JobOpportunity
        exclude = ['status', 'timestamp', 'employer']
        widgets = {
            'cooperation_type': forms.Select(choices=(
                (0, u'انتخاب کنید'),
                (1, u'تمام وقت'),
                (2, u'پاره وقت'),
                (3, u'دورکاری'),
            )),
            'certificate': forms.Select(choices=(
                (u'', u'انتخاب مدرک'),
                (u'دیپلم', u'دیپلم'),
                (u'کارشناسی', u'کارشناسی'),
                (u'کارشناسی ارشد', u'کارشناسی ارشد'),
                (u'دکتری', u'دکتری'),
            )),
            'sex': forms.Select(choices=(
                (u'', u'انتخاب جنسیت'),
                (True, u'مرد'),
                (False, u'زن'),
                (None, u'دیگر'),
            ))

        }

    def __init__(self, *args, **kwargs):
        super(JobOpportunityForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label


class ResponseForm(forms.Form):
    content = forms.CharField(required=True, label=u'متن درخواست', widget=forms.Textarea())
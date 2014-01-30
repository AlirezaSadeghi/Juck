# -*- coding: utf-8 -*-

from django import forms
from juck.requests.models import Request


class RequestForm(forms.Form):
    # sender = forms.CharField(max_length=200, required=True, label=u'فرستنده', widget=forms.TextInput(attrs={'disabled': 'disabled'}))
    # receiver = forms.CharField(max_length=200, required=True, label=u'گیرنده', widget=forms.TextInput(attrs={'disabled': 'disabled'}))

    title = forms.CharField(max_length=250, required=True, label=u'عنوان')
    cooperation_type = forms.ChoiceField(required=True, label=u'نوع همکاری',
                                         choices=(
                                             (1, u'تمام وقت'),
                                             (2, u'پاره وقت'),
                                             (3, u'دورکاری'),
                                         ))
    content = forms.CharField(required=True, label=u'متن درخواست', widget=forms.Textarea())

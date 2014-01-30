# -*- coding: utf-8 -*-

from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from juck.question.models import Question
from django.db.models import Q

from juck.requests.models import Request, JobseekerJobOffer, EmployerJobOffer, JobOpportunity


class RequestListFilter:
    class RequestFilterForm(forms.Form):
        employer = forms.CharField(label=u'کارفرما', max_length=150, required=False, widget=forms.TextInput(
            attrs={'class': '', 'placeholder': u''}))

        job_seeker = forms.CharField(label=u'کارجو', max_length=150, required=False, widget=forms.TextInput(
            attrs={'class': '', 'placeholder': u''}))

        title = forms.CharField(label=u'عنوان', max_length=150, required=False, widget=forms.TextInput(
            attrs={'class': '', 'placeholder': u''}))

        content = forms.CharField(label=u'متن', max_length=150, required=False, widget=forms.TextInput(
            attrs={'class': '', 'placeholder': u''}))

        major = forms.CharField(required=False)

        cooperation_type = forms.ChoiceField(label=u'نوع همکاری', required=False, choices=(
            ('', u''), (Request.COOPERATION_TYPES['full_time'], u'تمام وقت'),
            (Request.COOPERATION_TYPES['half_time'], u'پاره وقت'), (Request.COOPERATION_TYPES['tele_work'], u'پاره وقت')
        ))

        sex = forms.ChoiceField(label=u'جنسیت', required=False, choices=(
            ('', u'جنسیت نیروها'), ('', u'مرد'), ('', u'زن'),
        ))

        status = forms.ChoiceField(label=u'وضعیت پاسخ', required=False, choices=(
            ('', u'وضعیت پاسخ'), (True, u'پاسخ داده شده'), (False, u'پاسخ داده نشده'), ))

    Form = RequestFilterForm

    def init_filter(self, GET_dict, request_type='request', **kwargs):
        self.form = self.Form(GET_dict)

        if request_type == 'ejo' and 'employer' in kwargs:
            filter_kwargs = {}
            employer_filter = kwargs.pop('employer')
        else:
            filter_kwargs = kwargs
            employer_filter = ''

        job_seeker = ''
        major = ''
        if self.form.is_valid():
            title = self.form.cleaned_data.get('title', '')
            employer = self.form.cleaned_data.get('employer', '')
            job_seeker = self.form.cleaned_data.get('job_seeker', '')
            content = self.form.cleaned_data.get('content', '')
            cooperation_type = self.form.cleaned_data.get('cooperation_type', '')
            sex = self.form.cleaned_data.get('sex', '')
            major = self.form.cleaned_data.get('major', '')
            status = self.form.cleaned_data.get('status', '')

            if title:
                filter_kwargs.update({'title__icontains': title})
            if employer:
                filter_kwargs.update({'employer_profile__company_name__icontains': employer})
            if content:
                filter_kwargs.update({'content__icontains': content})
            if cooperation_type:
                filter_kwargs.update({'cooperation_type': cooperation_type})
            if sex:
                filter_kwargs.update({'sex': sex})
            if status:
                filter_kwargs.update({'status': status})

        if request_type == "jsjo":
            requests = JobseekerJobOffer.objects.filter(**filter_kwargs)
        elif request_type == "ejo":
            requests = EmployerJobOffer.objects.filter(**filter_kwargs)
        elif request_type == 'jo':
            requests = JobOpportunity.objects.filter(**filter_kwargs)
        else:
            requests = Request.objects.none()

        if request_type in ['jsjo', 'ejo']:
            if job_seeker:
                requests = requests.filter(
                    Q(sender__last_name__icontains=job_seeker) |
                    Q(sender__first_name__icontains=job_seeker))
            if major:
                requests = requests.filter(Q(first_major=major) |
                                           Q(second_major=major))

        if request_type == 'ejo' and employer_filter:
            requests = requests.filter(Q(employer=employer_filter) | Q(em_receiver=employer_filter))

        count = requests.count()

        requests = requests.order_by('-timestamp')
        paginator = Paginator(requests, settings.RESULTS_PER_PAGE)
        page = GET_dict.get('page')

        try:
            result = paginator.page(page)
        except PageNotAnInteger:
            result = paginator.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)

        return result, count

    def get_form(self):
        return self.form


class ResponseListFilter:
    class ResponseFilterForm(forms.Form):

        employer = forms.CharField(label=u'کارفرما', max_length=150, required=False, widget=forms.TextInput(
            attrs={'class': '', 'placeholder': u'کارفرما'}))

        cooperation_type = forms.ChoiceField(label=u'نوع همکاری', required=False, choices=(
            (1, u'aaa'),
            (2, u'bbb'),
            (3, u'ccc'),
            (4, u'ddd'),
            (5, u'eee'),
        ))

        title = forms.CharField(label=u'عنوان', max_length=150, required=False, widget=forms.TextInput(
            attrs={'class': '', 'placeholder': u''}))

        response = forms.CharField(label=u'متن', max_length=150, required=False, widget=forms.TextInput(
            attrs={'class': '', 'placeholder': u''}))

        status = forms.CharField(required=False)

    Form = ResponseFilterForm

    def init_filter(self, GET_dict, request_type='request', **kwargs):
        self.form = self.Form(GET_dict)

        if request_type == 'ejo' and 'employer' in kwargs:
            filter_kwargs = {}
            employer_filter = kwargs.pop('employer')
        else:
            filter_kwargs = kwargs
            employer_filter = ''

        job_seeker = ''
        major = ''
        if self.form.is_valid():
            title = self.form.cleaned_data.get('title', '')
            employer = self.form.cleaned_data.get('employer', '')
            job_seeker = self.form.cleaned_data.get('job_seeker', '')
            content = self.form.cleaned_data.get('content', '')
            cooperation_type = self.form.cleaned_data.get('cooperation_type', '')
            sex = self.form.cleaned_data.get('sex', '')
            major = self.form.cleaned_data.get('major', '')
            status = self.form.cleaned_data.get('status', '')

            if title:
                filter_kwargs.update({'title__icontains': title})
            if employer:
                filter_kwargs.update({'employer_profile__company_name__icontains': employer})
            if content:
                filter_kwargs.update({'content__icontains': content})
            if cooperation_type:
                filter_kwargs.update({'cooperation_type': cooperation_type})
            if sex:
                filter_kwargs.update({'sex': sex})
            if status:
                filter_kwargs.update({'status': status})

        if request_type == "jsjo":
            requests = JobseekerJobOffer.objects.filter(**filter_kwargs)
        elif request_type == "ejo":
            requests = EmployerJobOffer.objects.filter(**filter_kwargs)
        elif request_type == 'jo':
            requests = JobOpportunity.objects.filter(**filter_kwargs)
        else:
            requests = Request.objects.none()

        if request_type in ['jsjo', 'ejo']:
            if job_seeker:
                requests = requests.filter(
                    Q(sender__last_name__icontains=job_seeker) |
                    Q(sender__first_name__icontains=job_seeker))
            if major:
                requests = requests.filter(Q(first_major=major) |
                                           Q(second_major=major))

        if request_type == 'ejo' and employer_filter:
            requests = requests.filter(Q(employer=employer_filter) | Q(em_receiver=employer_filter))

        count = requests.count()

        requests = requests.order_by('-timestamp')
        paginator = Paginator(requests, settings.RESULTS_PER_PAGE)
        page = GET_dict.get('page')

        try:
            result = paginator.page(page)
        except PageNotAnInteger:
            result = paginator.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)

        return result, count

    def get_form(self):
        return self.form
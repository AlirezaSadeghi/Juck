# -*- coding: utf-8 -*-

from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from juck.accounts.models import Employer, JobSeeker
from juck.question.models import Question
from django.db.models import Q

from juck.requests.models import Request, JobseekerJobOffer, EmployerJobOffer, JobOpportunity, DiscussionThread


class RequestListFilter:
    class RequestFilterForm(forms.Form):

        total_search = forms.CharField(label=u'جستجو کلی', max_length=150, required=False,
                                       help_text=u'این قسمت میان عنوان, متن و نام کارفرمایان عملیات جستجو را انجام می دهد.',
                                       widget=forms.TextInput(
                                           attrs={'placeholder': u'جستجو'}))

        employer = forms.CharField(label=u'کارفرما', max_length=150, required=False, widget=forms.TextInput(
            attrs={'class': '', 'placeholder': u'کارفرما'}))

        title = forms.CharField(label=u'عنوان', max_length=150, required=False, widget=forms.TextInput(
            attrs={'class': ''}))

        content = forms.CharField(label=u'متن', max_length=150, required=False, widget=forms.TextInput(
            attrs={'class': '', 'placeholder': u'متن درخواست'}))

        major = forms.CharField(required=False, label=u'رشته تحصیلی', widget=forms.TextInput(
            attrs={'class': ''}))

        cooperation_type = forms.ChoiceField(label=u'نوع همکاری', required=False, choices=(
            ('', u'تمامی حالات'), (Request.COOPERATION_TYPES['full_time'], u'تمام وقت'),
            (Request.COOPERATION_TYPES['half_time'], u'پاره وقت'), (Request.COOPERATION_TYPES['tele_work'], u'دور کاری')
        ))

        sex = forms.ChoiceField(label=u'جنسیت', required=False, choices=(
            ('', u'همه موارد'), (True, u'مرد'), (False, u'زن'), (None, u'دیگر')
        ))

        def __init__(self, *args, **kwargs):
            super(RequestListFilter.RequestFilterForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs['placeholder'] = self.fields[field].label

    Form = RequestFilterForm


    def init_filter(self, GET_dict, request_type='request', **kwargs):
        self.form = self.Form(GET_dict)

        related = False
        resume = ''
        if 'related' in kwargs:
            related = kwargs.pop('related')
            resume = kwargs.pop('resume')

        if request_type == 'ejo' and 'employer' in kwargs:
            filter_kwargs = {}
            employer_filter = kwargs.pop('employer')
        else:
            filter_kwargs = kwargs
            employer_filter = ''

        job_seeker = ''
        major = ''
        if self.form.is_valid():
            total_search = self.form.cleaned_data.get('total_search', '')
            title = self.form.cleaned_data.get('title', '')
            employer = self.form.cleaned_data.get('employer', '')
            job_seeker = self.form.cleaned_data.get('job_seeker', '')
            content = self.form.cleaned_data.get('content', '')
            cooperation_type = self.form.cleaned_data.get('cooperation_type', '')
            sex = self.form.cleaned_data.get('sex', '')
            major = self.form.cleaned_data.get('major', '')
            # status = self.form.cleaned_data.get('status', '')

            if title:
                filter_kwargs.update({'title__icontains': title})
            if employer:
                filter_kwargs.update({'employer__profile__company_name__icontains': employer})
            if content:
                filter_kwargs.update({'content__icontains': content})
            if cooperation_type:
                filter_kwargs.update({'cooperation_type': cooperation_type})
            if sex != '':
                filter_kwargs.update({'sex': eval(sex)})

        if request_type == "jsjo":
            requests = JobseekerJobOffer.objects.filter(**filter_kwargs)
        elif request_type == "ejo":
            requests = EmployerJobOffer.objects.filter(**filter_kwargs)
        elif request_type == 'jo':
            requests = JobOpportunity.objects.filter(**filter_kwargs)
            if related:
                educations = resume.education.all()

                major_list = []
                for item in educations:
                    major_list.append(item.major)

                cert_list = []
                for item in educations:
                    cert_list.append(item.certificate)
                for i in range(len(educations)):
                    requests = requests.filter(
                        (Q(first_major=major_list[i]) | Q(second_major=major_list[i])),
                        certificate=cert_list[i])

        else:
            requests = Request.objects.none()

        print(requests)

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

        content = total_search
        requests = requests.filter((Q(title__icontains=content) | Q(content__icontains=content) | Q(
            employer__profile__company_name__icontains=content)   ))

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

        responder = forms.CharField(label=u'پاسخ دهنده', required=False)
        status = forms.ChoiceField(label=u'وضعیت پاسخ', required=False, choices=(
            ('', u'وضعیت پاسخ'), (True, u'قبول شده'), (False, u'رد شده'), (None, u'در دست بررسی') ))


        def __init__(self, *args, **kwargs):
            super(ResponseListFilter.ResponseFilterForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs['placeholder'] = self.fields[field].label

    Form = ResponseFilterForm

    def init_filter(self, GET_dict, item_pk=''):
        self.form = self.Form(GET_dict)

        request = JobOpportunity.objects.get(pk=item_pk)
        dts = DiscussionThread.objects.filter(request=request)

        if self.form.is_valid():
            responder = self.form.cleaned_data.get('responder', '')
            status = self.form.cleaned_data.get('status', '')

            if status:
                dts = dts.filter(request__status=eval(status))
            if responder:
                dts = dts.filter(Q(responder__first_name__icontains=responder) |
                                 Q(responder__last_name__icontains=responder))

        guys = []
        for dt in dts:
            guys.append(dt.responder.cast())

        count = dts.count()

        paginator = Paginator(guys, settings.RESULTS_PER_PAGE)
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


class DashboardListFilter:
    class DashboardFilterForm(forms.Form):

        total_search = forms.CharField(label=u'جستجو کلی', max_length=150, required=False,
                                       help_text=u'این قسمت میان عنوان و نام کارفرمایان جستجو می کند.',
                                       widget=forms.TextInput(
                                           attrs={'placeholder': u'جستجو'}))

        employer = forms.CharField(label=u'نام سازمان', max_length=150, required=False, widget=forms.TextInput(
            attrs={'class': '', 'placeholder': u''}), help_text=u'هم در میان فرستندگان و هم گیرندگان جستجو می شود.')

        title = forms.CharField(label=u'عنوان', max_length=150, required=False, widget=forms.TextInput(
            attrs={'class': '', 'placeholder': u''}))

        cooperation_type = forms.ChoiceField(label=u'نوع همکاری', required=False, choices=(
            ('', u'همه موارد'), (Request.COOPERATION_TYPES['full_time'], u'تمام وقت'),
            (Request.COOPERATION_TYPES['half_time'], u'پاره وقت'), (Request.COOPERATION_TYPES['tele_work'], u'دور کاری')
        ))

        status = forms.ChoiceField(label=u'وضعیت پاسخ', required=False, choices=(
            ('', u'همه موارد'), (True, u'قبول شده'), (False, u'رد شده'), (None, u'در دست بررسی') ))

        def __init__(self, *args, **kwargs):
            super(DashboardListFilter.DashboardFilterForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs['placeholder'] = self.fields[field].label


    Form = DashboardFilterForm


    def init_filter(self, GET_dict, user_type='', user_pk='', request_type='', **kwargs):
        self.form = self.Form(GET_dict)

        filter_kwargs = kwargs

        if self.form.is_valid():
            total_search = self.form.cleaned_data.get('total_search', '')
            employer = self.form.cleaned_data.get('employer', '')
            title = self.form.cleaned_data.get('title', '')
            cooperation_type = self.form.cleaned_data.get('cooperation_type', '')
            status = self.form.cleaned_data.get('status', '')
            if title:
                print(1)
                filter_kwargs.update({'request__title__icontains': title})
            if employer:
                print(2)
                filter_kwargs.update({'request__employer__profile__company_name__icontains': employer})
            if cooperation_type:
                print(3)
                filter_kwargs.update({'request__cooperation_type': cooperation_type})
            if status != '':
                filter_kwargs.update({'request__status': eval(status)})

        threads = []

        if user_type == 'employer':
            employer = Employer.objects.get(pk=user_pk)
            threads = DiscussionThread.objects.filter(Q(request__employer=employer) |
                                                      Q(responder=employer))

        elif user_type == 'jobseeker':
            jobseeker = JobSeeker.objects.get(pk=user_pk)
            threads = DiscussionThread.objects.filter(Q(responder=jobseeker) |
                                                      Q(request__jobseekerjoboffer__sender=jobseeker))

        threads = threads.filter(**filter_kwargs)

        if total_search:
            threads = threads.filter((Q(request__title__icontains=total_search) | Q( request__employer__profile__company_name__icontains=total_search)  ))

        dashboard_items = []
        for item in threads:
            request_child = item.request.cast()
            req_type = ''
            if isinstance(request_child, JobOpportunity):
                req_type = 'jo'
            elif isinstance(request_child, JobseekerJobOffer):
                req_type = 'jso'
            elif isinstance(request_child, EmployerJobOffer):
                req_type = 'ejo'

            resp = item.responses.all()[0] if item.responses.exists() else ''

            dashboard_items.append(
                {'request': item.request.cast(), 'response': resp, 'type': req_type, 'responder_pk': item.responder.pk})

        paginator = Paginator(dashboard_items, settings.RESULTS_PER_PAGE)
        page = GET_dict.get('page')

        try:
            result = paginator.page(page)
        except PageNotAnInteger:
            result = paginator.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)

        return result, len(dashboard_items)


    def get_form(self):
        return self.form

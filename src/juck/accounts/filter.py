# -*- coding: utf-8 -*-

from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from juck.accounts.models import *


class ManagerJobSeekerListFilter:
    class ManagerJobSeekerListFilterFrom(forms.Form):

        first_name = forms.CharField(label=u'نام', max_length=100, required=False)
        last_name = forms.CharField(label=u'نام خانوادگی', max_length=150, required=False)
        from_date = forms.DateTimeField(label=u'از تاریخ', required=False)
        to_date = forms.DateTimeField(label=u'تا تاریخ', required=False)

        #Educational
        certificate = forms.ChoiceField(label=u'مدرک تحصیلی', required=False, choices=(('under_grad', u'کارشناسی'),
                                                                                       ('grad', u'کارشناسی ارشد'),
                                                                                       ('phd', u'دکتری'),
                                                                                       ('post_doc', u'پست دکتری')), )
        edu_status = forms.CharField(label=u'وضعیت تحصیلی', max_length=100, required=False)
        edu_major = forms.CharField(label=u'رشته تحصیلی', max_length=200, required=False)
        edu_orientation = forms.CharField(label=u'گرایش تحصیلی', max_length=150)

        # TODO:
        # skill = forms.CharField(label=u'مهارت', max_length=200, required=False)
        # experience = forms.CharField(label=u'سابقه کاری', max_length=200, required=False)

        #Profile details:
        city = forms.CharField(label=u'شهر', max_length=100, required=False)
        state = forms.CharField(label=u'استان', max_length=100, required=False)
        #other information seems useless: sex/married/military_service_status / exemption_type

        # title = forms.CharField(label=u'عنوان', max_length=150, required=False, widget=forms.TextInput(
        #     attrs={'class': 'search-tab-content-input input-12', 'placeholder': u'عنوان سوال:'}))
        # answer = forms.CharField(label=u'پاسخ', max_length=150, required=False, widget=forms.TextInput(
        #     attrs={'class': 'search-tab-content-input input-12', 'placeholder': u'محتوی پاسخ:'}))
        # answered = forms.ChoiceField(label=u'وضعیت پاسخ', required=False, choices=(
        #     ('', u'وضعیت پاسخ'), (True, u'پاسخ داده شده'), (False, u'پاسخ داده نشده'), ))

    Form = ManagerJobSeekerListFilterFrom

    def init_filter(self, GET_dict, **kwargs):
        self.form = self.Form(GET_dict)

        filter_kwargs = {}
        job_seeker_filter_kwargs = kwargs

        if self.form.is_valid():
            first_name = self.form.cleaned_data.get('first_name', '')
            last_name = self.form.cleaned_data.get('last_name', '')
            from_date = self.form.cleaned_data.get('from_date', '')
            to_date = self.form.cleaned_data.get('to_date', '')
            certificate = self.form.cleaned_data.get('certificate', '')
            edu_status = self.form.cleaned_data.get('edu_status', '')
            edu_major = self.form.cleaned_data.get('edu_major', '')
            edu_orientation = self.form.cleaned_data.get('edu_orientation', '')
            city = self.form.cleaned_data.get('city', '')
            state = self.form.cleaned_data.get('state', '')

            if first_name:
                filter_kwargs.update({'first_name__icontains': first_name})
            if last_name:
                filter_kwargs.update({'last_name__icontains': last_name})
            if from_date:
                filter_kwargs.update({'date_joined__gte': from_date})
            if to_date:
                filter_kwargs.update({'date_joined_lte': to_date})

            if certificate:
                job_seeker_filter_kwargs.update({'resume__education__certificate': certificate})
            if edu_status:
                job_seeker_filter_kwargs.update({'resume__education__status': edu_status})
            if edu_major:
                job_seeker_filter_kwargs.update({'resume__education__major': edu_major})
            if edu_orientation:
                job_seeker_filter_kwargs.update({'resume__education__orientation': edu_orientation})
            if city:
                job_seeker_filter_kwargs.update({'profile__city__name': city})
            if state:
                job_seeker_filter_kwargs.update({'profile__state__name': state})

        user = JuckUser.objects.filter(**filter_kwargs).order_by('-date_joined')
        job_seeker = user.select_subclasses()
        job_seekers = job_seeker.objects.filter(**job_seeker_filter_kwargs)
        count = job_seekers.count()

        paginator = Paginator(job_seekers, settings.RESULTS_PER_PAGE)
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


class ManagerEmployerListFilter:
    class ManagerEmployerListFilterForm(forms.Form):

        #TODO : first and last? nah :-?
        # first_name = forms.CharField(label=u'نام', max_length=100, required=False)
        # last_name = forms.CharField(label=u'نام خانوادگی', max_length=150, required=False)

        from_date = forms.DateTimeField(label=u'از تاریخ', required=False)
        to_date = forms.DateTimeField(label=u'تا تاریخ', required=False)


        #Profile details:
        company_name = forms.CharField(label=u'نام سازمان', required=False, max_length=200)
        #TODO: choices maybe?
        company_type = forms.CharField(label=u'نوع سازمان', required=False, max_length=150)
        #TODO: remember me in html
        foundation_year_form = forms.IntegerField(label=u'از تاریخ',required=False)
        foundation_year_to = forms.IntegerField(label=u'تا تاریخ',required=False)
        #TODO: in model,moshakhasat is such a kossher name :D (esm is more esmi and better)
        manager = forms.CharField(label=u'نام مدیرعامل', required=False, max_length=250)
        #TODO: ye chizaE too hamin mayehaye field behtar nis model shan?searchesh gazjere akhe
        field = forms.CharField(label=u'زمینه فعالیت',required=False,  max_length=200)


        city = forms.CharField(label=u'شهر', max_length=100, required=False)
        state = forms.CharField(label=u'استان', max_length=100, required=False)

        #other information seems useless: sex/married/military_service_status / exemption_type

        # title = forms.CharField(label=u'عنوان', max_length=150, required=False, widget=forms.TextInput(
        #     attrs={'class': 'search-tab-content-input input-12', 'placeholder': u'عنوان سوال:'}))
        # answer = forms.CharField(label=u'پاسخ', max_length=150, required=False, widget=forms.TextInput(
        #     attrs={'class': 'search-tab-content-input input-12', 'placeholder': u'محتوی پاسخ:'}))
        # answered = forms.ChoiceField(label=u'وضعیت پاسخ', required=False, choices=(
        #     ('', u'وضعیت پاسخ'), (True, u'پاسخ داده شده'), (False, u'پاسخ داده نشده'), ))

    Form = ManagerEmployerListFilterForm

    def init_filter(self, GET_dict, **kwargs):
        self.form = self.Form(GET_dict)

        filter_kwargs = {}
        employer_filter_kwargs = kwargs

        if self.form.is_valid():
            first_name = self.form.cleaned_data.get('first_name', '')
            last_name = self.form.cleaned_data.get('last_name', '')
            from_date = self.form.cleaned_data.get('from_date', '')
            to_date = self.form.cleaned_data.get('to_date', '')
            company_name = self.form.cleaned_data.get('company_name', '')
            company_type = self.form.cleaned_data.get('company_type', '')
            foundation_year_form = self.form.cleaned_data.get('foundation_year_form', '')
            foundation_year_to = self.form.cleaned_data.get('foundation_year_to', '')
            manager = self.form.cleaned_data.get('manager', '')
            field = self.form.cleaned_data.get('field', '')
            city = self.form.cleaned_data.get('city', '')
            state = self.form.cleaned_data.get('state', '')

            if first_name:
                filter_kwargs.update({'first_name__icontains': first_name})
            if last_name:
                filter_kwargs.update({'last_name__icontains': last_name})
            if from_date:
                filter_kwargs.update({'date_joined__gte': from_date})
            if to_date:
                filter_kwargs.update({'date_joined_lte': to_date})

            if company_name:
                employer_filter_kwargs.update({'profile__company_name__icontains': company_name})
            if company_type:
                employer_filter_kwargs.update({'profile__company_type': company_type})
            if foundation_year_form:
                employer_filter_kwargs.update({'profile__foundation_year__gte': foundation_year_form})
            if foundation_year_form:
                employer_filter_kwargs.update({'profile__foundation_year__lte': foundation_year_to})
            if city:
                employer_filter_kwargs.update({'profile__manager__icontains': manager})
            if state:
                employer_filter_kwargs.update({'profile__field': field})
            if city:
                employer_filter_kwargs.update({'profile__city__name': city})
            if state:
                employer_filter_kwargs.update({'profile__state__name': state})

        user = JuckUser.objects.filter(**filter_kwargs).order_by('-date_joined')
        employer = user.select_subclasses()
        employers = employer.objects.filter(**employer_filter_kwargs)
        count = employers.count()

        paginator = Paginator(employers, settings.RESULTS_PER_PAGE)
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
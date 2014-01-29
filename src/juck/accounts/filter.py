# -*- coding: utf-8 -*-

from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from juck.accounts.models import *
from django.db.models import Q


class ManagerJobSeekerListFilter:
    class ManagerJobSeekerListFilterFrom(forms.Form):


        search_input = forms.CharField(max_length=200, required=False,
                                       widget=forms.TextInput(attrs={'placeholder': "جستجو..."}))

        first_name = forms.CharField(label=u'نام', max_length=100, required=False)
        last_name = forms.CharField(label=u'نام خانوادگی', max_length=150, required=False)

        #Educational
        certificate = forms.ChoiceField(label=u'مدرک تحصیلی', required=False,
                                        choices=(('', u'انتخاب کنید'),
                                                 ('under_grad', u'کارشناسی'),
                                                 ('grad', u'کارشناسی ارشد'),
                                                 ('phd', u'دکتری'),
                                                 ('post_doc', u'پست دکتری')), )
        edu_status = forms.ChoiceField(required=False, label=u'وضعیت تحصیلی',
                                       choices=(
                                           ('', u'انتخاب کنید'),
                                           ('student', u'دانشجو'),
                                           ('graduated', u'فارغ التحصیل'),
                                       ))
        edu_major = forms.CharField(label=u'رشته تحصیلی', max_length=200, required=False)
        edu_orientation = forms.CharField(label=u'گرایش تحصیلی', max_length=150, required=False)
        edu_uni_name = forms.CharField(label=u'نام دانشگاه', max_length=150, required=False)
        edu_uni_type = forms.ChoiceField(label=u'نوع دانشگاه', choices=(
            ('', u'انتخاب کنید.'),
            ('dolati', u'دولتی'),
            ('azad', u'آزاد'),
            ('entefaei', u'غیرانتفاعی'),
            ('payam_nur', u'پیام نور'),
            ('foregin', u'خارجی'),
        ), required=False)

        # Skill
        skill_title = forms.CharField(required=False, max_length=150, label=u'عنوان مهارت')
        skill_level = forms.ChoiceField(required=False, label=u'سطح تسلط',
                                        choices=(
                                            ('', u'انتخاب کنید.'),
                                            ('low', u'آشنا'),
                                            ('high', u'مسط'),
                                            ('certificate', u'دارای مدرک معتبر'),
                                        ))
        skill_description = forms.CharField(required=False, max_length=250, label=u'توضیحات')

        # Experience
        exp_title = forms.CharField(required=False, max_length=200, label=u'عنوان سابقه')
        exp_place = forms.CharField(required=False, max_length=200, label=u'محل کار')

        #Profile details:
        city = forms.CharField(label=u'شهر', max_length=100, required=False)
        state = forms.CharField(label=u'استان', max_length=100, required=False)
        sex = forms.ChoiceField(label=u'جنسیت',
                                choices=((0, u'انتخاب کنید'), (1, u'مرد'), (2, u'زن'), (3, u'دیگر'),), required=False)
        married = forms.ChoiceField(label=u'وضعیت تاهل ',
                                    choices=((0, u'انتخاب کنید'), (1, u'مجرد'), (2, u'متاهل'), ), required=False)

    Form = ManagerJobSeekerListFilterFrom

    def init_filter(self, GET_dict, **kwargs):
        self.form = self.Form(GET_dict)

        filter_kwargs = {'role': JuckUser.JOB_SEEKER}
        job_seeker_filter_kwargs = kwargs
        search_input = ""

        if self.form.is_valid():
            search_input = self.form.cleaned_data.get('search_input', '')

            first_name = self.form.cleaned_data.get('first_name', '')
            last_name = self.form.cleaned_data.get('last_name', '')
            certificate = self.form.cleaned_data.get('certificate', '')
            edu_status = self.form.cleaned_data.get('edu_status', '')
            edu_major = self.form.cleaned_data.get('edu_major', '')
            edu_orientation = self.form.cleaned_data.get('edu_orientation', '')
            edu_uni_name = self.form.cleaned_data.get('edu_uni_name', '')
            edu_uni_type = self.form.cleaned_data.get('edu_uni_type', '')

            skill_title = self.form.cleaned_data.get('skill_title', '')
            skill_level = self.form.cleaned_data.get('skill_level', '')
            skill_description = self.form.cleaned_data.get('skill_description', '')
            exp_title = self.form.cleaned_data.get('exp_title', '')
            exp_place = self.form.cleaned_data.get('exp_place', '')
            sex = self.form.cleaned_data.get('sex', '')
            married = self.form.cleaned_data.get('married', '')
            city = self.form.cleaned_data.get('city', '')
            state = self.form.cleaned_data.get('state', '')

            if first_name:
                filter_kwargs.update({'first_name__icontains': first_name})
            if last_name:
                filter_kwargs.update({'last_name__icontains': last_name})

            if certificate:
                job_seeker_filter_kwargs.update({'resume__education__certificate': certificate})
            if edu_status:
                job_seeker_filter_kwargs.update({'resume__education__status': edu_status})
            if edu_major:
                job_seeker_filter_kwargs.update({'resume__education__major': edu_major})
            if edu_orientation:
                job_seeker_filter_kwargs.update({'resume__education__orientation': edu_orientation})
            if edu_uni_name:
                job_seeker_filter_kwargs.update({'resume__education__university_name': edu_uni_name})
            if edu_uni_type:
                job_seeker_filter_kwargs.update({'resume__education__university_type': edu_uni_type})
            if sex:
                if int(sex):
                    job_seeker_filter_kwargs.update({'profile__sex': int(sex)})

            if skill_title:
                job_seeker_filter_kwargs.update({'resume__skill__title__icontains': skill_title})
            if skill_level:
                job_seeker_filter_kwargs.update({'resume__skill__level': skill_level})
            if skill_description:
                job_seeker_filter_kwargs.update({'resume__skill__description__icontains': skill_description})

            if exp_title:
                job_seeker_filter_kwargs.update({'resume__experience__title__icontains': exp_title})
            if exp_place:
                job_seeker_filter_kwargs.update({'resume__experience__place__icontains': exp_place})

            if married:
                if married == 1:
                    job_seeker_filter_kwargs.update({'profile__married': False})
                if married == 2:
                    job_seeker_filter_kwargs.update({'profile__married': True})
            if city:
                job_seeker_filter_kwargs.update({'profile__city__name': city})
            if state:
                job_seeker_filter_kwargs.update({'profile__state__name': state})

        user = JuckUser.objects.filter(**filter_kwargs).order_by('-date_joined')
        if search_input:
            user = user.filter(Q(first_name__icontains=search_input) | Q(last_name__icontains=search_input))

        job_seeker_filter_kwargs.update({'pk__in': user.values('pk')})
        # job_seeker = JobSeeker.objects.filter(pk__in=user.values('pk'))
        job_seekers = JobSeeker.objects.filter(**job_seeker_filter_kwargs)

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

        #TODO search what?!
        search_input = forms.CharField(max_length=200, required=False,
                                       widget=forms.TextInput(attrs={'placeholder': "جستجو..."}))

        #Profile details:
        company_name = forms.CharField(label=u'نام سازمان', required=False, max_length=200)
        company_type = forms.CharField(label=u'نوع سازمان', required=False, max_length=150)
        #TODO: remember me in html
        foundation_year_form = forms.IntegerField(label=u'تاسیس از سال', required=False)
        foundation_year_to = forms.IntegerField(label=u'تاسیس تا سال', required=False)
        manager = forms.CharField(label=u'نام مدیرعامل', required=False, max_length=250)
        field = forms.CharField(label=u'زمینه فعالیت', required=False, max_length=200)

        city = forms.CharField(label=u'شهر', max_length=100, required=False)
        state = forms.CharField(label=u'استان', max_length=100, required=False)

    Form = ManagerEmployerListFilterForm

    def init_filter(self, GET_dict, **kwargs):
        self.form = self.Form(GET_dict)

        filter_kwargs = {'role': JuckUser.EMPLOYER}
        employer_filter_kwargs = kwargs
        search_input = ""

        if self.form.is_valid():
            search_input = self.form.cleaned_data.get('search_input', '')

            # first_name = self.form.cleaned_data.get('first_name', '')
            # last_name = self.form.cleaned_data.get('last_name', '')
            # from_date = self.form.cleaned_data.get('from_date', '')
            # to_date = self.form.cleaned_data.get('to_date', '')
            company_name = self.form.cleaned_data.get('company_name', '')
            company_type = self.form.cleaned_data.get('company_type', '')
            foundation_year_form = self.form.cleaned_data.get('foundation_year_form', '')
            foundation_year_to = self.form.cleaned_data.get('foundation_year_to', '')
            manager = self.form.cleaned_data.get('manager', '')
            field = self.form.cleaned_data.get('field', '')
            city = self.form.cleaned_data.get('city', '')
            state = self.form.cleaned_data.get('state', '')

            # if first_name:
            #     filter_kwargs.update({'first_name__icontains': first_name})
            # if last_name:
            #     filter_kwargs.update({'last_name__icontains': last_name})
            # if from_date:
            #     filter_kwargs.update({'date_joined__gte': from_date})
            # if to_date:
            #     filter_kwargs.update({'date_joined_lte': to_date})

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
        # employer = Employer.objects.filter(pk__in=user.values('pk'))

        employer_filter_kwargs.update({'pk__in': user.values('pk')})
        employers = Employer.objects.filter(**employer_filter_kwargs)
        if search_input:
            employers = employers.filter(
                Q(profile__company_name__icontains=search_input) | Q(profile__manager__icontains=search_input) | Q(
                    profile__field__icontains=search_input))

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
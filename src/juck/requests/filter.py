# -*- coding: utf-8 -*-

from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from juck.question.models import Question


    #employer = models.ForeignKey(Employer, verbose_name=u'کارفرما', related_name='requests')
    #title = models.CharField(max_length=250, verbose_name=u'عنوان')
    #content = models.TextField(verbose_name=u'متن درخواست')
    #timestamp = models.DateTimeField(verbose_name=u'زمان ایجاد', auto_now=True)
    #cooperation_type = models.PositiveSmallIntegerField(verbose_name=u'نوع همکاری', blank=True, null=True)
    #status = models.NullBooleanField(verbose_name=u'وضعیت تایید', null=True, blank=True)


class RequestListFilter:

    class RequestFilterForm(forms.Form):
        employer = forms.CharField(label=u'', max_length=150, required=False, widget=forms.TextInput(
            attrs={'class': '', 'placeholder': u''}))

        title = forms.CharField(label=u'', max_length=150, required=False, widget=forms.TextInput(
            attrs={'class': '', 'placeholder': u''}))

        job_seeker = forms.CharField(label=u'', max_length=150, required=False, widget=forms.TextInput(
            attrs={'class': '', 'placeholder': u''}))

        content = forms.CharField(label=u'', max_length=150, required=False, widget=forms.TextInput(
            attrs={'class': '', 'placeholder': u''}))

        cooperation_type = forms.CharField(label=u'', max_length=150, required=False, widget=forms.TextInput(
            attrs={'class': '', 'placeholder': u''}))

        status = forms.ChoiceField(label=u'وضعیت پاسخ', required=False, choices=(
            ('', u'وضعیت پاسخ'), (True, u'پاسخ داده شده'), (False, u'پاسخ داده نشده'), ))

    Form = SecretaryQuestionListFilterForm

    def init_filter(self, GET_dict, **kwargs):
        self.form = self.Form(GET_dict)

        filter_kwargs = kwargs

        if self.form.is_valid():
            title = self.form.cleaned_data.get('title', '')
            answer = self.form.cleaned_data.get('answer', '')
            answered = self.form.cleaned_data.get('answered', '')

            if title:
                filter_kwargs.update({'title__icontains': title})
            if answered:
                filter_kwargs.update({'answer__isnull': True if answered == u'False' else False})
            if answer:
                filter_kwargs.update({'answer__content__icontains': answer})

        questions = Question.objects.filter(**filter_kwargs)
        count = questions.count()

        questions = questions.order_by('-issue_time')
        paginator = Paginator(questions, settings.RESULTS_PER_PAGE)
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
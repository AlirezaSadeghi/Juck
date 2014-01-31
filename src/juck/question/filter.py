# -*- coding: utf-8 -*-

from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from django.db.models.query_utils import Q
from juck.question.models import Question


class ManagerQuestionListFilter:
    class SecretaryQuestionListFilterForm(forms.Form):


        title = forms.CharField(label=u'عنوان', max_length=150, required=False,
                                help_text=u'با پر کردن موارد مد نظر خود عملیات جستجو در میان سوالات و جواب های موجود انجام می شود. دقت کنید نتیجه ی عملیات اشتراک موارد مشخص شده توسط شماست.'
                                ,widget=forms.TextInput(
            attrs={'class': 'search-tab-content-input input-12', 'placeholder': u'عنوان سوال:'}))
        answer = forms.CharField(label=u'پاسخ', max_length=150, required=False, widget=forms.TextInput(
            attrs={'class': 'search-tab-content-input input-12', 'placeholder': u'محتوی پاسخ:'}))
        answered = forms.ChoiceField(label=u'وضعیت پاسخ', required=False, choices=(
            ('', u'وضعیت پاسخ'), (True, u'پاسخ داده شده'), (False, u'پاسخ داده نشده'), ))

        both = forms.CharField(label=u'جستجو کلی', max_length=100, required=False, widget=forms.TextInput(
            attrs={'placeholder': u'جستجو'}))

    Form = SecretaryQuestionListFilterForm

    def init_filter(self, GET_dict, **kwargs):
        self.form = self.Form(GET_dict)

        filter_kwargs = kwargs

        if self.form.is_valid():
            title = self.form.cleaned_data.get('title', '')
            answer = self.form.cleaned_data.get('answer', '')
            answered = self.form.cleaned_data.get('answered', '')
            both = self.form.cleaned_data.get('both', '')

            if title:
                filter_kwargs.update({'title__icontains': title})
            if answered:
                filter_kwargs.update({'answer__isnull': True if answered == u'False' else False})
            if answer:
                filter_kwargs.update({'answer__content__icontains': answer})

        questions = Question.objects.filter(**filter_kwargs)
        questions = questions.filter((Q(title__icontains=both) | Q(answer__content__icontains=both)))
        count = questions.count()

        questions = questions.order_by('-timestamp')
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
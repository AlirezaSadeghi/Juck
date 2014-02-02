# -*- coding: utf-8 -*-

from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from django.db.models.query_utils import Q
from juck.question.models import Question


class ManagerQuestionListFilter:
    class SecretaryQuestionListFilterForm(forms.Form):


        title = forms.CharField(label=u'عنوان', max_length=150, required=False,
                                help_text=u'جستجو در عناوین سوالات. دقت کنید اشتراک این فیلد با سایر فیلد ها به عنوان نتیجه برگردانده می شود.'
                                ,widget=forms.TextInput(
            attrs={'class': 'search-tab-content-input input-12', 'placeholder': u'عنوان سوال:'}))

        content = forms.CharField(label=u'شرح', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': u'متن سوال:'}),
                                  help_text=u'جستجو در متن سوالات. دقت کنید اشتراک این فیلد با سایر فیلد ها به عنوان نتیجه برگردانده می شود.')

        answer = forms.CharField(help_text=u'جستجو در پاسخ سوالات. دقت کنید که اشتراک این فیلد با سایر فیلدها به عنوان نتیجه بازگردانده می شود.', label=u'پاسخ', max_length=150, required=False, widget=forms.TextInput(
            attrs={'class': 'search-tab-content-input input-12', 'placeholder': u'محتوی پاسخ:'}))
        answered = forms.ChoiceField(help_text=u'دسته بندی سوالات بر اساس وجود یا عدم پاسخ.دقت کنید که اشتراک این فیلد با سایر فیلدها به عنوان نتیجه باز گردانده می وشد.', label=u'وضعیت پاسخ', required=False, choices=(
            ('', u'وضعیت پاسخ'), (True, u'پاسخ داده شده'), (False, u'پاسخ داده نشده'), ))

        both = forms.CharField(help_text=u'جستجو در بین عناوین و پاسخ ها. اگر می خواهید از این فیلد استفاده کنید سایر فیلدهای جستجوی پیشرفته را خالی بگذارید.', label=u'جستجو کلی', max_length=100, required=False, widget=forms.TextInput(
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
        if both:
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
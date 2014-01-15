# -*- coding: utf-8 -*

from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from juck.articles.models import Article


class ArticleListFilter:
    class SecretaryArticleListFilterForm(forms.Form):

        from_date = forms.DateField(required=False, widget=forms.DateInput)
        to_date = forms.DateField(required=False, widget=forms.DateInput)
        title = forms.CharField(label=u'عنوان', max_length=100, required=False, widget=forms.TextInput(
            attrs={'class': 'search-tab-content-input input-12', 'placeholder': u'عنوان یا متن'}))
        dl_count = forms.IntegerField(required=False, widget=forms.TextInput)

    Form = SecretaryArticleListFilterForm

    def init_filter(self, GET_dict, **kwargs):
        self.form = self.Form(GET_dict)

        filter_kwargs = kwargs

        if self.form.is_valid():
            title = self.form.cleaned_data.get('title', '')
            answer = self.form.cleaned_data.get('answer', '')

            if title:
                filter_kwargs.update({'title__icontains': title})
            if answer:
                filter_kwargs.update({'answer__content__icontains': answer})

        questions = Article.objects.filter(**filter_kwargs)
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

# -*- coding: utf-8 -*

from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from django.db.models.query_utils import Q
from juck.articles.models import Article


class ArticleListFilter:
    class SecretaryArticleListFilterForm(forms.Form):

        #from_date = forms.DateField(required=False, widget=forms.DateInput)
        #to_date = forms.DateField(required=False, widget=forms.DateInput)
        both = forms.CharField(help_text=u'جستجو در عناوین و خلاصه مقالات. در صورت استفاده از این فیلد سایر فیلد ها را خالی بگذارید.', label=u'جستجو کلی', max_length=150,
                               required=False, widget=forms.TextInput(attrs={'placeholder': u'جستجو'}))
        title = forms.CharField(help_text=u'جستجو در عناوین مقالات', label=u'عنوان', max_length=100, required=False, widget=forms.TextInput(
            attrs={'class': 'search-tab-content-input input-12', 'placeholder': u'عنوان'}))
        summary = forms.CharField(label=u'جستجو در خلاصه مقالات', max_length=100, required=False, widget=forms.TextInput(
            attrs={'class': 'search-tab-content-input input-12', 'placeholder': u'خلاصه'}))
        dl_count = forms.IntegerField(help_text=u'مقالاتی که حداقل به این تعداد دانلود شده اند.' , required=False, widget=forms.TextInput(attrs={
            'placeholder': u'بار'
        }))
        author = forms.CharField(help_text=u'مقالاتی که شخص مورد نظر از نویسندگان آن است.',  label=u'نویسنده', required=False, widget=forms.TextInput())
        tag = forms.CharField(help_text=u'مقالاتی که برچسپ مورد نظر را دارند.', label=u'برچسب', required=False, widget=forms.TextInput())

    Form = SecretaryArticleListFilterForm

    def init_filter(self, GET_dict, **kwargs):
        self.form = self.Form(GET_dict)

        filter_kwargs = kwargs

        if self.form.is_valid():
            both = self.form.cleaned_data.get('both', '')
            title = self.form.cleaned_data.get('title', '')
            summary = self.form.cleaned_data.get('summary', '')
            dl_count = self.form.cleaned_data.get('dl_count', '')
            author = self.form.cleaned_data.get('author', '')
            tag = self.form.cleaned_data.get('tag', '')

            if title:
                filter_kwargs.update({'title__icontains': title})
            if summary:
                filter_kwargs.update({'title__summary': summary})
            if dl_count:
                filter_kwargs.update({'downloads_count__gte': int(dl_count)})
            if author:
                filter_kwargs.update({'authors': author})
            if tag:
                filter_kwargs.update({'tags': tag})
        articles = Article.objects.filter(**filter_kwargs)

        articles = articles.filter((Q(title__icontains=both) | Q(summary__icontains=both)))
        count = articles.count()

        articles = articles.order_by('-publish_date')
        paginator = Paginator(articles, settings.RESULTS_PER_PAGE)
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

# -*- coding: utf-8 -*-

from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from juck.news.models import News
from juck.question.models import Question
from django.db.models import Q


class NewsListFilter:
    class SecNewsListFilterForm(forms.Form):

        content = forms.CharField(label=u'جستجو کلی', max_length=150, required=False,
                                  help_text=u'این متن در بین عنوان ها و متن اخبار جستجو می گردد.',
                                  widget=forms.TextInput(
                                      attrs={'placeholder': u'جستجو'}))

        title = forms.CharField(label=u'عنوان', max_length=150, required=False,
                                help_text=u'عنوان کامل و یا بخشی از عنوان خبر که در جستجوی آن هستید را در این جا وارد کنید. دقت کنید که جواب های به دست آمده از این قسمت با قسمت های دیگر اشتراک گرفته می شود.',
                                widget=forms.TextInput(
                                    attrs={'placeholder': u'عنوان خبر'}))

        description = forms.CharField(label=u'توضیحات', max_length=150, required=False,
                                      help_text=u'متن کامل و یا بخشی از متن  خبر که در جستجوی آن هستید را در این جا وارد کنید. دقت کنید که جواب های به دست آمده از این قسمت با قسمت های دیگر اشتراک گرفته می شود.',
                                      widget=forms.Textarea(
                                          attrs={'placeholder': u'توضیحات'}))
        #from_date = forms.DateField(label=u'از تاریخ', required=False,widget=forms.DateField )
        #to_date = forms.DateField(label=u'تا تاریخ', required=False,widget=forms.DateField )

        min_score = forms.CharField(label=u'حداقل امتیاز', required=False,
                                    help_text=u'حداقل امتیازی که برای یک خبر در نظر دارید را در این محل وارد کنید. دقت کنید که جواب های به دست آمده از این قسمت با قسمت های دیگر اشتراک گرفته می شود.', )
        max_score = forms.CharField(label=u'حداکثر امتیاز', required=False,
                                    help_text=u'حداکثر امتیازی که برای یک خبر در نظر دارید را در این محل وارد کنید. دقت کنید که جواب های به دست آمده از این قسمت با قسمت های دیگر اشتراک گرفته می شود.')


        #answer = forms.CharField(label=u'پاسخ', max_length=150, required=False, widget=forms.TextInput(
        #    attrs={'class': 'search-tab-content-input input-12', 'placeholder': u'محتوی پاسخ:'}))
        #answered = forms.ChoiceField(label=u'وضعیت پاسخ', required=False, choices=(
        #    ('', u'وضعیت پاسخ'), (True, u'پاسخ داده شده'), (False, u'پاسخ داده نشده'), ))

    Form = SecNewsListFilterForm

    def init_filter(self, GET_dict, **kwargs):
        self.form = self.Form(GET_dict)

        filter_kwargs = kwargs

        if self.form.is_valid():
            content = self.form.cleaned_data.get('content', '')
            title = self.form.cleaned_data.get('title', '')
            description = self.form.cleaned_data.get('description', '')
            #from_date = self.form.cleaned_data.get('from_date', '')
            #to_date = self.form.cleaned_data.get('to_date', '')

            min_score = self.form.cleaned_data.get('min_score', '')
            max_score = self.form.cleaned_data.get('max_score', '')

            res = News.objects.all()
            #if content:
            #    filter_kwargs.update({'title__icontains': content})
            #res = res.filter(Q(description__icontains= content))

            if title:
                filter_kwargs.update({'title__icontains': title})
                #res = res.filter(Q(title__icontains= content))
            if description:
                filter_kwargs.update({'content__icontains': description})
                #res = res.fi
            #if not (title or description):
            #    #res = News.objects.filter(Q(title__icontains=content) | (Q(content__icontains=content)))
            #    filter_kwargs.update( Q(title__icontains=content) | (Q(content__icontains=content)))
            #if from_date:
            #    filter_kwargs.update({'publish_date__gte': from_date})
            #if to_date:
            #    filter_kwargs.update({'answer__content__icontains': to_date})
            if min_score:
                filter_kwargs.update({'score__gte': min_score})
            if max_score:
                filter_kwargs.update({'score__lte': max_score})

        # filter_kwargs.update( Q(title__icontains=content) | (Q(content__icontains=content)))
        # filter_kwargs.update({'title__icontains': content})
        news = News.objects.filter(**filter_kwargs)
        news = news.filter((Q(title__icontains=content) | Q(content__icontains=content)))
        count = news.count()

        news = news.order_by('-publish_date')
        paginator = Paginator(news, settings.RESULTS_PER_PAGE)
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
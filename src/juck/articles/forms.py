# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import Article, ArticleSubmission


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        exclude = ['downloads_count', 'tags', 'authors']

    help_texts = {
        'title': (u'عنوان مقاله ای را که می خواهید بارگذاری کنید در اینجا وارد کنید.'),
        'summary': (u'خلاصه مقاله ای را که می خواهید بارگذاری کنید در اینجا وارد کنید. ')
    }

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = u'عنوان'
        self.fields['summary'].widget.attrs['placeholder'] = u'خلاصه مقاله'
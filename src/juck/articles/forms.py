# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import Article


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        exclude = ['downloads_count', 'Tag', 'Author', 'source_file']

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = u'عنوان'
        self.fields['summary'].widget.attrs['placeholder'] = u'حداکثر ۸۰۰ کاراکتر'

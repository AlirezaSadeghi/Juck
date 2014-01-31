# -*- coding: utf-8 -*-

from django import forms
from juck.news.models import News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']

    help_texts = {
        'title': (u'عنوان خبر را در این جا وارد کنید.'),
    }
    # fields['title'].he

    #image = forms.ImageField





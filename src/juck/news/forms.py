# -*- coding: utf-8 -*-

from django import forms
from juck.news.models import News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content' ]

    #image = forms.ImageField





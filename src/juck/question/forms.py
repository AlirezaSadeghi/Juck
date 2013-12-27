# -*- coding: utf-8 -*-

# Nothing so far :D

from django.forms import ModelForm
from models import Question, Answer


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        exclude = ['sender', 'common', 'authors']

    # def __init__(self, *args, **kwargs):
    #     super(QuestionForm, self).__init__(*args, **kwargs)
    #     self.fields['title'].widget.attrs['type'] = 'text'
    #     self.fields['content'].widget.attrs['placeholder'] = u'خلاصه مقاله'


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        exclude = ['responder']
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

    help_texts = {
        'title': (u'عنوان سوال خود را در اینجا وارد کنید. عنوان سوال باید به اختصار موضوع را بیان کند.'),
        'content': (u'شرح سوال را در اینجا وارد کنید.'),
    }

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        exclude = ['responder']

    help_text = {
        'content' : (u'پاسخ سوال را مربوط را در اینجا وارد کنید.')
    }
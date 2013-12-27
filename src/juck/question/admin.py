from models import *
from django.contrib import admin


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'sender', 'issue_time', 'common', 'disabled')
    list_filter = ('sender', 'common', 'disabled')

    search_fields = ('title', 'sender', 'answer__content')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('responder', 'question', 'response_time', 'disabled')
    list_filter = ('responder', 'disabled')

    search_fields = ('responder', 'question__title', 'content')


admin.site.register(Question, QuestionAdmin)
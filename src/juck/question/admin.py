from models import *
from django.contrib import admin


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'sender', 'timestamp', 'common', )
    list_filter = ('sender', 'common', )

    search_fields = ('title', 'sender', 'answer__content', )


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('responder', 'question', 'timestamp', )
    list_filter = ('responder', )

    search_fields = ('responder', 'question__title', 'content')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
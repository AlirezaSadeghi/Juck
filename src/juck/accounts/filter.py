# # -*- coding: utf-8 -*-
#
# from django import forms
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from django.conf import settings
# from juck.acccounts.models import
#
#
# class ManagerUserListFilter:
#     class ManagerUserListFilterForm(forms.Form):
#
#
#         title = forms.CharField(label=u'عنوان', max_length=150, required=False, widget=forms.TextInput(
#             attrs={'class': 'search-tab-content-input input-12', 'placeholder': u'عنوان سوال:'}))
#         answer = forms.CharField(label=u'پاسخ', max_length=150, required=False, widget=forms.TextInput(
#             attrs={'class': 'search-tab-content-input input-12', 'placeholder': u'محتوی پاسخ:'}))
#         answered = forms.ChoiceField(label=u'وضعیت پاسخ', required=False, choices=(
#             ('', u'وضعیت پاسخ'), (True, u'پاسخ داده شده'), (False, u'پاسخ داده نشده'), ))
#
#     Form = ManagerUserListFilterForm
#
#     def init_filter(self, GET_dict, **kwargs):
#         self.form = self.Form(GET_dict)
#
#         filter_kwargs = kwargs
#
#         if self.form.is_valid():
#             title = self.form.cleaned_data.get('title', '')
#             answer = self.form.cleaned_data.get('answer', '')
#             answered = self.form.cleaned_data.get('answered', '')
#
#             if title:
#                 filter_kwargs.update({'title__icontains': title})
#             if answered:
#                 filter_kwargs.update({'answer__isnull': True if answered == u'False' else False})
#             if answer:
#                 filter_kwargs.update({'answer__content__icontains': answer})
#
#         questions = Question.objects.filter(**filter_kwargs)
#         count = questions.count()
#
#         questions = questions.order_by('-issue_time')
#         paginator = Paginator(questions, settings.RESULTS_PER_PAGE)
#         page = GET_dict.get('page')
#
#         try:
#             result = paginator.page(page)
#         except PageNotAnInteger:
#             result = paginator.page(1)
#         except EmptyPage:
#             result = paginator.page(paginator.num_pages)
#
#         return result, count
#
#     def get_form(self):
#         return self.form
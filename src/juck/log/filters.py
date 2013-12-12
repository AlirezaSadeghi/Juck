# -*- coding: utf-8 -*-

from django     import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from jaber.log.models import ActionLog
from django.conf        import settings

class ActionLogListFilter:

    class ActionLogListFilterForm(forms.Form):
        username        = forms.CharField(label=u'نام کاربری',max_length=200, required=False, widget=forms.TextInput(attrs={'class':'search-tab-content-input input-12', 'placeholder': u'نام کاربری'}))
        action_flag     = forms.CharField(label=u'نوع واقعه', max_length=40, required=False, widget=forms.Select(attrs={'class': 'checkbox'}, choices=(('', u'نوع رخداد'), (1, u'اعمال حذف'), (2, u'اعمال تغییر'), (3, u'اعمال افزودن'), (4, u'اعمال دیگر'))))
        description     = forms.CharField(label=u'توضیحات', max_length=150, required=False, widget=forms.TextInput(attrs={'class':'search-tab-content-input input-12', 'placeholder': u'توضیحات'}))

    Form        = ActionLogListFilterForm

    def init_filter(self, GET_dict, **kwargs):
        self.form       = self.Form(GET_dict)

        filter_kwargs   = kwargs

        if self.form.is_valid():
            action_flag     = self.form.cleaned_data.get('action_flag', '')
            description     = self.form.cleaned_data.get('description', '')
            username        = self.form.cleaned_data.get('username', '')

            if username.strip():
                filter_kwargs.update({'user__username__icontains': username})
            if action_flag:
                filter_kwargs.update({'action_flag':action_flag})
            if description:
                filter_kwargs.update({'description__icontains': description})

        log_items       = ActionLog.objects.filter(**filter_kwargs).order_by('-action_time')

        paginator       = Paginator(log_items, settings.RESULTS_PER_PAGE)
        page            = GET_dict.get('page')

        try:
            result      = paginator.page(page)
        except PageNotAnInteger:
            result      = paginator.page(1)
        except EmptyPage:
            result      = paginator.page(paginator.num_pages)

        return result


    def get_form(self):
        return self.form
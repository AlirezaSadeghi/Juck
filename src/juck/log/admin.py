# -*- coding: utf-8 -*-
from django.contrib     import admin
from models             import *
from django.utils.translation import ugettext_lazy as _
from persian_date.gregorian_persian_convertor import create_persian_date


class ActionFlagListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('action flag')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'action_flag'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('1', _(u'اعمال حذف')),
            ('2', _(u'اعمال تغییر')),
            ('3', _(u'اعمال افزودن')),
            ('4', _(u'اعمال متفرقه')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == '1':
            return queryset.filter(action_flag=1)
        if self.value() == '2':
            return queryset.filter(action_flag=2)
        if self.value() == '3':
            return queryset.filter(action_flag=3)
        if self.value() == '4':
            return queryset.filter(action_flag=4)

class ActionLogAdmin(admin.ModelAdmin):

    list_display    = ('user', 'get_persian_date', 'ip_address', 'description', 'content_object', 'object_id',)
    list_filter     = (ActionFlagListFilter, 'content_type',)
    search_fields   = ('user__username', 'user__first_name', 'user__last_name', 'description', )

    def get_persian_date(self, obj):
        time = obj.action_time.time()
        year, month, day = create_persian_date(obj.action_time.date())
        return '%s/%s/%s در ساعت %s' %(year, month, day, time)

    get_persian_date.short_description = u'زمان وقوع '


admin.site.register(ActionLog, ActionLogAdmin)
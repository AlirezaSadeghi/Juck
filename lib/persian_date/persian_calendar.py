# -*- coding: utf-8 -*-
from django         import forms
import datetime
from django.core    import validators
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from gregorian_persian_convertor import create_persian_date
from persian_date.gregorian_persian_convertor import create_gregorian_date


class PersianDateWidget(forms.DateInput):

    def render(self, name, value, attrs=None):
        input_html      = super(PersianDateWidget, self).render(name=name, value=self.get_value(value), attrs=attrs)
        rendered_html   = '<div class="date-input">' + input_html + '</div>'
        return mark_safe(rendered_html)

    def get_value(self, value):

        if isinstance(value, datetime.datetime):
            date        = value.date()
        elif isinstance(value, datetime.date):
            date        = value
        else:
            return value

        year, month, day = create_persian_date(date)
        p_date  = str(year) + " - " + str(month) + " - " + str(day)
        return p_date



class PersianDateField(forms.DateField):

    widget = PersianDateWidget

    default_error_messages = {
        u'FormatError': u'تاریخ وارد شده دارای فرمت صحیح نمی باشد'
    }


    def to_python(self, value):
        if value in validators.EMPTY_VALUES:
            return None
        if isinstance(value, datetime.datetime):
            return value.date()
        if isinstance(value, datetime.date):
            return value

        # Stuff for Persian Date
        try:
            ymd = value.split(value, " - ")
            year = int(ymd[0])
            month = int(ymd[1])
            day = int(ymd[2])
            return create_gregorian_date(year, month, day)
        except ValidationError:
            raise ValidationError(self.default_error_messages[u'FormatError'])


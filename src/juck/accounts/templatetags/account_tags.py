# -*- coding: utf-8 -*-=
from django.template import Library
from juck.accounts  import views
from persian_date.gregorian_persian_convertor import create_persian_date
from datetime import datetime

register = Library()


@register.assignment_tag(takes_context=True)
def get_user_type(context):
    user = context['user']
    return views.get_user_type(user.pk)


MONTHS = (
    u"فروردين", u"ارديبهشت", u"خرداد", u"تير", u"مرداد", u"شهريور", u"مهر", u"آبان", u"آذر", u"دي", u"بهمن", u"اسفند")


@register.simple_tag
def get_sex_rep(sex):
    if sex:
        return u'مرد'
    if sex is False:
        return u'زن'
    return u'دیگر'


@register.simple_tag
def get_hash_date(date):
    year, month, day = create_persian_date(date)
    return year * 1000 + month * 100 + day


@register.simple_tag
def get_current_pdate():
    date = datetime.now().date()
    return get_persian_date(date)


@register.simple_tag
def get_item_pdate(date):
    if not date:
        return ' --- '
    return get_persian_date(date)


@register.simple_tag
def get_persian_date(date):
    if isinstance(date, type('str')):
        return ' --- '

    year, month, day = create_persian_date(date)
    return u"%d %s %d" % (day, MONTHS[month - 1], year)
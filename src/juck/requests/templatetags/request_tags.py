# -*- coding: utf-8 -*-=

from django.template import Library
from juck.accounts.models import Employer
from juck.accounts.views import get_user_type
from persian_date.gregorian_persian_convertor import create_persian_date
from datetime import datetime


register = Library()

MONTHS = (
    u"فروردين", u"ارديبهشت", u"خرداد", u"تير", u"مرداد", u"شهريور", u"مهر", u"آبان", u"آذر", u"دي", u"بهمن", u"اسفند")


@register.simple_tag
def get_request_sender(item, req_type, response):
    if req_type == 'ejo':
        return item.employer.profile.company_name
    elif req_type == 'jso':
        return item.sender.get_full_name()
    elif req_type == 'jo':
        return response.thread.responder.get_full_name()

    return u'نا مشخص'

@register.simple_tag
def get_request_receiver(item, req_type, response):
    if req_type == 'ejo':
        return item.js_receiver.get_full_name() if item.js_receiver else item.em_receiver.get_full_name()
    if req_type == 'jso':
        return item.employer.profile.company_name
    if req_type == 'jo':
        return item.employer.profile.company_name

    return u'نا مشخص'

@register.simple_tag
def get_request_type(req_type):
    if req_type in ['jso', 'ejo']:
        return u'پیشنهاد همکاری'
    elif req_type == 'jo':
        return u'فرصت شغلی'

    return u'نا مشخص'

@register.simple_tag
def get_user_rep(user):
    if get_user_type(user.pk) == 'employer':
        return Employer.objects.get(pk=user.pk).profile.company_name
    return user.get_full_name()


@register.simple_tag
def get_alert_info(item):
    if item.status is False:
        return 'negative'
    if item.status is True:
        return 'positive'
    return 'warning'

@register.simple_tag
def get_request_status(item):
    if item.status is False:
        return u'در شده'
    if item.status is True:
        return u'تایید شده'
    return u'در حال بررسی'


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
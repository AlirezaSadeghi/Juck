# -*- coding: utf-8 -*-
from django.db import models
from model_utils.managers import InheritanceManager

from juck.accounts.models import Employer, JuckUser


class Request(models.Model):
    class Meta:
        verbose_name = u'درخواست'
        verbose_name_plural = u'درخواست ها'

    employer = models.ForeignKey(Employer, verbose_name=u'کارفرما', related_name='requests')
    title = models.CharField(max_length=250, verbose_name=u'عنوان')
    content = models.TextField(verbose_name=u'متن درخواست')
    timestamp = models.DateTimeField(verbose_name=u'زمان ایجاد', auto_now=True)
    cooperation_type = models.PositiveSmallIntegerField(verbose_name=u'نوع همکاری', blank=True, null=True)
    status = models.NullBooleanField(verbose_name=u'وضعیت تایید', null=True, blank=True)

    objects = InheritanceManager()

    def __unicode__(self):
        return self.title


class JobOpportunity(Request):
    class Meta:
        verbose_name = u'آگهی'
        verbose_name_plural = u'آگهی ها'

    first_major = models.CharField(max_length=200, verbose_name=u'رشته تحصیلی', )
    second_major = models.CharField(max_length=200, verbose_name=u'رشته تحصیلی', null=True, blank=True)
    certificate = models.CharField(max_length=100, verbose_name=u'مدرک تحصیلی', null=True, blank=True)
    sex = models.NullBooleanField(verbose_name=u'جنسیت', null=True, blank=True)


class JobOffer(Request):
    class Meta:
        verbose_name = u'پیشنهاد کاری'
        verbose_name_plural = u'پیشنهادات کاری'

    JS_TO_EMPLOYER = 1
    EMPLOYER_TO_JS = 2
    EMPLOYER_TO_EMPLOYER = 3

    sender = models.ForeignKey(JuckUser, verbose_name=u'فرستنده', related_name='sent_offers')
    direction = models.PositiveSmallIntegerField(verbose_name=u'از - به', default=JS_TO_EMPLOYER)


class Response(models.Model):
    class Meta:
        verbose_name = u'پاسخ به درخواست'
        verbose_name_plural = u'پاسخ ها به درخواست ها'

    request = models.ForeignKey(Request, verbose_name=u'درخواست', related_name='responses')
    timestamp = models.DateField(verbose_name=u'زمان ارسال پاسخ', auto_now=True)
    content = models.TextField(verbose_name=u'متن درخواست')




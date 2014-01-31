# -*- coding: utf-8 -*-
from django.db import models
from model_utils.managers import InheritanceManager

from juck.accounts.models import Employer, JuckUser, JobSeeker


class Request(models.Model):
    class Meta:
        verbose_name = u'درخواست'
        verbose_name_plural = u'درخواست ها'


    COOPERATION_TYPES = {'full_time': 1, 'half_time': 2, 'tele_work': 3}

    employer = models.ForeignKey(Employer, verbose_name=u'کارفرما', related_name='requests')
    title = models.CharField(max_length=250, verbose_name=u'عنوان')
    content = models.TextField(verbose_name=u'متن درخواست')
    timestamp = models.DateTimeField(verbose_name=u'زمان ایجاد', auto_now=True)
    cooperation_type = models.PositiveSmallIntegerField(verbose_name=u'نوع همکاری', blank=True, null=True)
    status = models.NullBooleanField(verbose_name=u'وضعیت تایید', null=True, blank=True)

    objects = InheritanceManager()

    def cast(self):
        for name in dir(self):
            try:
                attr = getattr(self, name)
                if isinstance(attr, self.__class__):
                    return attr
            except:
                pass
        return self

    def __unicode__(self):
        return self.title


class JobOpportunity(Request):
    class Meta:
        verbose_name = u'آگهی'
        verbose_name_plural = u'آگهی ها'

    first_major = models.CharField(max_length=200, verbose_name=u'رشته تحصیلی اول', )
    second_major = models.CharField(max_length=200, verbose_name=u'رشته تحصیلی دوم', null=True, blank=True)
    certificate = models.CharField(max_length=100, verbose_name=u'مدرک تحصیلی', null=True, blank=True)
    sex = models.NullBooleanField(verbose_name=u'جنسیت', null=True, blank=True)


class EmployerJobOffer(Request):
    class Meta:
        verbose_name = u'پیشنهاد کاری کارفرما'
        verbose_name_plural = u'پیشنهادات کاری کارفرمایان'

    em_receiver = models.ForeignKey(Employer, verbose_name=u'دریافت کننده کارفرما', related_name='received_offers',
                                    blank=True, null=True)
    js_receiver = models.ForeignKey(JobSeeker, verbose_name=u'دریافت کننده کارجو', related_name='received_offers',
                                    blank=True, null=True)


class JobseekerJobOffer(Request):
    class Meta:
        verbose_name = u'پیشنهاد کاری کارجو'
        verbose_name_plural = u'پیشنهادات کاری کارجویان'

    sender = models.ForeignKey(JobSeeker, verbose_name=u'فرستنده', related_name='sent_offers')


class DiscussionThread(models.Model):
    request = models.ForeignKey(Request, verbose_name=u'درخواست', related_name='dashboard_items')
    responder = models.ForeignKey(JuckUser, verbose_name=u'فرد دوم مکالمه')


class Response(models.Model):
    class Meta:
        verbose_name = u'پاسخ به درخواست'
        verbose_name_plural = u'پاسخ ها به درخواست ها'

    thread = models.ForeignKey(DiscussionThread, verbose_name=u'مکالمات', related_name='responses')
    timestamp = models.DateTimeField(verbose_name=u'زمان ارسال پاسخ', auto_now=True)
    content = models.TextField(verbose_name=u'متن درخواست')
    user = models.ForeignKey(JuckUser, verbose_name=u'کاربر پاسخ‌دهنده', related_name='responses')
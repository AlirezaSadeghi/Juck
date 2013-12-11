# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.contenttypes import generic
from juck.accounts.models import JuckUser


class ActionLog(models.Model):

    DELETE_FLAG = 1
    CHANGE_FLAG = 2
    ADD_FLAG = 3
    OTHERS_FLAG = 4

    class Meta:
        verbose_name        = u'لاگ'
        verbose_name_plural = u'لاگ‌ها'

    user        = models.ForeignKey(JuckUser, verbose_name=u'کاربر')
    ip_address  = models.CharField(max_length=150, verbose_name=u'آدرس آی‌پی کاربر')

    description = models.CharField(verbose_name=u'توضیحات لاگ', max_length=250, null=True, blank=True)
    action_time = models.DateTimeField(verbose_name=u'زمان وقوع', auto_now=True)
    action_flag = models.PositiveSmallIntegerField(verbose_name=u'توع لاگ')

    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(verbose_name=u'کلید اصلی', null=True, blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    disabled    = models.BooleanField(default=False, verbose_name=u'حذف شده است ؟')

    def __unicode__(self):
        return self.user.get_full_name() + self.description

    def action_flag_display(self):
        if self.action_flag == 1:
            return u'حذف'
        if self.action_flag == 2:
            return u'تغییر'
        if self.action_flag == 3:
            return u'افزودن'
        return u'متفرقه'
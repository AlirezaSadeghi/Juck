# -*- coding: utf-8 -*-
from django.db import models

from juck.accounts.models import Employer


class Request(models.Model):
    class Meta:
        verbose_name = u'درخواست'
        verbose_name_plural = u'درخواست ها'

    employer = models.ForeignKey(Employer, verbose_name=u'کارفرما', related_name='reuqests')
    title = models.CharField(max_length=250, verbose_name=u'عنوان')
    text = models.TextField(verbose_name=u'متن درخواست')
    timestamp = models.DateTimeField(verbose_name=u'زمان ایجاد')
    cooperation_type = models.PositiveSmallIntegerField(verbose_name=u'نوع همکاری', )


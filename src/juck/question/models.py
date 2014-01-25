# -*- coding: utf-8 -*-
from django.db import models
from juck.accounts.models import Manager, JuckUser


class Question(models.Model):
    class Meta:
        verbose_name = u'سوال'
        verbose_name_plural = u'سوالات'

    sender = models.ForeignKey(JuckUser, verbose_name=u'کاربر فرستنده', related_name='questions')
    title = models.CharField(verbose_name=u'عنوان', max_length=200)
    timestamp = models.DateTimeField(u'زمان پرسیده شدن', auto_now=True)
    common = models.BooleanField(u'سوال متداول', default=False)
    content = models.TextField(u'محتوی', null=True, blank=True)

    def __unicode__(self):
        return self.sender.email + u' ' + self.title


class Answer(models.Model):
    class Meta:
        verbose_name = u'پاسخ سوال'
        verbose_name_plural = u'پاسخ سوالات'

    responder = models.ForeignKey(Manager, verbose_name=u'مدیر  سایت', related_name='answers')
    question = models.OneToOneField(Question, verbose_name=u'سوال', related_name='answer')
    timestamp = models.DateTimeField(u'زمان پاسخ داده شدن', auto_now=True)
    content = models.TextField(u'پاسخ')

    def __unicode__(self):
        return u'پاسخ ' + self.responder.email + u' ' + self.question.title
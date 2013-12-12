# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
from juck.accounts.models import Manager
from juck.image.models import JuckImage
from persian_date.gregorian_persian_convertor import create_persian_date


class News(models.Model):

    class Meta:
        verbose_name = u'خبر'
        verbose_name_plural = u'اخبار'

    title = models.CharField(max_length=200, verbose_name=u'عنوان')
    content = models.TextField(verbose_name=u'متن خبر')
    publish_date = models.DateTimeField(verbose_name=u'زمان انتشار', auto_now=True)
    author = models.ForeignKey(Manager, verbose_name=u'نویسنده', related_name='news')
    image  = models.ForeignKey(JuckImage, verbose_name=u'عکس', null=True, blank=True)

    def __unicode__(self):
        return u'خبر: ' + self.title

    def get_persian_date(self):
        tup = create_persian_date(self.publish_date.date())
        return tup

    def calculate_score(self):
        pass

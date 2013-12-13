# -*- coding: utf-8 -*-
from django.db import models
from persian_date.gregorian_persian_convertor import create_persian_date

# Create your models here.


class Article(models.Model):

    class Meta:
        verbose_name = u'مقاله'
        verbose_name_plural = u'مقالات'

    title = models.CharField(max_length=200, verbose_name=u'عنوان')
    summary = models.TextField(verbose_name=u'خلاصه')
    publish_date = models.DateTimeField(verbose_name=u'زمان انتشار', auto_now=True)
    source_file = models.FileField(max_length=200, verbose_name=u'فایل')
    downloads_count = models.IntegerField(default=0, verbose_name=u'دفعات بارگیری')
    tags
    authors


class Tag:



    def __unicode__(self):
        return u'مقاله: ' + self.title

    def get_persian_date(self):
        tup = create_persian_date(self.publish_date.date())
        return tup

    def calculate_score(self):
        pass
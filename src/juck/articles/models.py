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
    tags = models.ManyToManyField(Tag, through='Article_tags')
    authors = models.ManyToManyField(Author, through='Article_authors')

    def __unicode__(self):
        return u'مقاله: ' + self.title

    def get_persian_date(self):
        tup = create_persian_date(self.publish_date.date())
        return tup

    def calculate_score(self):
        pass


class Tag(models.Model):

    class Meta:
        verbose_name = u'برچسب'
        verbose_name_plural = u'برچسب ها'

    name = models.CharField(max_length=200, verbose_name=u'نام')


class Author(models.Model):

    class Meta:
        verbose_name = u'نویسنده'
        verbose_name_plural = u'نویسندگان'

    full_name = models.CharField(max_length=200, verbose_name=u'نام و نام خانوادگی')


class Article_tags(models.Model):
    tag = models.ForeignKey(Tag)
    article = models.ForeignKey(Article)


class Article_authors(models.Model):
    author = models.ForeignKey(Author)
    article = models.ForeignKey(Article)

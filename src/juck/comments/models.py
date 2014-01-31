# -*- coding: utf-8 -*-

from django.db import models
from juck.accounts.models import JuckUser, JobSeeker, Employer
from juck.articles.models import Article
from juck.news.models import News
from persian_date.gregorian_persian_convertor import create_persian_date


MONTHS = (
    u"فروردين", u"ارديبهشت", u"خرداد", u"تير"
    , u"مرداد", u"شهريور", u"مهر", u"آبان", u"آذر", u"دي", u"بهمن", u"اسفند", )


# Create your models here.
class JobSeekerComment(models.Model):
    class Meta:
        ordering = ('date_created',)
        verbose_name = u'نظر درمورد کارجو'
        verbose_name_plural = u'نظرات درمورد کارجویان'

    user = models.ForeignKey(JuckUser, verbose_name=u'کاربر')
    content = models.ForeignKey(JobSeeker, verbose_name=u'کارجو', related_name='comments')

    comment = models.CharField(max_length=250, verbose_name=u'نظر')

    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u'زمان ایجاد')

    def __unicode__(self):
        return u' '.join([u'نظر شماره', str(self.id)])

    def get_persian_date(self):
        year, month, day = create_persian_date(self.date_created)
        if self.date_created.time().minute > 9:
            return u"%d %s %d در ساعت %s" % (day, MONTHS[month - 1], year, (
                str(self.date_created.time().hour) + ":" + str(self.date_created.time().minute)))
        else:
            return u"%d %s %d در ساعت %s" % (day, MONTHS[month - 1], year, (
                str(self.date_created.time().hour) + ":" + "0" + str(self.date_created.time().minute)))


class EmployerComment(models.Model):
    class Meta:
        ordering = ('date_created',)
        #TODO change theses shits
        verbose_name = u'نظر درمورد کارجو'
        verbose_name_plural = u'نظرات درمورد کارجویان'

    user = models.ForeignKey(JuckUser, verbose_name=u'کاربر')
    content = models.ForeignKey(Employer, verbose_name=u'کارفرما', related_name='comments')

    comment = models.CharField(max_length=250, verbose_name=u'نظر')

    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u'زمان ایجاد')

    def __unicode__(self):
        return u' '.join([u'نظر شماره', str(self.id)])

    def get_persian_date(self):
        year, month, day = create_persian_date(self.date_created)
        if self.date_created.time().minute > 9:
            return u"%d %s %d در ساعت %s" % (day, MONTHS[month - 1], year, (
                str(self.date_created.time().hour) + ":" + str(self.date_created.time().minute)))
        else:
            return u"%d %s %d در ساعت %s" % (day, MONTHS[month - 1], year, (
                str(self.date_created.time().hour) + ":" + "0" + str(self.date_created.time().minute)))


class ArticleComment(models.Model):
    class Meta:
        ordering = ('date_created',)
        #TODO change theses shits
        verbose_name = u'نظر درمورد کارجو'
        verbose_name_plural = u'نظرات درمورد کارجویان'

    user = models.ForeignKey(JuckUser, verbose_name=u'کاربر')
    content = models.ForeignKey(Article, verbose_name=u'مقاله', related_name='comments')

    comment = models.CharField(max_length=250, verbose_name=u'نظر')

    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u'زمان ایجاد')

    def __unicode__(self):
        return u' '.join([u'نظر شماره', str(self.id)])

    def get_persian_date(self):
        year, month, day = create_persian_date(self.date_created)
        if self.date_created.time().minute > 9:
            return u"%d %s %d در ساعت %s" % (day, MONTHS[month - 1], year, (
                str(self.date_created.time().hour) + ":" + str(self.date_created.time().minute)))
        else:
            return u"%d %s %d در ساعت %s" % (day, MONTHS[month - 1], year, (
                str(self.date_created.time().hour) + ":" + "0" + str(self.date_created.time().minute)))


class NewsComment(models.Model):
    class Meta:
        ordering = ('date_created',)
        #TODO change theses shits
        verbose_name = u'نظر درمورد کارجو'
        verbose_name_plural = u'نظرات درمورد کارجویان'

    user = models.ForeignKey(JuckUser, verbose_name=u'کاربر')
    content = models.ForeignKey(News, verbose_name=u'خبر', related_name='comments')

    comment = models.CharField(max_length=250, verbose_name=u'نظر')

    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u'زمان ایجاد')

    def __unicode__(self):
        return u' '.join([u'نظر شماره', str(self.id)])

    def get_persian_date(self):
        year, month, day = create_persian_date(self.date_created)
        if self.date_created.time().minute > 9:
            return u"%d %s %d در ساعت %s" % (day, MONTHS[month - 1], year, (
                str(self.date_created.time().hour) + ":" + str(self.date_created.time().minute)))
        else:
            return u"%d %s %d در ساعت %s" % (day, MONTHS[month - 1], year, (
                str(self.date_created.time().hour) + ":" + "0" + str(self.date_created.time().minute)))

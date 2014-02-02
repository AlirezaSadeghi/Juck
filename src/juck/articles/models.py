# -*- coding: utf-8 -*-
from django.db import models
from persian_date.gregorian_persian_convertor import create_persian_date
from juck.accounts.models import JuckUser
from django.conf import settings

# Create your models here.

MONTHS = (
    u"فروردين", u"ارديبهشت", u"خرداد", u"تير"
    , u"مرداد", u"شهريور", u"مهر", u"آبان", u"آذر", u"دي", u"بهمن", u"اسفند", )

class Article(models.Model):
    class Meta:
        verbose_name = u'مقاله'
        verbose_name_plural = u'مقالات'

    tags = models.ManyToManyField('Tag')
    authors = models.ManyToManyField('Author')

    title = models.CharField(max_length=200, verbose_name=u'عنوان')
    summary = models.TextField(verbose_name=u'خلاصه')
    publish_date = models.DateTimeField(verbose_name=u'زمان انتشار', auto_now=True)
    source_file = models.FileField(max_length=200, verbose_name=u'فایل', upload_to=settings.MEDIA_ROOT + "articles",
                                   null=True, blank=True)
    downloads_count = models.IntegerField(default=0, verbose_name=u'دفعات بارگیری')

    def __unicode__(self):
        return u'مقاله: ' + self.title

    def get_persian_date(self):
        year, month, day = create_persian_date(self.publish_date)
        if (self.publish_date.time().minute > 9 ):
            return u"%d %s %d در ساعت %s" % (day, MONTHS[month - 1], year, (
            str(self.publish_date.time().hour) + ":" + str(self.publish_date.time().minute)))
        else:
            return u"%d %s %d در ساعت %s" % (day, MONTHS[month - 1], year, (
            str(self.publish_date.time().hour) + ":" + "0" + str(self.publish_date.time().minute)))

    def calculate_score(self):
        pass

    def get_likes(self):
        ratings = self.ratings.all()

        rate = 0
        for item in ratings:
            if item.rate > 0:
                rate += 1

        return rate

    def get_dislikes(self):
        ratings = self.ratings.all()

        rate = 0
        for item in ratings:
            if item.rate < 0:
                rate += 1

        return rate


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


class ArticleSubmission(models.Model):
    class Meta:
        verbose_name = u'مقاله کاربر'
        verbose_name_plural = u'مقاله‌های کاربران'

    article = models.ForeignKey(Article, verbose_name=u'مقاله')
    user = models.ForeignKey(JuckUser, verbose_name=u'کاربر')

    is_accepted = models.BooleanField(verbose_name=u'تایید شده', default=False)
    accept_date = models.DateTimeField(verbose_name=u'زمان تایید', null=True, editable=False)

    def get_persian_date(self):
        year, month, day = create_persian_date(self.publish_date)
        if (self.publish_date.time().minute > 9 ):
            return u"%d %s %d در ساعت %s" % (day, MONTHS[month - 1], year, (
            str(self.publish_date.time().hour) + ":" + str(self.publish_date.time().minute)))
        else:
            return u"%d %s %d در ساعت %s" % (day, MONTHS[month - 1], year, (
            str(self.publish_date.time().hour) + ":" + "0" + str(self.publish_date.time().minute)))

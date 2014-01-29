# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
from juck.accounts.models import Manager
from juck.image.models import JuckImage
from persian_date.gregorian_persian_convertor import create_persian_date

MONTHS = (
    u"فروردين", u"ارديبهشت", u"خرداد", u"تير"
    , u"مرداد", u"شهريور", u"مهر", u"آبان", u"آذر", u"دي", u"بهمن", u"اسفند", )


class News(models.Model):
    class Meta:
        verbose_name = u'خبر'
        verbose_name_plural = u'اخبار'

    title = models.CharField(max_length=200, verbose_name=u'عنوان')
    content = models.TextField(verbose_name=u'متن خبر')
    publish_date = models.DateTimeField(verbose_name=u'زمان انتشار', auto_now=True)
    author = models.ForeignKey(Manager, verbose_name=u'نویسنده', related_name='news')
    image = models.ForeignKey(JuckImage, verbose_name=u'عکس', null=True, blank=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    score = models.IntegerField(default=0)


    def __unicode__(self):
        return u'خبر: ' + self.title

    def get_persian_date(self):
        year, month, day = create_persian_date(self.publish_date)
        if (self.publish_date.time().minute > 9 ):
            return u"%d %s %d در ساعت %s" % (day, MONTHS[month - 1], year, (str(self.publish_date.time().hour)+ ":" + str(self.publish_date.time().minute)))
        else:
            return u"%d %s %d در ساعت %s" % (day, MONTHS[month - 1], year, (str(self.publish_date.time().hour)+ ":" + "0" + str(self.publish_date.time().minute)))

    def calculate_score(self):
        self.score = self.likes - self.dislikes
        #self.save()
        return self.score

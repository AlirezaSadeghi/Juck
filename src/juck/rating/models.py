# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
from juck.accounts.models import Employer, JuckUser, JobSeeker
from juck.articles.models import Article
from juck.news.models import News


class EmployerRating(models.Model):
    class Meta:
        verbose_name = u'اعتبار کارفرما'
        verbose_name_plural = u'اعتبار کارفرمایان'

    employer = models.ForeignKey(Employer, verbose_name=u'کارفرما', related_name=u'ratings')
    user = models.ForeignKey(JuckUser, verbose_name=u'کاربر امتیاز دهنده', related_name=u'rated_employers')
    rate = models.PositiveIntegerField(default=0)


class JobseekerRating(models.Model):
    class Meta:
        verbose_name = u'اعتبار کارفرما'
        verbose_name_plural = u'اعتبار کارفرمایان'

    jobseeker = models.ForeignKey(JobSeeker, verbose_name=u'کارفرما', related_name=u'ratings')
    employer = models.ForeignKey(Employer, verbose_name=u'کارفرما امتیاز دهنده', related_name=u'rated_jobseekers')
    rate = models.PositiveIntegerField(default=0)


class ArticleRating(models.Model):
    class Meta:
        verbose_name = u'اعتبار کارفرما'
        verbose_name_plural = u'اعتبار کارفرمایان'

    article = models.ForeignKey(Article, verbose_name=u'مقاله', related_name=u'ratings')
    user = models.ForeignKey(JuckUser, verbose_name=u'کاربر امتیاز دهنده', related_name=u'rated_articles')
    rate = models.IntegerField(default=0, verbose_name=u'امتیاز')


class NewsRating(models.Model):
    class Meta:
        verbose_name = u'امتیاز خبر'
        verbose_name_plural = u'امتیاز اخبار'

    news = models.ForeignKey(News, verbose_name=u'خبر', related_name='ratings')
    user = models.ForeignKey(JuckUser, verbose_name=u'امتیاز دهنده', related_name='rated_news')
    rate = models.IntegerField(default=0, verbose_name=u'امتیاز')

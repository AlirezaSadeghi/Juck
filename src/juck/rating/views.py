# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from juck.accounts.views import get_user_type
from utils import json_response
from juck.rating.models import *


@login_required()
def add_rate(request):
    if request.method == 'POST':
        obj_type, obj_id, rate = request.POST['obj_type'], request.POST['obj_id'], int(request.POST['rate'])
        user_type = get_user_type(request.user.pk)
        again = True

        if obj_type == 'job_seeker' and user_type == 'employer':
            try:
                user = Employer.objects.get(id=request.user.id)
                js = JobSeeker.objects.get(id=obj_id)
                if not JobseekerRating.objects.filter(jobseeker=js, employer=user):
                    rate = JobseekerRating(rate=rate, jobseeker=js,
                                           employer=user)
                    rate.save()
                    again = False
            except ObjectDoesNotExist:
                return json_response({'op_status': 'failed', 'message': u'چنین کارجویی وجود ندارد.'})

        elif obj_type == 'employer' and user_type in ['employer', 'job_seeker']:
            try:
                user = JuckUser.objects.get(id=request.user.id)
                em = Employer.objects.get(id=obj_id)
                if not EmployerRating.objects.filter(employer=em, user=user):
                    rate = EmployerRating(rate=rate, employer=em,
                                          user=user)
                    rate.save()
                    again = False
            except ObjectDoesNotExist:
                return json_response({'op_status': 'failed', 'message': u'چنین کارفرمایی وجود ندارد.'})

        elif obj_type == 'article' and user_type in ['employer', 'job_seeker']:
            try:
                user = JuckUser.objects.get(id=request.user.id)
                ar = Article.objects.get(id=obj_id)
                if not ArticleRating.objects.filter(user=user, article=ar):
                    rate = ArticleRating(rate=rate, article=ar,
                                         user=user)
                    rate.save()
                    again = False
            except ObjectDoesNotExist:
                return json_response({'op_status': 'failed', 'message': u'چنین مقاله‌ای وجود ندارد.'})

        elif obj_type == 'news' and user_type in ['employer', 'job_seeker']:
            try:
                user = JuckUser.objects.get(id=request.user.id)
                n = News.objects.get(id=obj_id)
                if not NewsRating.objects.filter(user=user, news=n):
                    rate = NewsRating(rate=rate, news=n,
                                      user=user)
                    rate.save()
                    again = False
            except ObjectDoesNotExist:
                return json_response({'op_status': 'failed', 'message': u'چنین خبری وجود ندارد.'})

        else:
            return json_response({'op_status': 'failed', 'message': u'درخواست غیرمجاز'})

        if again:
            return json_response({'op_status': 'failed', 'message': u'قبلا امتیاز داده‌اید.'})

        return json_response({'op_status': 'success', 'message': u'اضافه کردن امتیاز با موفقیت انجام شد.'})

    else:
        return render(request, 'messages.html', {'message':u'دسترسی غیرمجاز'})
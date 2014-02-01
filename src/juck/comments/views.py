# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.template.loader import render_to_string
from utils import json_response
from juck.comments.models import *
import math


def get_comments(request):
    if request.method == 'POST':

        obj_type, obj_id, comments = request.POST['type'], request.POST['id'], ''
        page, page_size = int(request.POST['page']), int(request.POST['page_size'])
        obj_div = request.POST['obj_div']

        # print('everything is here')
        if obj_type == 'job_seeker':
            comments = JobSeekerComment.objects.filter(content__id=obj_id)
        elif obj_type == 'employer':
            comments = EmployerComment.objects.filter(content__id=obj_id)
        elif obj_type == 'article':
            comments = ArticleComment.objects.filter(content__id=obj_id)
        elif obj_type == 'news':
            comments = NewsComment.objects.filter(content__id=obj_id)
        else:
            return json_response({'op_status': 'failed', 'message': u'درخواست نامعتبر'})

        # print('i know my type and i am ready for pagination')
        first_index = (page - 1) * page_size
        last_index = first_index + page_size
        if last_index > len(comments):
            last_index = len(comments)

        comment_list = comments[first_index:last_index]

        # print('pagination done')
        pages = [i + 1 for i in range(int(math.ceil(len(comments) / page_size)))]

        out = {'page': page, 'page_size': page_size, 'obj_id': obj_id, 'obj_type': obj_type,
                            'pages': pages, 'total_results': len(comments), 'comments': comment_list, 'obj_div': obj_div}

        html = render_to_string('comments/comments.html', out)
        res = {'html': html, 'op_status':'success'}
        return json_response(res)

    else:
        return render(request, 'messages.html', {'message': u'دسترسی غیرمجاز'})


@login_required()
def add_comment(request):
    if request.method == 'POST':
        # print('post')
        obj_type, obj_id, comment = request.POST['type'], request.POST['id'], request.POST['comment']
        # print(obj_type+" "+obj_id+" "+comment)
        if obj_type == 'job_seeker':
            try:
                # print('js')
                js = JobSeeker.objects.get(id=obj_id)
                user = JuckUser.objects.get(id=request.user.id)
                cm = JobSeekerComment(user=user, content=js,
                                      comment=comment)
                cm.save()

            except ObjectDoesNotExist:
                return json_response({'op_status': 'failed', 'message': u'چنین کارجویی وجود ندارد.'})
        elif obj_type == 'employer':
            try:
                # print('em')
                em = Employer.objects.get(id=obj_id)
                user = JuckUser.objects.get(id=request.user.id)
                cm = EmployerComment(user=user, content=em,
                                     comment=comment)
                cm.save()

            except ObjectDoesNotExist:
                return json_response({'op_status': 'failed', 'message': u'چنین کارفرمایی وجود ندارد.'})

        elif obj_type == 'article':
            try:
                # print('ar')
                ar = Article.objects.get(id=obj_id)
                user = JuckUser.objects.get(id=request.user.id)
                cm = ArticleComment(user=user, content=ar,
                                      comment=comment)
                cm.save()
            except ObjectDoesNotExist:
                return json_response({'op_status': 'failed', 'message': u'چنین مقاله‌ای وجود ندارد.'})

        elif obj_type == 'news':

            try:
                # print('n')
                n = News.objects.get(id=obj_id)
                user = JuckUser.objects.get(id=request.user.id)
                cm = NewsComment(user=user, content=n,
                                      comment=comment)
                cm.save()
            except ObjectDoesNotExist:
                return json_response({'op_status': 'failed', 'message': u'چنین خبری وجود ندارد.'})
        else:
            return json_response({'op_status': 'failed', 'message': u'درخواست نامعتبر'})


        # print('done')
        return json_response({'op_status': 'success', 'message': u'اضافه کردن نظر با موفقیت انجام شد.'})

    else:
        return render(request, 'messages.html', {'message': u'دسترسی غیرمجاز'})

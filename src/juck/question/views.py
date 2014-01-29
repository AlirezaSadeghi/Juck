# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from juck.accounts.models import Manager, JuckUser
from juck.accounts.views import check_user_type, get_user_type
from juck.question.filter import ManagerQuestionListFilter
from juck.question.models import Question, Answer
from utils import create_pagination_range, json_response
from forms import QuestionForm

@login_required
def ask_question(request):
    if request.is_ajax():
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        sender = request.user
        Question.objects.create(sender=sender, title=title, content=content)
        return json_response({'op_status': 'success', 'redirect': '/question/your_questions/'})

    return json_response({'op_status': 'fail'})


def common_questions(request):
    if request.method == "GET":
        form = QuestionForm()
        get_params = request.GET.copy()
        if 'page' in get_params:
            del get_params['page']

        search_filter = ManagerQuestionListFilter()
        questions, count = search_filter.init_filter(request.GET, **{'common': True})
        search_form = search_filter.get_form()

        page_range = create_pagination_range(questions.number, questions.paginator.num_pages)

        if get_user_type(request.user) == 'manager':
            return render_to_response('question/manager_common_questions.html',
                                      {'questions': questions, 'count': count, 'search_form': search_form,
                                       'page_range': page_range, 'get_params': get_params, 'form': form},
                                      context_instance=RequestContext(request, ))

        return render_to_response('question/common_questions.html',
                                  {'questions': questions, 'count': count, 'search_form': search_form,
                                   'page_range': page_range, 'get_params': get_params},
                                  context_instance=RequestContext(request, ))
    return render_to_response('messages.html', {'message': u'صفحه ی مورد نظر موجود نمی باشد'})


@login_required
@user_passes_test(lambda user: check_user_type(user.pk, 'manager'))
def asked_questions(request):
    if request.method == "GET":
        get_params = request.GET.copy()
        if 'page' in get_params:
            del get_params['page']

        search_filter = ManagerQuestionListFilter()
        questions, count = search_filter.init_filter(request.GET, **{'common': False})
        search_form = search_filter.get_form()

        page_range = create_pagination_range(questions.number, questions.paginator.num_pages)

        return render_to_response('question/asked_questions.html',
                                  {'questions': questions, 'count': count, 'search_form': search_form,
                                   'page_range': page_range, 'get_params': get_params},
                                  context_instance=RequestContext(request))

    return render_to_response('messages.html', {'message': u'صفحه ی مورد نظر موجود نمی باشد'}, context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda user: check_user_type(user.pk, 'manager'))
def answer_question(request):
    if request.is_ajax() and request.POST.get('pk', ''):
        pk = request.POST.get('pk', '')
        delete = request.POST.get('del', False)
        if '_' in pk:
            pk = pk.split('_')[1]
        if not delete:
            answer_cnt = request.POST.get('answer', '')
            try:
                question = Question.objects.get(pk=pk)
                if hasattr(question, 'answer'):
                    answer = question.answer
                else:
                    answer = Answer(question=question)

                answer.responder = Manager.objects.get(pk=request.user.pk)
                answer.content = answer_cnt
                answer.save()

                return json_response({'op_status': 'success'})
            except Exception as e:
                print (e)

        else:
            question = Question.objects.get(pk=pk)
            if hasattr(question, 'answer'):
                question.answer.delete()
            question.delete()
            return json_response({'op_status': 'success'})

    return render_to_response('messages.html', {'message': u'اجازه دسترسی ندارید.'}, context_instance=RequestContext(request,))


@login_required
def your_questions(request):
    if request.method == "GET":
        get_params = request.GET.copy()
        form = QuestionForm()
        if 'page' in get_params:
            del get_params['page']

        search_filter = ManagerQuestionListFilter()
        questions, count = search_filter.init_filter(request.GET,
                                                     **{'common': False, 'sender': request.user})
        search_form = search_filter.get_form()

        page_range = create_pagination_range(questions.number, questions.paginator.num_pages)

        return render_to_response('question/your_questions.html',
                                  {'questions': questions, 'count': count, 'search_form': search_form,
                                   'page_range': page_range, 'get_params': get_params, 'form': form},
                                  context_instance=RequestContext(request))

    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request, ))


@login_required
@user_passes_test(lambda user: check_user_type(user.pk, 'manager'))
def add_common_question(request):
    if request.method == "POST" and request.user:
        title = request.POST.get('title', '')
        ans = request.POST.get('content', '')

        try:
            question = Question.objects.create(title=title, sender=request.user, common=True)
            Answer.objects.create(responder=Manager.objects.get(pk=request.user.pk), question=question, content=ans)
        except Exception as e:
            print (e)

        return json_response(dict(redirect='/question/common/', op_status= 'success'))

    return render_to_response('question/manager_common_questions.html', {}, context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda user: check_user_type(user.pk, 'manager'))
def edit_common_question(request):
    if request.is_ajax():
        pk = request.POST.get('pk', '')
        title = request.POST.get('title', '')
        answer_cnt = request.POST.get('answer', '')

        if pk:
            question = Question.objects.get(pk=pk)
            answer = question.answer

            question.title = title
            answer.content = answer_cnt

            question.save()
            answer.save()

            return json_response({'op_status': 'success'})

    return json_response({'op_status': 'fail'})


@login_required
@user_passes_test(lambda user: check_user_type(user.pk, 'manager'))
def remove_common_question(request):
    if request.is_ajax():
        pk = request.POST.get('pk', '')

        if pk:
            qs = Question.objects.get(pk=pk)
            try:
                ans = qs.answer
                ans.delete()
                qs.delete()
            except Exception as e:
                print (e)

            return json_response({'op_status': 'success'})

    return json_response({'op_status': 'fail'})

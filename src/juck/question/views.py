# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from juck.accounts.models import Manager, JuckUser
from juck.accounts.views import check_user_type
from juck.question.filter import ManagerQuestionListFilter
from juck.question.models import Question, Answer
from utils import create_pagination_range, json_response
from forms import QuestionForm


@login_required
def ask_question(request):
    if request.is_ajax():
        title = request.POST.get('title', '')
        sender = request.user
        Question.objects.create(sender=sender, title=title)
        return json_response({'op_status': 'success'})

    return json_response({'op_status': 'fail'})


def common_questions(request):
    if request.method == "GET":
        get_params = request.GET.copy()
        if 'page' in get_params:
            del get_params['page']

        search_filter = ManagerQuestionListFilter()

        questions, count = search_filter.init_filter(request.GET, **{'common': True})
        search_form = search_filter.get_form()
        page_range = create_pagination_range(questions.number, questions.paginator.num_pages)

        if isinstance(request.user, Manager):
            return render_to_response('question/manager_common_questions.html',
                                      {'questions': questions, 'count': count, 'search_form': search_form,
                                       'page_range': page_range, 'get_params': get_params},
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

    return render_to_response('messages.html', {'message': u'صفحه ی مورد نظر موجود نمی باشد'},
                              context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda user: check_user_type(user.pk, 'manager'))
def answer_question(request):
    if request.is_ajax() and request.POST.get('pk', ''):
        pk = request.POST.get('pk', '')
        if '_' in pk:
            pk = pk.split('_')[1]

        answer_cnt = request.POST.get('answer', '')
        try:
            question = Question.objects.get(pk=pk)
            if hasattr(question, 'answer'):
                answer = question.answer
            else:
                answer = Answer(question=question)

            answer.responder = request.user
            answer.content = answer_cnt
            answer.save()

            return json_response({'op_status': 'success'})
        except Exception:
            pass
    return json_response({'op_status': 'fail'})


@login_required
def your_questions(request):
    if request.method == "GET":
        form = QuestionForm()
        # get_params = request.GET.copy()
        # if 'page' in get_params:
        #     del get_params['page']
        #
        # search_filter = ManagerQuestionListFilter()
        # questions, count = search_filter.init_filter(request.GET,
        #                                              **{'disabled': False, 'common': False, 'sender': request.user})
        # search_form = search_filter.get_form()
        #
        # page_range = create_pagination_range(questions.number, questions.paginator.num_pages)
        #
        # return render_to_response('question/your_questions.html',
        #                           {'questions': questions, 'count': count, 'search_form': search_form,
        #                            'page_range': page_range, 'get_params': get_params},
        #                           context_instance=RequestContext(request))
        return render_to_response('question/your_questions.html', {'form': form},
                                  context_instance=RequestContext(request))

    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request, ))


@login_required
@user_passes_test(lambda user: check_user_type(user.pk, 'manager'))
def add_common_question(request):
    if request.method == "POST" and request.user:
        title = request.POST.get('title', '')
        ans = request.POST.get('answer', '')

        question = Question.objects.create(title=title, sender=request.user, common=True)
        Answer.objects.create(responder=request.user, question=question, content=ans)

        return HttpResponseRedirect(reverse('common_questions'))

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
            qs.disabled = True

            ans = qs.answer
            ans.disabled = True

            qs.save()
            ans.save()

            return json_response({'op_status': 'success'})

    return json_response({'op_status': 'fail'})

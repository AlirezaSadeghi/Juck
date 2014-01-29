# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from juck.requests.filter import RequestListFilter
from utils import create_pagination_range


def dashboard(request):
    return render_to_response('requests/dashboard.html', {}, context_instance=RequestContext(request, ))


def conversation(request):
    return render_to_response('requests/conversation.html', {}, context_instance=RequestContext(request, ))


def advertisements(request):
    if request.method == "GET":
        get_params = request.GET.copy()
        if 'page' in get_params:
             del get_params['page']

        search_filter = RequestListFilter()
        requests, count = search_filter.init_filter(request.GET, **{'common': True})
        search_form = search_filter.get_form()

        page_range = create_pagination_range(requests.number, requests.paginator.num_pages)

        if request.user.role == 'manager':
             return render_to_response('question/manager_common_questions.html',
                                       {'requests': request, 'count': count, 'search_form': search_form,
                                        'page_range': page_range, 'get_params': get_params},
                                       context_instance=RequestContext(request, ))

        return render_to_response('requests/show_requests.html',
                                   {'questions': requests, 'count': count, 'search_form': search_form,
                                    'page_range': page_range, 'get_params': get_params},
                                   context_instance=RequestContext(request, ))

    return render_to_response('messages.html', {'message': u'صفحه ی مورد نظر موجود نمی باشد'})



def show_requests(request):
    return render_to_response('messages.html', {}, context_instance=RequestContext(request, ))


def show_js_requests(request):
    return render_to_response('messages.html', {}, context_instance=RequestContext(request, ))


def show_em_requests(request):
    return render_to_response('messages.html', {} , context_instance=RequestContext(request, ))

# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from juck.accounts.models import Employer, JobSeeker
from juck.accounts.views import get_user_type
from juck.requests.filter import RequestListFilter
from utils import create_pagination_range


def dashboard(request):
    return render_to_response('requests/dashboard.html', {}, context_instance=RequestContext(request, ))


def conversation(request):
    return render_to_response('requests/conversation.html', {}, context_instance=RequestContext(request, ))



@login_required
def my_needs(request):
    if request.method == "GET":
        get_params = request.GET.copy()
        if 'page' in get_params:
            del get_params['page']

        search_filter = RequestListFilter()
        requests, count = search_filter.init_filter(request.GET, request_type='jo', **{'employer': Employer.objects.get(pk=request.user.pk)})
        search_form = search_filter.get_form()

        page_range = create_pagination_range(requests.number, requests.paginator.num_pages)

        if request.user.role == 'manager':
            return render_to_response('requests/show_requests.html',
                                      {'requests': request, 'request_type': 'ads', 'count': count, 'search_form': search_form,
                                       'page_range': page_range, 'get_params': get_params},
                                      context_instance=RequestContext(request, ))

        return render_to_response('requests/show_requests.html',
                                  {'requests': requests, 'count': count, 'search_form': search_form,
                                   'page_range': page_range, 'get_params': get_params},
                                  context_instance=RequestContext(request, ))

    return render_to_response('messages.html', {'message': u'صفحه ی مورد نظر موجود نمی باشد'})




def advertisements(request):
    if request.method == "GET":
        get_params = request.GET.copy()
        if 'page' in get_params:
            del get_params['page']

        search_filter = RequestListFilter()
        requests, count = search_filter.init_filter(request.GET, request_type='jo')
        search_form = search_filter.get_form()

        page_range = create_pagination_range(requests.number, requests.paginator.num_pages)

        if request.user.role == 'manager':
            return render_to_response('requests/show_requests.html',
                                      {'requests': request, 'request_type': 'ads', 'count': count, 'search_form': search_form,
                                       'page_range': page_range, 'get_params': get_params},
                                      context_instance=RequestContext(request, ))

        return render_to_response('requests/show_requests.html',
                                  {'requests': requests, 'count': count, 'search_form': search_form,
                                   'page_range': page_range, 'get_params': get_params},
                                  context_instance=RequestContext(request, ))

    return render_to_response('messages.html', {'message': u'صفحه ی مورد نظر موجود نمی باشد'})


def show_requests(request):
    return render_to_response('messages.html', {}, context_instance=RequestContext(request, ))


def show_js_requests(request):
    if request.method == "GET":
        get_params = request.GET.copy()
        if 'page' in get_params:
            del get_params['page']


        kwargs = {}
        u_type = get_user_type(request.user.pk)
        if  u_type == 'manager':
            pass
        elif u_type == 'jobseeker':
            kwargs.update({'sender': JobSeeker.objects.get(pk=request.user.pk)})
        else:
            kwargs.update({'employer': Employer.objects.get(pk=request.user.pk)})

        search_filter = RequestListFilter()
        requests, count = search_filter.init_filter(request.GET, request_type='jsjo', **kwargs)
        search_form = search_filter.get_form()

        page_range = create_pagination_range(requests.number, requests.paginator.num_pages)

        if request.user.role == 'manager':
            return render_to_response('requests/show_requests.html',
                                      {'requests': request, 'request_type': 'offer', 'count': count, 'search_form': search_form,
                                       'page_range': page_range, 'get_params': get_params},
                                      context_instance=RequestContext(request, ))

        return render_to_response('requests/show_requests.html',
                                  {'requests': requests, 'request_type': 'offer', 'count': count, 'search_form': search_form,
                                   'page_range': page_range, 'get_params': get_params},
                                  context_instance=RequestContext(request, ))

    return render_to_response('messages.html', {}, context_instance=RequestContext(request, ))


def show_em_requests(request):
    if request.method == "GET":
        get_params = request.GET.copy()
        if 'page' in get_params:
            del get_params['page']

        u_type = get_user_type(request.user.pk)
        kwargs = {}
        if  u_type == 'manager':
            pass
        elif u_type == 'jobseeker':
            kwargs.update({'js_receiver': JobSeeker.objects.get(pk=request.user.pk)})
        else:
            kwargs.update({'employer': Employer.objects.get(pk=request.user.pk)})

        search_filter = RequestListFilter()
        requests, count = search_filter.init_filter(request.GET, request_type='ejo', **kwargs)
        search_form = search_filter.get_form()

        page_range = create_pagination_range(requests.number, requests.paginator.num_pages)

        if request.user.role == 'manager':
            return render_to_response('requests/show_requests.html',
                                      {'requests': request, 'request_type': 'offer', 'count': count, 'search_form': search_form,
                                       'page_range': page_range, 'get_params': get_params},
                                      context_instance=RequestContext(request, ))

        return render_to_response('requests/show_requests.html',
                                  {'requests': requests, 'request_type': 'offer', 'count': count, 'search_form': search_form,
                                   'page_range': page_range, 'get_params': get_params},
                                  context_instance=RequestContext(request, ))
    return render_to_response('messages.html', {}, context_instance=RequestContext(request, ))

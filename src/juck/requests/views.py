# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from juck.accounts.models import Employer, JobSeeker
from juck.accounts.views import get_user_type, check_user_type
from juck.requests.filter import RequestListFilter
from juck.requests.forms import RequestForm, ResponseForm
from juck.requests.models import Response, Request, JobOpportunity, EmployerJobOffer, JobseekerJobOffer
from utils import create_pagination_range


@login_required
def dashboard(request):
    if request.method == "GET":
        if get_user_type(request.user.pk) == 'employer':
            employer = Employer.objects.get(pk=request.user.pk)

            job_opportunities = JobOpportunity.objects.filter(employer=employer, responses__isnull=False)
            job_opps = []
            for item in job_opportunities:
                if item not in job_opps:
                    job_opps.append({'request': item, 'responses': item.responses.all(), 'type': 'jo'})

            employer_offers = EmployerJobOffer.objects.filter(employer=employer, responses__isnull=False)
            emp_offs = []
            for item in employer_offers:
                if item not in emp_offs:
                    emp_offs.append({'request': item, 'responses': item.responses.all(), 'type': 'ejo'})

            jobseeker_offers = JobseekerJobOffer.objects.filter(employer=employer)
            js_offs = []
            for item in jobseeker_offers:
                if item not in js_offs:
                    js_offs.append({'request': item, 'responses': item.responses.all(), 'type': 'jso'})

            dashboard_items = job_opps + emp_offs + js_offs
            dashboard_items.sort(key=sort_by_timestamp)
            dashboard_items.reverse()

    return render_to_response('requests/dashboard.html', {'requests': dashboard_items}, context_instance=RequestContext(request, ))


@login_required
def offer_conversation(request, req_id):
    req = Request.objects.get(pk=req_id)
    responses = req.responses.all().order_by('-timestamp')

    return render_to_response('requests/conversation.html', {'req': req, 'responses': responses}, context_instance=RequestContext(request, ))


@login_required
def request_conversation(request, req_id, resp_id):
    return render_to_response('requests/conversation.html', {}, context_instance=RequestContext(request, ))


@login_required
def my_needs(request):
    if request.method == "GET":
        get_params = request.GET.copy()
        if 'page' in get_params:
            del get_params['page']

        search_filter = RequestListFilter()
        kwargs = {}
        u_type = get_user_type(request.user.pk)
        if u_type == 'manager':
            pass
        elif u_type == 'employer':
            kwargs.update({'employer': Employer.objects.get(pk=request.user.pk)})
        elif u_type == 'jobseeker':
            kwargs.update({'responses__isnull': False, 'responses__user': request.user})

        requests, count = search_filter.init_filter(request.GET, request_type='jo', **kwargs)
        search_form = search_filter.get_form()

        page_range = create_pagination_range(requests.number, requests.paginator.num_pages)

        return render_to_response('requests/show_requests.html',
                                  {'requests': requests, 'request_type': 'ads', 'count': count,
                                   'search_form': search_form,
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

        return render_to_response('requests/show_requests.html',
                                  {'requests': requests, 'request_type': 'ads', 'req_param': 'jOpp', 'count': count,
                                   'search_form': search_form,
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
        if u_type == 'manager':
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
                                      {'requests': request, 'request_type': 'offer', 'count': count,
                                       'search_form': search_form,
                                       'page_range': page_range, 'get_params': get_params},
                                      context_instance=RequestContext(request, ))

        return render_to_response('requests/show_requests.html',
                                  {'requests': requests, 'request_type': 'offer', 'req_param': 'jReq', 'count': count,
                                   'search_form': search_form,
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
        if u_type == 'manager':
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
                                      {'requests': request, 'request_type': 'offer', 'count': count,
                                       'search_form': search_form,
                                       'page_range': page_range, 'get_params': get_params},
                                      context_instance=RequestContext(request, ))

        return render_to_response('requests/show_requests.html',
                                  {'requests': requests, 'request_type': 'offer', 'req_param': 'eReq', 'count': count,
                                   'search_form': search_form,
                                   'page_range': page_range, 'get_params': get_params},
                                  context_instance=RequestContext(request, ))
    return render_to_response('messages.html', {}, context_instance=RequestContext(request, ))


@login_required()
def add_request(request, request_type, item_pk):
    u_type = get_user_type(request.user.pk)
    if request.method == "POST":
        form = ResponseForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get('content', '')
            if request_type == 'jOpp':
                req = Request.objects.get(pk=item_pk)
                Response.objects.create(request=req, content=content, user=request.user)
                return HttpResponseRedirect(reverse('dashboard'))
            elif request_type == 'eReq':
                pass
            elif request_type == 'jReq':
                pass
            return render_to_response('messages.html', {'type': 'green', 'message': 'درخواست با موفقیت ثبت شد.'},
                                      context_instance=RequestContext(request, ))
    else:
        if request_type == 'jOpp':
            form = ResponseForm()
        else:
            form = RequestForm()
        kwargs = {}
        req = ''
        if request_type == 'jOpp':
            req = JobOpportunity.objects.get(pk=item_pk)
        elif request == 'eReq':
            req = EmployerJobOffer.objects.get()
            pass

    return render_to_response('requests/add_request.html', {'form': form, 'req': req, 'req_type': request_type},
                              context_instance=RequestContext(request, ))


@user_passes_test(lambda user: check_user_type(user.pk, 'manager'))
def view_request_status(request, request_type, item_pk):
    if request.method == 'GET':
        req = ''
        if request_type == 'jOpp':
            req = JobOpportunity.objects.get(pk=item_pk)
        elif request_type == 'eReq':
            req = EmployerJobOffer.objects.get(pk=item_pk)
        elif request_type == 'jReq':
            req = JobseekerJobOffer.objects.get(pk=item_pk)

        responses = req.responses.all().order_by('-timestamp')
        return render_to_response('messages.html', {'message': 'Implement Later ! :D'},
                                  context_instance=RequestContext(request, ))
            



def sort_by_timestamp(item):
    return item['request'].timestamp
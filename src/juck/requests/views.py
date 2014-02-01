# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from juck.accounts.models import Employer, JobSeeker, JuckUser
from juck.accounts.views import get_user_type, check_user_type
from juck.requests.filter import RequestListFilter, DashboardListFilter
from juck.requests.forms import RequestForm, ResponseForm, JobOpportunityForm
from juck.requests.models import Response, Request, JobOpportunity, EmployerJobOffer, JobseekerJobOffer, DiscussionThread
from utils import create_pagination_range, json_response


@login_required
def dashboard(request):
    if request.method == "GET":
        get_params = request.GET.copy()
        if 'page' in get_params:
            del get_params['page']

        search_filter = DashboardListFilter()
        threads, count = search_filter.init_filter(request.GET, user_type=get_user_type(request.user.pk),
                                                   user_pk=request.user.pk, **{})
        search_form = search_filter.get_form()

        page_range = create_pagination_range(threads.number, threads.paginator.num_pages)

        return render_to_response('requests/dashboard.html',
                                  {'threads': threads, 'count': count, 'search_form': search_form,
                                   'page_range': page_range, 'get_params': get_params},
                                  context_instance=RequestContext(request))

    return render_to_response('messages.html', {'message': u'درخواستی موجود نمی‌باشد', 'type': 'warning'},
                              context_instance=RequestContext(request, ))


@login_required
def offer_conversation(request, req_id):
    req = Request.objects.get(pk=req_id)
    if req.responses.exists():
        responses = req.responses.all().order_by('-timestamp')
    else:
        responses = ''
    return render_to_response('requests/conversation.html', {'req': req, 'responses': responses},
                              context_instance=RequestContext(request, ))


@login_required
def request_conversation(request, req_id, user_id):
    dt = DiscussionThread.objects.get(request=Request.objects.get(pk=req_id),
                                      responder=JuckUser.objects.get(pk=user_id))
    req = dt.request.cast()
    req_type = ''
    if isinstance(req, JobOpportunity):
        req_type = 'jo'
    elif isinstance(req, JobseekerJobOffer):
        req_type = 'jso'
    elif isinstance(req, EmployerJobOffer):
        req_type = 'ejo'

    responses = dt.responses.all().order_by('timestamp')
    return render_to_response('requests/conversation.html',
                              {'req': req, 'req_type': req_type, 'dt_id': dt.pk, 'responses': responses,
                               'responder': dt.responder},
                              context_instance=RequestContext(request, ))


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


@login_required
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


@login_required
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


@login_required
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


@login_required
def add_request(request, request_type):
    if request.method == "POST":
        if request_type == 'jOpp':
            form = JobOpportunityForm(request.POST)
            if form.is_valid():
                jopp = form.save(commit=False)
                jopp.employer = Employer.objects.get(pk=request.user.pk)
                jopp.save()
        elif request_type in ['jReq', 'eReq']:
            form = RequestForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data.get('content', '')
                title = form.cleaned_data.get('title', '')
                pp_pk = request.POST.get('pp_pk', '')
                dest_user = JuckUser.objects.get(pk=pp_pk).role

                if request_type == 'eReq':
                    ereq = EmployerJobOffer(content=content, title=title)
                    ereq.employer = Employer.objects.get(pk=request.user.pk)
                    if dest_user == 2:
                        ereq.em_receiver = Employer.objects.get(pk=pp_pk)
                        ereq.save()
                        DiscussionThread.objects.create(request=ereq, responder=ereq.em_receiver)
                    else:
                        ereq.js_receiver = JobSeeker.objects.get(pk=pp_pk)
                        ereq.save()
                        DiscussionThread.objects.create(request=ereq, responder=ereq.js_receiver)

                if request_type == 'jReq':
                    jreq = JobseekerJobOffer(content=content, title=title)
                    jreq.sender = JobSeeker.objects.get(pk=request.user.pk)
                    jreq.employer = Employer.objects.get(pk=pp_pk)
                    jreq.save()
                    DiscussionThread.objects.create(request=jreq, responder=jreq.employer)

        return render_to_response('messages.html', {'type': 'green', 'message': 'درخواست با موفقیت ثبت شد.'},
                                  context_instance=RequestContext(request, ))
    else:
        if request_type == 'jOpp':
            form = JobOpportunityForm()
        elif request_type == 'eReq':
            pp_pk = request.GET.get('pk', '')
            form = RequestForm()
        elif request_type == 'jReq':
            pp_pk = request.GET.get('pk', '')
            form = RequestForm()
        else:
            return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز', 'type': 'Error'},
                                      context_instance=RequestContext(request, ))

    return render_to_response('requests/add_request.html', {'form': form, 'req_type': request_type, 'pp_pk': pp_pk},
                              context_instance=RequestContext(request, ))


@login_required
def respond(request):
    if request.is_ajax() and request.POST.get('dt_id') and request.POST.get('content', ''):
        dt_id = request.POST.get('dt_id')
        content = request.POST.get('content', '')
        dt = DiscussionThread.objects.get(pk=dt_id)
        resp = Response.objects.create(thread=dt, content=content, user=request.user)
        author = request.user.get_full_name() if get_user_type(
            request.user.pk) == 'jobseeker' else Employer.objects.get(pk=request.user.pk).profile.company_name
        return json_response({'op_status': 'success', 'pk': resp.pk, 'author': author})

    return json_response({'op_status': 'fail', 'message': u'لطفا تمامی قسمت‌های مورد نظر را تکمیل نمایید.'})


@login_required
def apply_for_job_opportunity(request, item_pk):
    form = ResponseForm()
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get('content', '')
            req = Request.objects.get(pk=item_pk)
            thread = DiscussionThread.objects.get_or_create(request=req, responder=request.user)[0]
            Response.objects.create(thread=thread, content=content, user=request.user)
            return HttpResponseRedirect(reverse('dashboard'))

    req = JobOpportunity.objects.get(pk=item_pk)
    return render_to_response('requests/apply_jo.html', {'form': form, 'req': req},
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


@login_required
def approve_request(request):
    if request.is_ajax() and request.POST.get('pk', ''):
        pk = request.POST.get('pk', '')
        request = Request.objects.get(pk=pk)
        request.status = True
        request.save()
        return json_response({'op_status': 'success'})
    return json_response({'op_status': 'fail'})


@login_required
def reject_request(request):
    if request.is_ajax() and request.POST.get('pk', ''):
        pk = request.POST.get('pk', '')
        request = Request.objects.get(pk=pk)
        request.status = False
        request.save()
        return json_response({'op_status': 'success'})
    return json_response({'op_status': 'fail'})


@user_passes_test(lambda user: check_user_type(user.pk, 'jobseeker'))
def related_ads(request):
    if request.method == "GET":
        get_params = request.GET.copy()
        if 'page' in get_params:
            del get_params['page']

        user = JobSeeker.objects.get(pk=request.user.pk)
        kwargs = {'related': True, 'resume': user.resume}

        search_filter = RequestListFilter()
        requests, count = search_filter.init_filter(request.GET, request_type='jo', **kwargs)
        search_form = search_filter.get_form()

        page_range = create_pagination_range(requests.number, requests.paginator.num_pages)

        return render_to_response('requests/show_requests.html',
                                  {'requests': requests, 'request_type': 'ads', 'req_param': 'jOpp', 'count': count,
                                   'search_form': search_form,
                                   'page_range': page_range, 'get_params': get_params},
                                  context_instance=RequestContext(request, ))

    return render_to_response('messages.html', {'message': u'صفحه ی مورد نظر موجود نمی باشد'})


def sort_by_timestamp(item):
    return item['request'].timestamp
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from juck.log.filters import ActionLogListFilter
from juck.log.models import ActionLog
from utils import create_pagination_range, json_response


@permission_required('accounts.view_manager_lists')
def show_logs_for_user(request):
    if request.method == "GET":

        get_params = request.GET.copy()
        if 'page' in get_params:
            del get_params['page']
        if 'action_flag' in get_params:
            del get_params['action_flag']

        pk = request.GET.get('pk', '')

        dic = {}
        if pk and pk.isdigit():
            dic.update({'user': User.objects.get(pk=pk)})

        search_filter = ActionLogListFilter()
        items = search_filter.init_filter(request.GET, **dic)
        search_form = search_filter.get_form()

        page_range = create_pagination_range(items.number, items.paginator.num_pages)

        return render_to_response('log/view_action_logs.html',
                                  {'actions': items, 'self': False, 'search_form': search_form,
                                   'page_range': page_range, 'get_params': get_params},
                                  context_instance=RequestContext(request, ))

    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request, ))


@login_required()
def show_self_log(request):
    if request.method == "GET":

        get_params = request.GET.copy()
        if 'page' in get_params:
            del get_params['page']

        search_filter = ActionLogListFilter()
        items = search_filter.init_filter(request.GET, **{'user': request.user, 'disabled': False})
        search_form = search_filter.get_form()

        page_range = create_pagination_range(items.number, items.paginator.num_pages)

        return render_to_response('log/view_action_logs.html',
                                  {'actions': items, 'self': True, 'search_form': search_form, 'page_range': page_range,
                                   'get_params': get_params}, context_instance=RequestContext(request, ))

    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request, ))


@login_required
def remove_self_log(request):
    if request.is_ajax() and request.POST.get('pk', ''):
        pk = request.POST.get('pk')
        al = ActionLog.objects.get(pk=pk)
        al.disabled = True
        al.save()
        return json_response({'op_status': 'success'})

    return json_response({'op_status': 'fail'})


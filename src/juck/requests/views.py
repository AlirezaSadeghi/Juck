from django.shortcuts import render_to_response
from django.template.context import RequestContext

__author__ = 'Sina'


def dashboard(request):
    return render_to_response('requests/dashboard.html', {}, context_instance=RequestContext(request, ))


def conversation(request):
    return render_to_response('requests/conversation.html', {}, context_instance=RequestContext(request, ))
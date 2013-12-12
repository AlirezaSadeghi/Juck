# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from juck.news.models import News


def show_news_list(request):
    if request.method == "GET":
        news = News.objects.all()
        return render_to_response('news/news-list.html', {'news': news}, context_instance=RequestContext(request))
    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request))


def show_news_description(request):
    if request.method == "GET":
        pk = request.GET.get('pk', 1)
        try:
            news = News.objects.get(pk=pk)
            comments = []
            #comments = Comment.objects.filter(news=news)
            return render_to_response('news/news_description.html', {'news': news, 'comments': comments},
                                      context_instance=RequestContext(request))
        except ObjectDoesNotExist:
            pass
    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request))

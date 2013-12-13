# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from juck.articles.models import Article


# Create your views here.

def show_news_list(request):
    if request.method == "GET":
        articles = Article.objects.all()
        return render_to_response('articles/articles-list.html', {'articles': articles}, context_instance=RequestContext(request))
    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request))


def show_news_description(request):
    if request.method == "GET":
        pk = request.GET.get('pk', 1)
        try:
            article = Article.objects.get(pk=pk)
            comments = []
            #comments = Comment.objects.filter(news=news)
            return render_to_response('articles/article_description.html', {'article': article, 'comments': comments},
                                      context_instance=RequestContext(request))
        except ObjectDoesNotExist:
            pass
    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request))
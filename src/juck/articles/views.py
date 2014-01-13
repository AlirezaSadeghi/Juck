# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from juck.articles.models import Article, Author, Tag, ArticleSubmission
from forms import ArticleForm

# Create your views here.


def show_articles_list(request):
    if request.method == "GET":
        articles = Article.objects.all().order_by('-publish_date')
        return render_to_response('articles/articles_list.html', {'articles': articles}, context_instance=RequestContext(request))
    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request))


def show_article_description(request):
    if request.method == "GET":
        pk = request.GET.get('pk', 1)
        try:
            article = Article.objects.get(pk=pk)
            comments = []
            #comments = Comment.objects.filter(article=article)
            # print(article.authors.all()[1])
            return render_to_response('articles/article_description.html', {'article': article, 'comments': comments},
                                      context_instance=RequestContext(request))
        except ObjectDoesNotExist:
            pass
    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request))


def show_add_article(request):
    if request.method == "GET":
        return render_to_response('articles/add_article.html', {}, context_instance=RequestContext(request))
    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request))


def add_article(request):
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            # az raveshe form.cleanData systeme alireza estefade kon
            authors = request.POST.get('authors', '').split(',')[:-1]
            print(authors)
            tags = request.POST.get('tags', '').split(',')[:-1]

            for author in authors:
                article.authors.add(Author.objects.get_or_create(full_name=author)[0])

            for tag in tags:
                article.tags.add(Tag.objects.get_or_create(name=tag)[0])

            return HttpResponseRedirect(reverse('articles_list'))

    return render_to_response('articles/add_article.html',{'form':form}, context_instance=RequestContext(request, ))

def submit_article(request):

    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            # az raveshe form.cleanData systeme alireza estefade kon
            authors = request.POST.get('authors', '').split(',')[:-1]
            print(authors)
            tags = request.POST.get('tags', '').split(',')[:-1]

            for author in authors:
                article.authors.add(Author.objects.get_or_create(full_name=author)[0])

            for tag in tags:
                article.tags.add(Tag.objects.get_or_create(name=tag)[0])

            ArticleSubmission(user = request.user, article=article).save()

            return HttpResponseRedirect(reverse('articles_list'))

    return render_to_response('articles/add_article.html',{'form':form}, context_instance=RequestContext(request, ))
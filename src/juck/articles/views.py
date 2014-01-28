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
        pk = request.GET.get('a_pk', None)
        if pk is not None and pk != "":
            pdf = Article.objects.get(pk=pk).source_file
            pdf_file = open(pdf.name)
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="%s"' % pdf.name
            return response
        else:
            articles = Article.objects.all().order_by('-publish_date')
            not_acc = ArticleSubmission.objects.filter(is_accepted=False).values_list('article', flat=True)
            articles = Article.objects.all().order_by('-publish_date').exclude(pk__in=set(not_acc))

            return render_to_response('articles/articles_list.html', {'articles': articles}, context_instance=RequestContext(request))

    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request))


def show_article_description(request):
    if request.method == "GET":
        pk = request.GET.get('pk', 1)
        try:
            if request.GET.get('dl', 'false') == 'true':
                pdf = Article.objects.get(pk=pk).source_file
                file = open(pdf.name)
                response = HttpResponse(file, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="%s"' % pdf.name
                return response
            else:
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


# def show_add_article(request):
#     if request.method == "GET":
#         return render_to_response('articles/add_article.html', {}, context_instance=RequestContext(request))
#     return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
#                               context_instance=RequestContext(request))


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

    return render_to_response('articles/add_article.html', {'form': form}, context_instance=RequestContext(request, ))


def show_article_recommendations_list(request):
    if request.method == "GET":
        ids = ArticleSubmission.objects.filter(is_accepted=False).values_list('article', flat=True)
        articles = Article.objects.filter(pk__in=set(ids)).order_by('-publish_date')
        return render_to_response('articles/article_recommendations_list.html', {'articles': articles}, context_instance=RequestContext(request))
    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request))


def submitted_article_description(request):
    if request.method == "GET":
        pk = request.GET.get('pk', 1)
        try:
            # article_sub = ArticleSubmission.objects.values_list('article', flat=True)
            # article = Article.objects.get(pk=pk)
            article_sub = ArticleSubmission.objects.get(article__pk=pk)
            return render_to_response('articles/submitted_article_description.html', {'article': article_sub.article,'sub_article':article_sub},
                                      context_instance=RequestContext(request))
        except ObjectDoesNotExist:
            pass
    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request))

def review_submitted_article(request):
    if request.method == "POST" and request.is_ajax():
        if request.POST['id'] and request.POST['is_accepted']:
            return HttpResponse('i want to review this')
    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                            context_instance=RequestContext(request))

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
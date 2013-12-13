# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django import forms
from django.db import models

from juck.accounts.models import Manager
from juck.news.models import News
from juck.image.models import JuckImage


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


def add_news(request):
    if request.method == "GET":
        #news = News.objects.all()
        return render_to_response('news/add_news.html', {}, context_instance=RequestContext(request))
    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request))


def submit_news(request):

    if request.method == "POST":

        author = Manager.objects.all()[0] # must be user how use the system now
        title = request.POST.get('title','')
        name  = request.POST.get('name','')
        description = request.POST.get('description', '')
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['image']
            picture = JuckImage(upload_root='news')
            picture.create_picture(image)
            picture.file_name = name
            picture.save()

            new_news = News(title=title,content=description,author=author , image=picture)

        else:
            new_news = News(title=title,content=description,author=author)

        new_news.save()
        return HttpResponseRedirect("/news/news_list")

    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request))


def create_JUCK_image(I_url):
    temp_image = models.ImageField(upload_to=I_url, verbose_name=u'عکس', max_length=250)
    new_image = JuckImage.create_picture(JuckImage(),temp_image)
    return new_image

def upload_news_pic(request):

    if request.method == 'POST':
        print(request.FILES)
        form = ImageUploadForm(request.POST, request.FILES)
        #if form.is_valid():
            #handle_uploaded_file(request.FILES['file'])
            #m = ExampleModel.objects.get(pk=course_id)
            #m.model_pic = form.cleaned_data['image']
            #m.save()
            #return HttpResponse('image upload success')
            #return HttpResponseRedirect('/success/url/')
        pass
    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request))


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()

# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django import forms

from django.conf import settings

from juck.accounts.models import Manager
from juck.accounts.views import check_user_type
from juck.news.filter import NewsListFilter
from juck.news.models import News
from juck.image.models import JuckImage

from juck.news.forms import NewsForm
from utils import create_pagination_range, json_response


def show_news_list(request):
    if request.method == "GET":
        get_params = request.GET.copy()
        if 'page' in get_params:
            del get_params['page']
            #news = {}
        #count = 0
        #search_form = None
        #page_range = None
        search_filter = NewsListFilter()
        news, count = search_filter.init_filter(request.GET, **{})
        search_form = search_filter.get_form()
        page_range = create_pagination_range(news.number, news.paginator.num_pages)

        if not count:
            return render_to_response('messages.html',
                                      {'message': 'متاسفانه خبری موجود نمی باشد.'},
                                      context_instance=RequestContext(request))
        else:

            return render_to_response('news/news-list.html',
                                      {'news': news, 'count': count, 'search_form': search_form,
                                       'page_range': page_range, 'get_params': get_params},
                                      context_instance=RequestContext(request))

    else:
        return render_to_response('messages.html',
                                  {'message': 'دسترسی شما به صفحه ای که درخواست کرده اید مقدور نمی باشد.'},
                                  context_instance=RequestContext(request))


        #if request.method == "GET":
        #    news = News.objects.all().order_by('-publish_date')
        #    return render_to_response('news/news-list.html', {'news': news}, context_instance=RequestContext(request))
        #return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
        #                          context_instance=RequestContext(request))


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
            return render_to_response('messages.html', {'message': u'چنین صفحه‌ای وجود ندارد.'},
                          context_instance=RequestContext(request))

    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request))

@user_passes_test(lambda user: check_user_type(user.pk, 'manager'))
def add_news(request):
    form = NewsForm()
    # print "SADSAD"
    # print request.FILES
    if request.method == "POST":
        form = NewsForm(request.POST)
        print(request.user.pk)
        author = Manager.objects.get(pk=request.user.pk) # must be user how use the system now
        #title = request.POST.get('title','')
        #name  = request.POST.get('name','')
        #description = request.POST.get('description', '')
        #form = ImageUploadForm(request.POST, request.FILES)
        # print ("1111111111")
        if form.is_valid():
            news = form.save(commit=False)
            news.author = author

            image = request.FILES.get('image', '')
            # print ("2222222222")
            if image:
                # print ("3333333333333")
                picture = JuckImage(upload_root="news")
                picture.create_picture(image)
                picture.save()
                news.image = picture
            news.save()
            #
            #new_news = News(title=title,content=description,author=author , image=picture)
            return HttpResponseRedirect(reverse('news_list'))

    return render_to_response('news/add_news.html', {'form': form}, context_instance=RequestContext(request))


def upload_news_pic(request):
    if request.method == 'POST':
        print("xxxxxxxxxxxxxx")
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


def unreachable(request):
        return render_to_response('messages.html', {'message': u' متاسفانه شما در سیستم ما حساب کاربری ندارید.'},
                              context_instance=RequestContext(request))

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()

@login_required
@user_passes_test(lambda user: check_user_type(user.pk, 'manager'))
def remove_news(request):
    if request.method == "POST" and request.is_ajax():
        if request.POST['id']:
            try:
                article = News.objects.get(id=int(request.POST['id']))
                article.delete()
                return json_response({'op_status': 'success', 'message': u'خبر موردنظر باموفقیت حذف شد.'})
            except ObjectDoesNotExist:
                return json_response({'op_status': 'failed', 'message': u'چنین خبری وجود ندارد.'})

    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request))


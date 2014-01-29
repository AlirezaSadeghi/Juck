# -*- coding: utf-8 -*-
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseRedirect, HttpResponse
from datetime import datetime, timedelta
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from juck.accounts.forms import LoginForm, CaptchaForm
from django.contrib import auth
from django.conf import settings
from juck.accounts.models import TemporaryLink, JuckUser, Manager, JobSeeker, Employer
from juck.log.models import ActionLog
from utils import json_response, send_html_mail
import hashlib
import time
from html_builder import HtmlBuilder
from django.views.decorators.csrf import csrf_exempt
from juck.accounts.filter import ManagerJobSeekerListFilter, ManagerEmployerListFilter
from utils import create_pagination_range
from django.contrib.formtools.wizard.views import SessionWizardView

from juck.accounts.forms import *
from juck.news.models import News
from juck.articles.models import Article, ArticleSubmission


def user_panel(request):
    news = News.objects.all()
    articles = Article.objects.all()
    art_sub = ArticleSubmission.objects.all()
    return render_to_response('accounts/user_panel.html',
                              {'user_type': 'manager', 'news': news, 'articles': articles, 'art_sub': art_sub},
                              context_instance=RequestContext(request, ))


def about_us(request):
    return render_to_response('about.html', {}, context_instance=RequestContext(request, ))


def contact_us(request):
    return render_to_response('contact.html', {}, context_instance=RequestContext(request, ))


def homepage(request):
    if request.user.is_authenticated():
        if request.user.is_superuser:
            return HttpResponseRedirect('/admin/')

        news = News.objects.all()
        articles = Article.objects.all()
        art_sub = ArticleSubmission.objects.all()

        if check_user_type(request.user.pk, 'manager'):
            user_type = 'manager'
        elif check_user_type(request.user.pk, 'employer'):
            user_type = 'employer'
        else:
            user_type = 'job_seeker'

        return render_to_response("accounts/user_panel.html",
                                  {'user_type': user_type, 'news': news, 'article': articles, 'art_sub': art_sub},
                                  context_instance=RequestContext(request, ))
    return render_to_response("accounts/homepage.html", {}, context_instance=RequestContext(request))


def login(request):
    form = LoginForm(request.POST or None)
    message = ''

    if form.is_valid():
        username = form.cleaned_data.get('username', '')
        password = form.cleaned_data.get('password', '')

        user = auth.authenticate(username=username, password=password)
        if not (user and user.is_active):
            message = u'حساب کاربری شما وجود ندارد یا در حال حاضر فعال نمی باشد.'
        else:
            auth.login(user)

            if user.is_superuser:
                return HttpResponseRedirect('/admin/')

            next_url = request.POST.get('next', '/')

            if not next_url:
                next_url = '/'

            return HttpResponseRedirect(next_url)

    next_url = request.GET.get('next', '')

    return render_to_response('accounts/login.html', {'message': message, 'next': next_url, 'form': form},
                              context_instance=RequestContext(request, ))


def ajax_login(request):
    if request.is_ajax():
        username = request.POST.get('username')
        password = request.POST.get('password')
        redirect_to_url = settings.LOGIN_REDIRECT_URL
        if JuckUser.objects.filter(email=username).count():
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    if user.is_superuser:
                        redirect_to_url = '/admin/'
                    return json_response({'op_status': 'success', 'redirect_url': redirect_to_url})
                else:
                    return json_response({'op_status': 'not_active', 'message': u'حساب کاربری  مسدود می باشد.'})
            else:
                return json_response({'op_status': 'failed', 'message': u'نام کاربری یا رمز عبور صحیح نیست.'})

        return json_response({'op_status': 'failed', 'message': u'حساب کاربری موجود نمی باشد.'})


def refresh_captcha(request):
    kwargs = {'op_status': 'fail'}

    if request.is_ajax():
        new_key = CaptchaStore.generate_key()
        kwargs['op_status'] = 'success'
        kwargs['key'] = new_key
        kwargs['url'] = captcha_image_url(new_key)

    return json_response(kwargs)


def dos_prevention(request):
    form = CaptchaForm(request.POST or None)

    if form.is_valid():
        if request.session.has_key('next'):
            next_url = request.session.get('next')
        else:
            next_url = '/'

        del request.session['bot']
        del request.session['dos']

        return HttpResponseRedirect(next_url)

    return render_to_response('captcha.html', {'form': form}, context_instance=RequestContext(request, ))


def password_recover(request):
    if request.method == "POST":
        mail = request.POST.get('email', '')
        if mail:
            try:
                user = User.objects.get(email=mail)
            except ObjectDoesNotExist:
                message = u'چنین رایانامه‌ای در پایگاه داده جاک موجود نمی‌باشد'
                return render_to_response('messages.html', {'message': message},
                                          context_instance=RequestContext(request, ))

            hash_value = hashlib.sha224(settings.SECRET_KEY + mail + str(datetime.now())).hexdigest()
            TemporaryLink.objects.create(url_hash=hash_value, email=mail,
                                         expire_date=datetime.now() + timedelta(hours=settings.EMAIL_EXPIRY_INTERVAL))
            html_content = create_password_recovery_mail_html(hash_value)
            send_html_mail(mail, u'سامانه جابر |‌ فراموشی رمز عبور', html=html_content)

            ActionLog.objects.create(user=user, description=u'درخواست ارسال ایمیل فراموشی رمز عبور',
                                     action_flag=ActionLog.OTHERS_FLAG, ip_address=request.get_host())

            return render_to_response('messages.html', {
                'message': u'مراحل مورد نیاز برای تغییر رمز عبور به پست الکترونیکی شما ارسال گردید.'},
                                      context_instance=RequestContext(request, ))

        return render_to_response('messages.html', {'message': u'شما مجاز به انجام این عملیات نیستید.'},
                                  context_instance=RequestContext(request, ))

    return render_to_response('accounts/login.html', {}, context_instance=RequestContext(request, ))


def js_registration(request):
    return HttpResponse("Okay")


def employer_registration(request):
    return HttpResponse("K MothaFucka")


def create_password_recovery_mail_html(hash_value):
    builder = HtmlBuilder()

    text = builder.append_tag('p', u' سلام')
    text += builder.br()
    text += builder.append_tag('p', settings.PASSWORD_RECOVERY_MAIL_CONTENT)
    text += builder.br()
    text += builder.append_tag('a', u'برای تغییر رمز عبور حا را کلیک کنید.',
                               **{'href': settings.SITE_URL + "accounts/password_change_recover/" + hash_value})
    return text


JOB_SEEKER_FORMS = [
    ("Phase_1", JobSeekerRegisterForm1),
    #("Phase_2", JobSeekerRegisterForm2),
    ("Phase_2", JobSeekerRegisterDummyForm),
    #("Phase_3", JobSeekerRegisterForm3),
    ("Phase_3", JobSeekerRegisterDummyForm),
    ("Phase_4", JobSeekerRegisterForm4),
]

EMPLOYER_FORMS = [
    ("Phase_1", EmployerRegisterForm1),
    ("Phase_2", EmployerRegisterForm2),
    ("Phase_3", EmployerRegisterForm3),
]


class JobSeekerWizard(SessionWizardView):
    template_name = 'accounts/job_seeker_registration.html'

    def get_context_data(self, form, **kwargs):
        context = super(JobSeekerWizard, self).get_context_data(form=form, **kwargs)

        if self.steps.step1 == 2:
            current_edu = self.request.session.get("added_edu", None)
            current_skill = self.request.session.get("added_skills", None)
            edu_form = JobSeekerRegisterEducationForm()
            skill_form = JobSeekerRegisterSkillForm()
            context.update({'edu_form': edu_form, 'skill_form': skill_form, 'current_edu': current_edu,
                            'current_skill': current_skill})
        elif self.steps.step1 == 3:
            current_work = self.request.session.get("added_work", None)
            experience_form = JobSeekerRegisterForm3()
            context.update({'experience_form': experience_form, 'current_work': current_work})

        return context

    def done(self, form_list, **kwargs):
        print form_list
        return render_to_response('messages.html', {
            'message': u'خب الان باید تموم شده باشه ! :دی'
        })


class EmployerWizard(SessionWizardView):
    template_name = 'accounts/employer_registration.html'

    def done(self, form_list, **kwargs):
        return render_to_response('messages.html', {
            'message': u'خب الان باید تموم شده باشه ! :دی'
        })


def jobseeker_addedu(request):
    if request.method == "POST":
        message = u"ERROR"

        form = JobSeekerRegisterEducationForm(request.POST)
        if form.is_valid():
            if not request.session.get("added_edu", None) or not isinstance(request.session.get("added_edu", None),
                                                                            dict):
                request.session["added_edu"] = {}
            item_id = int(round(time.time() * 1000))
            request.session["added_edu"][item_id] = form.cleaned_data

            return HttpResponse("{}".format(item_id))

        return HttpResponse(message)

    return HttpResponse("")


def jobseeker_addskill(request):
    if request.method == "POST":
        message = u"ERROR"

        form = JobSeekerRegisterSkillForm(request.POST)
        if form.is_valid():
            if not request.session.get("added_skills", None) or not isinstance(
                    request.session.get("added_skills", None), dict):
                request.session["added_skills"] = {}

            item_id = int(round(time.time() * 1000))
            request.session["added_skills"][item_id] = form.cleaned_data
            return HttpResponse("{}".format(item_id))

        return HttpResponse(message)

    return HttpResponse("")


def jobseeker_addexp(request):
    if request.method == "POST":
        message = u"ERROR"

        form = JobSeekerRegisterForm3(request.POST)
        if form.is_valid():
            if not request.session.get("added_work", None) or not isinstance(request.session.get("added_work", None),
                                                                             dict):
                request.session["added_work"] = {}

            item_id = int(round(time.time() * 1000))
            request.session["added_work"][item_id] = form.cleaned_data
            return HttpResponse("{}".format(item_id))

        return HttpResponse(message)

    return HttpResponse("")


# ------------------------------- these are gaaazjer and u know it ------------------------------------#

# def job_seeker_list(request):
#     if request.method == "GET":
#         return render_to_response('accounts/job_seeker_list.html', {}, context_instance=RequestContext(request))
#     return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
#                               context_instance=RequestContext(request))
#
#
# def employer_list(request):
#     if request.method == "GET":
#         return render_to_response('accounts/employer_list.html', {}, context_instance=RequestContext(request))
#     return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
#                               context_instance=RequestContext(request))


# @login_required
# def pending_employers_list(request, type):
#     pass
#
#
# @login_required
# def pending_jobseekers_list(request, type):
#     pass


# ------------------------------- these are gaaazjer and u know it ------------------------------------#

@login_required()
@user_passes_test(lambda user: check_user_type(user.pk, 'manager'))
def job_seeker_list(request, approved_status):
    if request.method == "GET":

        if approved_status == 'approved':
            approved = True
        elif approved_status == 'not-approved':
            approved = False
        else:
            return render_to_response('messages.html', {'message': u'صفحه موردنظر وجود ندارد.'},
                                      context_instance=RequestContext(request))

        get_params = request.GET.copy()
        if 'page' in get_params:
            del get_params['page']

        search_filter = ManagerJobSeekerListFilter()
        job_seekers, count = search_filter.init_filter(request.GET, **{'profile__approved': approved})
        search_form = search_filter.get_form()

        page_range = create_pagination_range(job_seekers.number, job_seekers.paginator.num_pages)

        return render_to_response('accounts/employer_list.html',
                                  {'job_seekers': job_seekers, 'count': count, 'search_form': search_form,
                                   'page_range': page_range,
                                   'get_params': get_params}, context_instance=RequestContext(request))
    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request))


@login_required()
@user_passes_test(lambda user: check_user_type(user.pk, 'manager'))
def employer_list(request, approved_status):
    if request.method == "GET":

        if approved_status == 'approved':
            approved = True
        elif approved_status == 'not-approved':
            approved = False
        else:
            return render_to_response('messages.html', {'message': u'صفحه موردنظر وجود ندارد.'},
                                      context_instance=RequestContext(request))

        get_params = request.GET.copy()
        if 'page' in get_params:
            del get_params['page']

        search_filter = ManagerEmployerListFilter()
        employers, count = search_filter.init_filter(request.GET, **{'profile__approved': approved})
        search_form = search_filter.get_form()

        page_range = create_pagination_range(employers.number, employers.paginator.num_pages)

        return render_to_response('accounts/employer_list.html',
                                  {'employers': employers, 'count': count, 'search_form': search_form,
                                   'page_range': page_range,
                                   'get_params': get_params}, context_instance=RequestContext(request))
    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request))


@login_required
def show_profile(request):
    pass


@csrf_exempt
def jobseeker_remove(request, what):
    obj_id = request.POST.get('id', None)
    if not obj_id:
        return HttpResponse("ERROR")
    else:
        #obj_id = int(obj_id)
        pass

    if what == "edu":
        del request.session["added_edu"][obj_id]
        print request.session["added_edu"]
    elif what == "skill":
        del request.session["added_skills"][obj_id]
    elif what == "work":
        del request.session["added_work"][obj_id]

    request.session.modified = True

    return HttpResponse("SUCCESS")


def get_user_type(pk):
    try:
        Manager.objects.get(pk=pk)
        user_type = 'manager'
    except ObjectDoesNotExist:
        try:
            Employer.objects.get(pk=pk)
            user_type = 'employer'
        except ObjectDoesNotExist:
            user_type = 'jobseeker'

    return user_type


def check_user_type(pk, user_type):
    if user_type == get_user_type(pk):
        return True
    return False


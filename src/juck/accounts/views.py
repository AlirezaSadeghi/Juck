# -*- coding: utf-8 -*-
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseRedirect, HttpResponse
from datetime import datetime, timedelta
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from juck.accounts.forms import LoginForm, CaptchaForm
from django.contrib import auth
from django.conf import settings
from juck.accounts.models import TemporaryLink
from juck.log.models import ActionLog
from utils import json_response, send_html_mail
import hashlib
from html_builder import HtmlBuilder


def about_us(request):
    return render_to_response('about.html', {}, context_instnace=RequestContext(request, ))


def contact_us(request):
    return render_to_response('contact.html', {}, context_instance=RequestContext(request, ))


def homepage(request):
    if request.user.is_authenticated():
        if request.user.is_superuser:
            return HttpResponseRedirect('/admin/')
        return render_to_response("accounts/homepage.html", {}, context_instance=RequestContext(request, ))
    return render_to_response("base.html", {}, context_instance=RequestContext(request))


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
        username = request.POST.get('login_username')
        password = request.POST.get('login_password')
        redirect_to_url = settings.LOGIN_REDIRECT_URL
        if User.objects.filter(username=username).count():
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
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
    if request.method == "GET":
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


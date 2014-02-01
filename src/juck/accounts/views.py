# -*- coding: utf-8 -*-
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponse
from datetime import datetime, timedelta
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from juck.accounts.forms import LoginForm, CaptchaForm
from django.contrib import auth
from django.conf import settings
from juck.accounts.models import *
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
import uuid
from functools import wraps


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

        news = News.objects.all()[0:5]
        articles = Article.objects.all()[0:5]
        art_sub = ArticleSubmission.objects.all()[0:5]

        if check_user_type(request.user.pk, 'manager'):
            user_type = 'manager'
        elif check_user_type(request.user.pk, 'employer'):
            user_type = 'employer'
        else:
            user_type = 'job_seeker'

        return render_to_response("accounts/user_panel.html",
                                  {'user_type': user_type, 'news': news, 'article': articles, 'art_sub': art_sub},
                                  context_instance=RequestContext(request, ))
        # home_details = HomeDetails.objects.filter(state=True)[0]

    form = CaptchaForm()
    return render_to_response("accounts/homepage.html", {'form': form}, context_instance=RequestContext(request))


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

            if user.is_staff:
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
                role = user.role
                if role == 2:
                    user_cast = Employer.objects.get(pk=user.pk)
                    if not user_cast.profile.approved:
                        return json_response(
                            {'op_status': 'failed', 'message': u'حساب کاربری توسط مدیر تایید نشده است.'})
                elif role == 3:
                    user_cast = JobSeeker.objects.get(pk=user.pk)
                    if not user_cast.profile.approved:
                        return json_response(
                            {'op_status': 'failed', 'message': u'حساب کاربری توسط مدیر تایید نشده است.'})

                if user.is_active:
                    auth.login(request, user)
                    if user.is_staff:
                        redirect_to_url = '/admin/'
                    return json_response({'op_status': 'success', 'redirect_url': redirect_to_url})
                else:
                    return json_response({'op_status': 'not_active', 'message': u'حساب کاربری  فعال نمی باشد.'})
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
    ("Phase_2", JobSeekerRegisterDummyForm),
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
        data = {}
        edu_objs = []
        skill_objs = []
        work_objs = []
        edu_session = self.request.session.get("added_edu", None)
        print(edu_session)
        skill_session = self.request.session.get("added_skills", None)
        print(skill_session)
        work_session = self.request.session.get("added_work", None)
        print(work_session)

        for form in form_list:
            data.update(form.cleaned_data)
        try:
            state_object = State.objects.get(name=data['state'])
        except State.DoesNotExist:
            state_object = State(name=data['state'])
            state_object.save()
        try:
            city_object = City.objects.get(name=data['city'])
        except City.DoesNotExist:
            city_object = City(name=data['city'], state=state_object)
            city_object.save()

        jobseeker_resume = Resume()
        jobseeker_resume.save()

        if edu_session:
            del self.request.session['added_edu']
            for i, edu in edu_session.items():
                edu_obj = Education(certificate=edu['certificate'],
                                    status=edu['status'], major=edu['major'],
                                    orientation=edu['orientation'],
                                    university_name=edu['university_name'],
                                    university_type=edu['university_type'])
                edu_obj.save()
                jobseeker_resume.education.add(edu_obj)
                # edu_objs.append(edu_obj)

        if skill_session:
            del self.request.session['added_skills']
            for i, skill in skill_session.items():
                skill_obj = Skill(title=skill['skill_title'],
                                  level=skill['skill_level'],
                                  description=skill['skill_description'])
                skill_obj.save()
                # skill_objs.append(skill_obj)
                jobseeker_resume.skill.add(skill_obj)

        if work_session:
            del self.request.session['added_work']
            for i, work in work_session.items():
                work_obj = Experience(title=work['title'],
                                      to_date=work['to_date'], from_date=work['from_date'],
                                      place=work['place'],
                                      description=work['description'],
                                      cooperation_type=work['cooperation_type'],
                                      exit_reason=work['exit_reason'])
                work_obj.save()
                # work_objs.append(edu_obj)
                jobseeker_resume.experience.add(work_obj)

        # jobseeker_resume.save()

        activation_key = str(uuid.uuid4())

        jobseeker_profile = JobSeekerProfile(city=city_object, state=state_object,
                                             national_id=data['national_id'],
                                             phone_number=data['phone_num'],
                                             mobile_number=data['mobile_num'],
                                             approved=False)

        jobseeker_profile.save()

        jobseeker = JobSeeker(first_name=data['first_name'],
                              last_name=data['last_name'],
                              email=data['email'], role=JuckUser.JOB_SEEKER,
                              profile=jobseeker_profile, resume=jobseeker_resume,
                              activation_key=activation_key)

        jobseeker.set_password(data['password'])
        jobseeker.save()

        #TODO
        html_content = create_confirm_email_html(activation_key, 'job_seeker')
        try:
            send_html_mail(data['email'], u'سامانه جاک | تایید ثبت‌نام', html=html_content)
        except:
            pass

        return render_to_response('messages.html', {
            # 'message': activation_key
            'message': u'ثبت‌نام شما با موفقیت انجام شد،جهت تایید ثبت‌نام پست‌الکترونیکی برای شما فرستاده شده است.'
        })


def passed_captcha(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if 'captcha_solved' in request.session and request.session['captcha_solved']:
            return view(request, request.user.username, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    return wrapper


class EmployerWizard(SessionWizardView):
    template_name = 'accounts/employer_registration.html'

    def done(self, form_list, **kwargs):
        activation_key = ''
        email, first_name, last_name, password, user_rank, company_name = '', '', '', '', '', ''
        company_type, reg_num, manager, field = '', '', '', ''
        foundation_year = 1392
        for index in range(0, len(form_list)):

            if index == 0:
                email = form_list[index].cleaned_data['email']

                print(email)
                # first_name = form_list[index].cleaned_data['first_name']
                # last_name = form_list[index].cleaned_data['last_name']
                password = form_list[index].cleaned_data['password']
                user_rank = form_list[index].cleaned_data['connector_rank']

            elif index == 1:
                company_name = form_list[index].cleaned_data['company_name']
                company_type = form_list[index].cleaned_data['company_type']
                reg_num = form_list[index].cleaned_data['reg_num']
                foundation_year = int(form_list[index].cleaned_data['foundation_year'])
                manager = form_list[index].cleaned_data['manager']
                field = form_list[index].cleaned_data['field']

            else:
                website = form_list[index].cleaned_data['website']
                phone_number = form_list[index].cleaned_data['phone_num']
                mobile_number = form_list[index].cleaned_data['mobile_num']
                city = form_list[index].cleaned_data['city']
                state = form_list[index].cleaned_data['state']
                address = form_list[index].cleaned_data['address']
                postal_code = form_list[index].cleaned_data['postal_code']

                try:
                    state_object = State.objects.get(name=state)
                except State.DoesNotExist:
                    state_object = State(name=state)
                    state_object.save()
                try:
                    city_object = City.objects.get(name=city)
                except City.DoesNotExist:
                    city_object = City(name=city, state=state_object)
                    city_object.save()

                activation_key = str(uuid.uuid4())

                profile = EmployerProfile(company_name=company_name, company_type=company_type,
                                          foundation_year=foundation_year, reg_num=reg_num,
                                          manager=manager, user_rank=user_rank, field=field,
                                          address=address, postal_code=postal_code, phone_number=phone_number,
                                          mobile_number=mobile_number, website=website,
                                          state=state_object, city=city_object, approved=False)
                profile.save()
                emp = Employer(email=email, profile=profile, role=JuckUser.EMPLOYER, activation_key=activation_key)
                emp.set_password(password)
                emp.save()

                #TODO
                html_content = create_confirm_email_html(activation_key, 'employer')
                try:
                    send_html_mail(email, u'سامانه جاک | تایید ثبت‌نام', html=html_content)
                except:
                    pass

        return render_to_response('messages.html', {
            # 'message': activation_key
            'message': u'ثبت‌نام شما با موفقیت انجام شد،جهت تایید ثبت‌نام پست‌الکترونیکی برای شما فرستاده شده است.'
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
            request.session.modified = True

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
            request.session.modified = True

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
            request.session.modified = True

            return HttpResponse("{}".format(item_id))

        return HttpResponse(message)

    return HttpResponse("")


@login_required()
def job_seeker_list(request, approved_status):
    if request.method == "GET":

        if approved_status == 'approved':
            approved = True
        elif approved_status == 'not-approved':
            approved = False
        else:
            return render_to_response('messages.html', {'message': u'صفحه موردنظر وجود ندارد.'},
                                      context_instance=RequestContext(request))
        user_type = get_user_type(request.user.pk)

        if user_type != 'manager' and not approved:
            return render_to_response('messages.html', {'message': u'دسترسی غیرمجاز'},
                                      context_instance=RequestContext(request))

        get_params = request.GET.copy()
        if 'page' in get_params:
            del get_params['page']

        search_filter = ManagerJobSeekerListFilter()
        job_seekers, count = search_filter.init_filter(request.GET, **{'profile__approved': approved})
        search_form = search_filter.get_form()

        page_range = create_pagination_range(job_seekers.number, job_seekers.paginator.num_pages)

        return render_to_response('accounts/job_seeker_list.html',
                                  {'job_seekers': job_seekers, 'count': count, 'search_form': search_form,
                                   'page_range': page_range, 'approved': approved, 'user_type': user_type,
                                   'get_params': get_params}, context_instance=RequestContext(request))
    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request))


@login_required()
def employer_list(request, approved_status):
    if request.method == "GET":

        if approved_status == 'approved':
            approved = True
        elif approved_status == 'not-approved':
            approved = False
        else:
            return render_to_response('messages.html', {'message': u'صفحه موردنظر وجود ندارد.'},
                                      context_instance=RequestContext(request))
        user_type = get_user_type(request.user.pk)

        if user_type != 'manager' and not approved:
            return render_to_response('messages.html', {'message': u'دسترسی غیرمجاز'},
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
                                   'page_range': page_range, 'approved': approved, 'user_type': user_type,
                                   'get_params': get_params}, context_instance=RequestContext(request))
    return render_to_response('messages.html', {'message': u'دسترسی غیر مجاز'},
                              context_instance=RequestContext(request))


@login_required
def show_profile(request):
    if request.method == "GET" and request.GET.get('pk', ''):
        pk = int(request.GET.get('pk', ''))
        self_profile = pk == request.user.pk
        user = JuckUser.objects.get(pk=pk) if not self_profile else request.user

        if request.method == "GET":
            u_type = get_user_type(user.pk)
            kwargs = {}

            kwargs['self_profile'] = True if self_profile else False
            print(kwargs['self_profile'])
            if u_type == 'jobseeker':
                kwargs['jobseeker'] = JobSeeker.objects.get(pk=user.pk)
                # user = kwargs['jobseeker']
                # kwargs['profile'] = user.profile
                # kwargs['resume'] = user.resume
                # kwargs['educations'] = user.resume.education.all()
                # kwargs['skills'] = user.resume.skill.all()
                # kwargs['experiences'] = user.resume.experience.all()
                #
                return render_to_response('accounts/jobseeker_profile_self.html', kwargs,
                                          context_instance=RequestContext(request, ))
            elif u_type == 'employer':
                kwargs['employer'] = Employer.objects.get(pk=user.pk)
                # kwargs['profile'] = kwargs['employer'].profile
                return render_to_response('accounts/employer_profile.html', kwargs,
                                          context_instance=RequestContext(request))

    return render_to_response('messages.html', {'message': u'چنین کاربری وجود ندارد'},
                              context_instance=RequestContext(request, ))


@csrf_exempt
def jobseeker_remove(request, what):
    obj_id = request.POST.get('id', None)
    if not obj_id:
        return HttpResponse("ERROR")
    else:
        obj_id = int(obj_id)
        # print(obj_id)
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


def ajax_remove_or_approve_user(request):
    if request.is_ajax():
        function = request.POST.get('function')
        user_type = request.POST.get('user_type')
        id = request.POST.get('id')
        if user_type == 'job_seeker':
            users = JobSeeker.objects.all()
        elif user_type == 'employer':
            users = Employer.objects.all()
        else:
            return json_response({'op_status': 'failed', 'message': u'چنین نوع کاربری وجود ندارد.'})

        if users.filter(id=id).exists():
            user = users.filter(id=id)[0]
            if function == 'approve':
                profile = user.profile
                profile.approved = True
                profile.save()
                user.save()

                html_content = create_manager_confirm_html(function)
                try:
                    send_html_mail(user.email, u'سامانه جاک | تایید حساب‌کاربری', html=html_content)
                except:
                    pass

                return json_response({'op_status': 'success', 'message': u'کاربر موردنظر با موفقیت تایید شد.'})
            elif function == 'remove':

                html_content = create_manager_confirm_html(function)
                try:
                    send_html_mail(user.email, u'سامانه جاک | حذف حساب‌کاربری', html=html_content)
                except:
                    pass

                user.delete()

                return json_response({'op_status': 'success', 'message': u'کاربر موردنظر با موفقیت حذف گردید.'})
            elif function == 'disapprove':
                profile = user.profile
                profile.approved = False
                profile.save()
                user.save()

                return json_response({'op_status': 'success', 'message': u'کاربر موردنظر با موفقیت غیرفعال شد.'})
            else:
                return json_response({'op_status': 'failed', 'message': u'چنین کارکردی وجود ندارد.'})
        return json_response({'op_status': 'failed', 'message': u'حساب کاربری موجود نمی باشد.'})


def captcha_view(request, u_type):
    if request.method == 'POST':
        form = CaptchaForm(request.POST)
        if form.is_valid():
            url = ''
            if 'captcha_solve' not in request.session:
                request.session['captcha_solved'] = True
                if u_type == 'jobseeker':
                    url = 'jobseeker_registration'
                elif u_type == 'employer':
                    url = 'employer_registration'
            if url:
                return HttpResponseRedirect(reverse(url))
    else:
        pass
    return render_to_response('accounts/captcha_form.html', {'form': form},
                              context_instance=RequestContext(request))


def check_catpcha(request):
    if request.is_ajax():
        form = CaptchaForm(request.POST)
        if form.is_valid():
            request.session['captcha_solved'] = True
            request.session.modified = True
            if request.POST.get('reg_type', '') == 'jobseeker':
                url = '/accounts/jobseeker_registration/'
            if request.POST.get('reg_type', '') == 'employer':
                url = '/accounts/employer_registration/'
            return json_response({'op_status': 'success', 'url': url})

    return json_response({'op_status': 'fail'})


def confirm_registration(request, user_type, key):
    user, active, exists = '', False, True
    if user_type == 'job_seeker':
        try:
            user = JobSeeker.objects.get(activation_key=key)
            if user.is_active:
                active = True
        except JobSeeker.DoesNotExist:
            exists = False
    elif user_type == 'employer':
        try:
            user = Employer.objects.get(activation_key=key)
            if user.is_active:
                active = True
        except Employer.DoesNotExist:
            exists = False
    else:
        return render_to_response('messages.html', {'message': u'صفحه موردنظر وجود ندارد.'},
                                  context_instance=RequestContext(request))

    if active or request.user.is_authenticated():
        return render_to_response('messages.html', {'message': u'حساب کاربری شما فعال است.'},
                                  context_instance=RequestContext(request))
    if exists:
        user.is_active = True
        user.save()
        return render_to_response('messages.html', {
            'message': u'حساب کاربری شما فعال شد. برای استفاده از امکانات سایت، تا تایید ثبت‌نام توسط مدیر شکیبا باشید.'},
                                  context_instance=RequestContext(request))

    else:
        return render_to_response('messages.html', {
            'message': u'صفحه موردنظر وجود ندارد.'},
                                  context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda user: check_user_type(user.pk, 'employer'))
def employer_edit_profile(request):
    try:
        profile = Employer.objects.get(pk=request.user.pk).profile
    except ObjectDoesNotExist:
        return render_to_response('messages.html', {
            'message': u'صفحه موردنظر وجود ندارد.'}, context_instance=RequestContext(request))

    if request.method == "POST":
        form = EditEmployerProfile(request.POST, request.FILES, instance=profile)
        # print('post with form')
        if form.is_valid():
            data = form.cleaned_data
            try:
                state_object = State.objects.get(name=data['state'])
            except State.DoesNotExist:
                state_object = State(name=data['state'])
                state_object.save()
            try:
                city_object = City.objects.get(name=data['city'])
            except City.DoesNotExist:
                city_object = City(name=data['city'], state=state_object)
                city_object.save()

            new_profile = EmployerProfile(city=city_object, state=state_object,
                                          company_name=data['company_name'], company_type=data['company_type'],
                                          foundation_year=data['foundation_year'], reg_num=data['reg_num'],
                                          user_rank=data['user_rank'], field=data['field'], address=data['address'],
                                          postal_code=data['postal_code'], mobile_number=data['mobile_number'],
                                          phone_number=data['phone_number'], manager=data['manager'],
                                          approved=True)

            image = request.FILES.get('image', '')
            if image:
                picture = JuckImage(upload_root="news")
                picture.create_picture(image)
                picture.save()
                new_profile.image = picture

            new_profile.save()
            emp = Employer.objects.get(pk=request.user.pk)
            emp.profile = new_profile
            emp.save()
            # print('doooooneeeeee')
            return HttpResponseRedirect('accounts/show_profile/?pk=%s' %request.user.pk)
    else:
        initial = {'city': profile.city.name, 'state': profile.state.name}
        if profile.image:
            initial.update({'image': profile.image.image})
        form = EditEmployerProfile(instance=profile, initial=initial)

    # print('no done :-<')
    return render_to_response('accounts/employer_edit_form.html', {'form': form},
                              context_instance=RequestContext(request))


@login_required
def jobseeker_edit_profile(request):
    pass


def create_manager_confirm_html(function):
    mail_content = ''
    if function == 'approve':
        mail_content = u'اطلاعات ثبت‌نام شما توسط مدیر تایید شد و می‌توانید وارد سایت شوید.'
    elif function == 'remove':
        mail_content = u'اکانت شما توسط مدیر حذف گردید.'
    else:
        return mail_content

    builder = HtmlBuilder()

    text = builder.append_tag('p', u'با سلام')
    text += builder.br()
    text += builder.append_tag('p', mail_content)
    text += builder.br()
    text += builder.append_tag('a', u'سامانه جاک',
                               **{'href': (
                                   settings.SITE_URL )})
    return text


def create_confirm_email_html(activation_key, type):
    mail_content = u'ثبت‌نام شما در سامانه جاک در مراحل نهایی است.برای تکمیل ثبت‌نام برروی لینک زیر کلیک کنید.همچنین پس از انجام این عمل باید تا زمان تایید مدیریت منتظر بمانید.'

    builder = HtmlBuilder()

    text = builder.append_tag('p', u'با سلام')
    text += builder.br()
    text += builder.append_tag('p', mail_content)
    text += builder.br()
    text += builder.append_tag('a', u'برای تایید ثبت نام در سامانه جاک اینجا را کلیک کنید',
                               **{'href': (
                                   settings.SITE_URL + "accounts/confirm/" + type + "/" + activation_key)})
    return text


def get_user_type(pk):
    try:
        int(pk)
    except TypeError:
        return 'external'

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


# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from django.forms.util import ErrorList
from persian_captcha import PersianCaptchaField
from django.forms.fields import Field
from juck.accounts.models import *
from django.core.validators import MinLengthValidator, MaxLengthValidator


class EditEmployerProfile(ModelForm):
    state = forms.CharField(required=True, label=u'استان', max_length=100)
    city = forms.CharField(required=True, label=u'شهر', max_length=100)
    image = forms.ImageField(required=False, label=u'عکس')

    def clean_postal_code(self):

        data = self.cleaned_data['postal_code']
        ok = True
        if not data:
            return data
        for i in data.split('-'):
            if not i.isdigit():
                ok = False
                break
        if ok:
            return data
        else:
            print('it\'s not')
            raise forms.ValidationError((u" کدپستی واردشده نامعتبر است."), code='notNumber')

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        ok = True

        for i in data.split('-'):
            if not i.isdigit():
                ok = False
                break
        if ok:
            return data
        else:
            print('it\'s not')
            raise forms.ValidationError((u"شماره تلفن واردشده نامعتبر است."), code='notNumber')

    def clean_mobile_number(self):
        data = self.cleaned_data['mobile_number']
        if not data:
            return data
        ok = True
        for i in data.split('-'):
            if not i.isdigit():
                ok = False
                break
        if ok:
            return data
        else:
            raise forms.ValidationError((u"شماره تلفن همراه واردشده نامعتبر است."), code='notNumber')

    class Meta:
        model = EmployerProfile
        exclude = ('approved', 'city', 'state', 'image')


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label=u'نام کاربری')
    password = forms.CharField(required=True, widget=forms.PasswordInput(render_value=False), label=u'رمز عبور')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'login-page-input'
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label


class CaptchaForm(forms.Form):
    captcha = PersianCaptchaField(label=u'کد امنیتی', required=True)

    def __init__(self, *args, **kwargs):
        super(CaptchaForm, self).__init__(*args, **kwargs)


class JobSeekerRegisterForm1(forms.Form):
    first_name = forms.CharField(required=True, label=u'نام', help_text=u'نام خود. مانند سینا, مریم , علی')
    last_name = forms.CharField(required=True, label=u'نام خانوادگی',
                                help_text=u'نام خانوادگی. مانند حسن پور, صادقی, فراهانی')
    email = forms.EmailField(required=True, label=u'پست الکترونیکی', widget=forms.TextInput(attrs={'dir': 'ltr'}),
                             help_text=u'آدرس الکترونیکی خودتان. حتما درست و کامل وارد شود زیرا برای تایید شدن شما نیاز است و همچنین نام کاربری شما در سایت می باشد. به فرمت درست مانند alireza@juck.com وارد شود. همچنین دقت شود از هر آدرس الکترونیک فقط یک بار در سایت می توانید ثبت نام کنید.')
    national_id = forms.CharField(required=True, label=u'کدملی', max_length=20,
                                  help_text=u'کد ملی ذکر شده در کارت ملی شما. فقط اعداد آن به صورت منظم وارد شوند و از گذاشتن فاصله و یا - خودداری شود.')
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label=u'رمز عبور',
                               validators=[MinLengthValidator(4)],
                               help_text=u'گذرواژه ی شما برای ورود به سایت می باشد. حداقل باید از 4 کارکتر تشکیل شده باشد.')
    re_password = forms.CharField(widget=forms.PasswordInput(), required=True, label=u'تکرار رمز عبور',
                                  help_text=u'تکرار گذرواژه برای اطمینان از درست وارد شدن آن.')
    # captcha = PersianCaptchaField(required=True, label=u'کد امنیتی')

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            JuckUser.objects.get(email=data)
            raise forms.ValidationError((u"پست الکترونیکی قبلا استفاده شده است."), code='userExists')
        except JuckUser.DoesNotExist:
            return data

    def clean_national_id(self):
        data = self.cleaned_data['national_id']
        if JobSeekerProfile.objects.filter(national_id=data):
            raise forms.ValidationError((u"کدمدلی قبلا استفاده شده است."), code='userExists')
        else:
            return data

    def clean(self):
        cleaned_data = super(JobSeekerRegisterForm1, self).clean()
        pass1 = cleaned_data.get('password', '')
        pass2 = cleaned_data.get('re_password', '')

        if pass1 != pass2 and pass1 and pass2:
            self._errors['password'] = ErrorList([u'رمز عبور و تکرار آن باید یکسان باشند.'])
            del cleaned_data['password']

        return cleaned_data


class JobSeekerRegisterForm2(forms.Form):
    status = forms.ChoiceField(required=True, label=u'وضغیت تحصیلی',
                               choices=(
                                   ('student', u'دانشچو'),
                                   ('grauated', u'فارغ التحصیل'),
                               ), help_text=u'وضعیت تحصیلی کنونی شما.')
    certificate = forms.ChoiceField(required=True, label=u'مقطع تحصیلی',
                                    choices=(
                                        ('diploma', u'دیپلم'),
                                        ('under_grad', u'کارشناسی'),
                                        ('grad', u'کارشناسی ارشد'),
                                        ('phd', u'دکتری'),
                                        ('post_doc', u'پست دکتری'),
                                    ),
                                    help_text=u'مقطعی که اکنون در حال تحصیل هستید و یا گذرانده اید.')
    major = forms.CharField(required=True, max_length=200, label=u'رشته تحصیلی')
    orientation = forms.CharField(required=True, max_length=150, label=u'گرایش تحصیلی')
    university_name = forms.CharField(required=True, max_length=150, label=u'نام دانشگاه')
    university_type = forms.ChoiceField(required=True, label=u'نوع دانشگاه',
                                        choices=(
                                            ('dolati', u'دولتی'),
                                            ('azad', u'آزاد'),
                                            ('entefaei', u'غیرانتفاعی'),
                                            ('payam_nur', u'پیام نور'),
                                            ('foregin', u'خارجی'),
                                        ),
                                        help_text=u'نوع دانشگاهی که مرتبط با مدرکی که در حال وارد کردن آن هستید, می باشد.')
    # certificate_file = forms.FileField(required=False, label=u'بارگذاری مدرک')

    skill_title = forms.CharField(required=True, max_length=150, label=u'عنوان مهارت')
    skill_level = forms.ChoiceField(required=True, label=u'سطح تسلط',
                                    choices=(
                                        ('low', u'آشنا'),
                                        ('high', u'مسط'),
                                        ('certificate', u'دارای مدرک معتبر'),
                                    ),
                                    help_text=u'میزان تسلط شما به مهارت معرفی شده .'

    )
    skill_description = forms.CharField(required=False, max_length=250, label=u'توضیحات',
                                        help_text=u'اگر نکاتی وجود دارد که به نظر شما در فرم لحاظ نشده است در این جا درج کنید.')


class JobSeekerRegisterEducationForm(forms.Form):
    status = forms.ChoiceField(required=True, label=u'وضغیت تحصیلی',
                               choices=(
                                   ('student', u'دانشجو'),
                                   ('graduated', u'فارغ التحصیل'),
                               ))
    certificate = forms.ChoiceField(required=True, label=u'مقطع تحصیلی',
                                    choices=(
                                        ('under_grad', u'کارشناسی'),
                                        ('grad', u'کارشناسی ارشد'),
                                        ('phd', u'دکتری'),
                                        ('post_doc', u'پست دکتری'),
                                    ))
    major = forms.CharField(required=True, max_length=200, label=u'رشته تحصیلی')
    orientation = forms.CharField(required=True, max_length=150, label=u'گرایش تحصیلی')
    university_name = forms.CharField(required=True, max_length=150, label=u'نام دانشگاه')
    university_type = forms.ChoiceField(required=True, label=u'نوع دانشگاه',
                                        choices=(
                                            ('dolati', u'دولتی'),
                                            ('azad', u'آزاد'),
                                            ('entefaei', u'غیرانتفاعی'),
                                            ('payam_nur', u'پیام نور'),
                                            ('foregin', u'خارجی'),
                                        ))


class JobSeekerRegisterSkillForm(forms.Form):
    skill_title = forms.CharField(required=True, max_length=150, label=u'عنوان مهارت')
    skill_level = forms.ChoiceField(required=True, label=u'سطح تسلط',
                                    choices=(
                                        ('low', u'آشنا'),
                                        ('high', u'مسط'),
                                        ('certificate', u'دارای مدرک معتبر'),
                                    ))
    skill_description = forms.CharField(required=False, max_length=250, label=u'توضیحات')


class JobSeekerRegisterDummyForm(forms.Form):
    #dummy = forms.CharField(widget=forms.HiddenInput, required=False)    
    pass


class JobSeekerRegisterForm3(forms.Form):
    title = forms.CharField(required=True, max_length=200, label=u'عنوان سابقه',
                            help_text=u'در کمتر از 200 حرف عنوان مناسب را انتخاب کنید.')
    place = forms.CharField(required=False, max_length=200, label=u'سازمان یا دانشگاه مربوطه')
    from_date = forms.IntegerField(required=True, label=u'از سال')
    to_date = forms.IntegerField(required=True, label=u'تا سال')
    description = forms.CharField(widget=forms.Textarea(), required=False, label=u'توضیحات',
                                  help_text=u'لطفا توضیحات را هرچه دقیق تر بیان کنید و از کلی گویی بپرهیزید.')
    cooperation_type = forms.CharField(required=False, label=u'نوع همکاری', max_length=150,
                                       help_text=u'استخدام یا قراردادی بودن')
    exit_reason = forms.CharField(required=False, label=u'دلیل قطع همکاری', max_length=200,
                                  help_text=u'در صورت امکان دلیل جدایی خود را از کار قبلی به صورت مختصر ( 200 حرف) شرح دهید.')


class JobSeekerRegisterForm4(forms.Form):
    website = forms.URLField(required=False, label=u'وب سایت',
                             help_text=u'سایت رسمی خود را در این جا بنویسید., دقت کنید به فرمت دقیق مانند www.juck.com در فرم بنویسید.')
    phone_num = forms.CharField(required=True, label=u'شماره تلفن',
                                help_text=u'شماره تماس اصلی خودتان زا برای برقراری ارتباط وارد کنید. پیش شماره شهر خود را نیز حتما درج کنید.')
    mobile_num = forms.CharField(required=False, label=u'شماره تلفن همراه')
    state = forms.CharField(required=True, label=u'استان', max_length=100)
    city = forms.CharField(required=True, label=u'شهر', max_length=100)
    # address = forms.CharField(required=True, widget=forms.Textarea(attrs={'style': 'width:400px;margin-top:-15px'}),
    #                           label=u'آدرس')
    # postal_code = forms.CharField(required=False, label=u'کد پستی')

    # def clean_postal_code(self):
    #     data = self.cleaned_data['postal_code']
    #     ok = True
    #     if not data:
    #         return data
    #     for i in data.split('-'):
    #         if not i.isdigit():
    #             ok = False
    #             break
    #     if ok:
    #         return data
    #     else:
    #         print('it\'s not')
    #         raise forms.ValidationError((u" کدپستی واردشده نامعتبر است."), code='notNumber')


    def clean_phone_num(self):
        data = self.cleaned_data['phone_num']
        ok = True

        for i in data.split('-'):
            if not i.isdigit():
                ok = False
                break
        if ok:
            return data
        else:
            print('it\'s not')
            raise forms.ValidationError((u"شماره تلفن واردشده نامعتبر است."), code='notNumber')

    def clean_mobile_num(self):
        data = self.cleaned_data['mobile_num']
        if not data:
            return data
        ok = True
        for i in data.split('-'):
            if not i.isdigit():
                ok = False
                break
        if ok:
            return data
        else:
            raise forms.ValidationError((u"شماره تلفن همراه واردشده نامعتبر است."), code='notNumber')


class JobSeekerEditProfileForm(forms.ModelForm):
    state = forms.CharField(required=True, label=u'استان', max_length=100)
    city = forms.CharField(required=True, label=u'شهر', max_length=100)
    image = forms.ImageField(required=False, label=u'عکس')

    def clean_postal_code(self):

        data = self.cleaned_data['postal_code']
        ok = True
        if not data:
            return data
        for i in data.split('-'):
            if not i.isdigit():
                ok = False
                break
        if ok:
            return data
        else:
            print('it\'s not')
            raise forms.ValidationError((u" کدپستی واردشده نامعتبر است."), code='notNumber')

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        ok = True

        for i in data.split('-'):
            if not i.isdigit():
                ok = False
                break
        if ok:
            return data
        else:
            print('it\'s not')
            raise forms.ValidationError((u"شماره تلفن واردشده نامعتبر است."), code='notNumber')

    def clean_mobile_number(self):
        data = self.cleaned_data['mobile_number']
        if not data:
            return data
        ok = True
        for i in data.split('-'):
            if not i.isdigit():
                ok = False
                break
        if ok:
            return data
        else:
            raise forms.ValidationError((u"شماره تلفن همراه واردشده نامعتبر است."), code='notNumber')

    class Meta:
        model = JobSeekerProfile
        exclude = ('approved', 'image', 'city', 'state')
        widgets = {
            'married': forms.Select(choices=(
                ('', u'انتخاب وضعیت'),
                (True, u'متاهل'),
                (False, u'مجرد'),
            )),
            'sex': forms.Select(choices=(
                ('', u'انتخاب جنسیت'),
                (True, u'مرد'),
                (False, u'زن'),
            )),
        }


class EmployerRegisterForm1(forms.Form):
    email = forms.EmailField(required=True, label=u'پست الکترونیکی', widget=forms.TextInput(attrs={'dir': 'ltr'}),
                             help_text=u'آدرس الکترونیکی خودتان. حتما درست و کامل وارد شود زیرا برای تایید شدن شما نیاز است و همچنین نام کاربری شما در سایت می باشد. به فرمت درست مانند alireza@juck.com وارد شود. همچنین دقت شود از هر آدرس الکترونیک فقط یک بار در سایت می توانید ثبت نام کنید.')
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label=u'رمز عبور',
                               validators=[MinLengthValidator(4)],
                               help_text=u'گذرواژه ی شما برای ورود به سایت می باشد. حداقل باید از 4 کارکتر تشکیل شده باشد.')
    re_password = forms.CharField(widget=forms.PasswordInput(), required=True, label=u'تکرار رمز عبور',
                                  help_text=u'تکرار گذرواژه برای اطمینان از درست وارد شدن آن.')
    # connector_name = forms.CharField(required=True, label=u'نام شخص رابط')
    connector_rank = forms.CharField(label=u'سمت شخص رابط',
                                     help_text=u'نقش (شغل) شما در شرکت و یا سازمانی که می خواهید در سامانه ثبت کنید.')
    # captcha = PersianCaptchaField(required=True, label=u'کد امنیتی')

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            JuckUser.objects.get(email=data)
            raise forms.ValidationError((u"پست الکترونیکی قبلا استفاده شده است."), code='userExists')
        except JuckUser.DoesNotExist:
            return data

    def clean(self):
        cleaned_data = super(EmployerRegisterForm1, self).clean()
        pass1 = cleaned_data.get('password', '')
        pass2 = cleaned_data.get('re_password', '')

        if pass1 and pass2 and pass1 != pass2:
            self._errors['password'] = ErrorList([u'رمز عبور و تکرار آن باید یکسان باشند.'])
            del cleaned_data['password']

        return cleaned_data


class EmployerRegisterForm2(forms.Form):
    company_name = forms.CharField(required=True, label=u'نام سازمان')
    company_type = forms.CharField(required=True, label=u'نوع سازمان', help_text=u'دولتی, خصوصی, نیمه دولتی ')
    reg_num = forms.CharField(required=True, label=u'شماره ثبت')
    foundation_year = forms.CharField(required=True, label=u'سال تاسیس')
    manager = forms.CharField(required=False, label=u'نام مدیرعامل')
    field = forms.CharField(required=True, label=u'زمینه فعالیت', help_text=u'تا جایی که امکان دارد دقیق بنویسید.')

    def clean_foundation_year(self):
        data = self.cleaned_data['foundation_year']
        if data.isdigit():
            return data
        else:
            print('it\'s not')
            raise forms.ValidationError((u" سال تاسیس واردشده نامعتبر است."), code='notNumber')


class EmployerRegisterForm3(forms.Form):
    website = forms.URLField(required=False, label=u'وب سایت',
                             help_text=u'سایت رسمی سازمان یا شرکت شما برای معرفی به بقیه, دقت کنید به فرمت دقیق مانند www.juck.com در فرم بنویسید.')
    phone_num = forms.CharField(required=True, label=u'شماره تلفن',
                                help_text=u'شماره تماس اصلی شرکت برای برقراری ارتباط, این قسمت را حتما پر کنید. پیش شماره شهر خود را نیز حتما درج کنید.')
    mobile_num = forms.CharField(required=False, label=u'شماره تلفن همراه')
    postal_code = forms.CharField(required=False, label=u'کد پستی')
    state = forms.CharField(required=True, label=u'استان', max_length=100)
    city = forms.CharField(required=True, label=u'شهر', max_length=100)
    address = forms.CharField(required=True, label=u'آدرس',
                              widget=forms.Textarea(attrs={'style': 'width:400px;margin-top:-15px'}))

    def clean_postal_code(self):
        data = self.cleaned_data['postal_code']
        ok = True
        if not data:
            return data
        for i in data.split('-'):
            if not i.isdigit():
                ok = False
                break
        if ok:
            return data
        else:
            print('it\'s not')
            raise forms.ValidationError((u" کدپستی واردشده نامعتبر است."), code='notNumber')


    def clean_phone_num(self):
        data = self.cleaned_data['phone_num']
        ok = True

        for i in data.split('-'):
            if not i.isdigit():
                ok = False
                break
        if ok:
            return data
        else:
            print('it\'s not')
            raise forms.ValidationError((u"شماره تلفن واردشده نامعتبر است."), code='notNumber')

    def clean_mobile_num(self):
        data = self.cleaned_data['mobile_num']
        if not data:
            return data
        ok = True
        for i in data.split('-'):
            if not i.isdigit():
                ok = False
                break
        if ok:
            return data
        else:
            raise forms.ValidationError((u"شماره تلفن همراه واردشده نامعتبر است."), code='notNumber')




setattr(Field, 'is_textarea', lambda self: isinstance(self.widget, forms.Textarea))

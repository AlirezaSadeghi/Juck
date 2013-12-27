# -*- coding: utf-8 -*-

from django import forms
from persian_captcha import PersianCaptchaField
from django.forms.fields import Field


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
    pass


class JobSeekerRegisterForm2(forms.Form):
    pass


class JobSeekerRegisterForm3(forms.Form):
    pass


class JobSeekerRegisterForm4(forms.Form):
    pass


class EmployerRegisterForm1(forms.Form):
    email = forms.EmailField(required=True, label=u'پست الکترونیکی')
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label=u'رمز عبور')
    re_password = forms.CharField(widget=forms.PasswordInput(), required=True, label=u'تکرار رمز عبور')
    # connector_name = forms.CharField(required=True, label=u'نام شخص رابط')
    connector_rank = forms.CharField(required=True, label=u'سمت شخص رابط')
    captcha = PersianCaptchaField(required=True, label=u'کد امنیتی')


class EmployerRegisterForm2(forms.Form):
    company_name = forms.CharField(required=True, label=u'نام شرکت')
    company_type = forms.CharField(required=True, label=u'نوع شرکت')
    reg_num = forms.CharField(required=True, label=u'شماره ثبت')
    foundation_year = forms.IntegerField(required=True, label=u'سال تاسیس')
    manager = forms.CharField(required=True,label= u'نام مدیرعامل')
    field = forms.CharField(required=True, label=u'زمینه فعالیت')


class EmployerRegisterForm3(forms.Form):
    website = forms.URLField(required=False, label=u'وب سایت')
    phone_num = forms.IntegerField(required=True, label=u'شماره تلفن')
    mobile_num = forms.IntegerField(required=False, label=u'شماره تلفن همراه')
    postal_code = forms.CharField(required=False, label=u'کد پستی')
    address = forms.CharField(required=True, widget=forms.Textarea(), label=u'آدرس')


setattr(Field, 'is_textarea', lambda self: isinstance(self.widget, forms.Textarea ))

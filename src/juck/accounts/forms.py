# -*- coding: utf-8 -*-

from django import forms
from persian_captcha import PersianCaptchaField


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
    email = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    re_password = forms.CharField(widget=forms.PasswordInput, required=True)
    connector_name = forms.CharField(required=True)
    captcha = PersianCaptchaField()


class EmployerRegisterForm2(forms.Form):
    company_name = forms.CharField(required=True)
    company_type = forms.CharField(required=True)
    reg_num = forms.CharField(required=True)
    foundation_year = forms.CharField(required=True)
    manager = forms.CharField(required=True)
    field = forms.CharField(required=True)


class EmployerRegisterForm3(forms.Form):
    postal_code = forms.CharField()
    website = forms.URLField()
    phone_num = forms.IntegerField()
    mobile_num = forms.IntegerField(required=True)
    address = forms.CharField(required=True, widget=forms.Textarea())

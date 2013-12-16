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
    pass

class EmployerRegisterForm2(forms.Form):
    pass

class EmployerRegisterForm3(forms.Form):
    pass
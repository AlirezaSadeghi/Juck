# -*- coding: utf-8 -*-

from captcha.conf           import settings as captcha_settings
from captcha.models         import CaptchaStore, get_safe_now
from captcha.fields         import CaptchaField, CaptchaTextInput

from django.forms.fields    import CharField
from django.forms           import ValidationError

from django.utils.translation              import ugettext_lazy as _



class PersianCaptchaField(CaptchaField):
    def __init__(self, *args, **kwargs):
        fields = (
            CharField(show_hidden_initial=True),
            CharField(),
            )
        if 'error_messages' not in kwargs or 'invalid' not in kwargs.get('error_messages'):
            if 'error_messages' not in kwargs:
                kwargs['error_messages'] = dict()
            kwargs['error_messages'].update(dict(invalid=_(u'کد امنیتی وارد شده صحیح نمی باشد')))

        widget_kwargs = dict(
            output_format=kwargs.get('output_format', None) or captcha_settings.CAPTCHA_OUTPUT_FORMAT
        )
        for k in ('output_format',):
            if k in kwargs:
                del(kwargs[k])
        super(CaptchaField, self).__init__(fields=fields, widget=CaptchaTextInput(**widget_kwargs), *args, **kwargs)


    def clean(self, value):
        super(CaptchaField, self).clean(value)
        response, value[1] = value[1].strip().lower(), ''
        CaptchaStore.remove_expired()
        try:
            store = CaptchaStore.objects.get(response=response, hashkey=value[0], expiration__gt=get_safe_now())
            store.delete()
        except Exception:
            raise ValidationError(getattr(self, 'error_messages', dict()).get('invalid', _(u'.کد امنیتی وارد شده صحیح نمی باشد')))
        return value

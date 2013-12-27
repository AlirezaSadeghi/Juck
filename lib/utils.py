from django.http.response import HttpResponse
import json
from django.conf import settings
from django.core.mail   import send_mail



def send_html_mail(receiver, subject, text='', html=''):
    send_mail(subject, html, settings.EMAIL_SENDER, [receiver, ])


def json_response(arr):
    return HttpResponse(json.dumps(arr), mimetype='application/json')


def create_pagination_range(current, max_num):
    limit = 4
    counter = 0
    i = current - 1
    rng = []

    while i > 0:
        counter += 1
        if counter > 2:
            break
        rng.append(i)
        i -= 1
    limit -= counter if counter == 0 else counter - 1
    rng.reverse()

    rng.append(current)

    i = current + 1
    counter = 0
    while i <= max_num:
        counter += 1
        if counter > limit:
            break
        rng.append(i)
        i += 1

    return rng
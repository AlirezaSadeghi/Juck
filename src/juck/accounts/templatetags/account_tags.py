
from django.template import Library
from juck.accounts  import views

register = Library()


@register.assignment_tag(takes_context=True)
def get_user_type(context):
    user = context['user']
    return views.get_user_type(user.pk)
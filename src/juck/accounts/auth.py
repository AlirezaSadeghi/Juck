from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist
from models import JuckUser as User


class JuckAuthenticationBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except ObjectDoesNotExist:
            pass
        return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            pass
        return None


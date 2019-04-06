from django.conf import settings
from django.contrib.auth.backends import ModelBackend

from order.models import AccountUser

class CustomUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = AccountUser.objects.get(username=username)
        except AccountUser.DoesNotExist:
            return None

        if not user.check_password(password):
            return None

        return user

    def get_user(self, user_id):
        try:
            return AccountUser.objects.get(pk=user_id)
        except AccountUser.DoesNotExist:
            return None


from django.conf import settings
from django.apps import apps
from django.contrib.auth.backends import ModelBackend

class CustomUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = self.user_class.objects.get(username=username)
            if user.check_password(password):
                return user
        except self.user_class.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return self.user_class.objects.get(pk=user_id)
        except self.user_class.DoesNotExist:
            return None

    @property
    def user_class(self):
        return apps.get_model('order', 'AccountUser')


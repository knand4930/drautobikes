from django.contrib.auth.backends import ModelBackend
from .models import *


class CustomUserBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, otp=None, **kwargs):
        try:
            user = User.objects.get(phone_number=phone_number, otp=otp)
        except User.DoesNotExist:
            return None
        return user

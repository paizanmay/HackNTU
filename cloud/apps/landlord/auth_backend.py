# -*- coding: utf-8 -*-
from django.contrib.auth.backends import ModelBackend

from apps.landlord.models import LandlordUser

class AuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None, request=None):
        try:
            user = LandlordUser.objects.get(username=username)
            if user.check_password(password):
                return user
            else:
                return None
        except Exception:
            return None

    def get_user(self, user_id):
        try:
            return LandlordUser.objects.get(pk=user_id)
        except LandlordUser.DoesNotExist:
            return None

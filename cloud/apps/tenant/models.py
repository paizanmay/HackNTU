# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import uuid
import requests

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings


def generate_uuid():
    return str(uuid.uuid4())


class TenantUser(AbstractBaseUser):
    uuid = models.CharField(max_length=40L, default=generate_uuid)
    username = models.CharField(unique=True, max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    fb_id = models.CharField(max_length=100L, db_index=True, unique=True, null=True)
    sender_id = models.CharField(max_length=50L, db_index=True, null=True)
    profile_img_url = models.TextField(null=True, blank=True)
    live_room = models.ForeignKey("landlord.Room", null=True, on_delete=models.SET_NULL, related_name='tenant_user')

    bank_code = models.CharField(max_length=3L, blank=True)
    bank_account = models.CharField(max_length=50L, blank=True)

    USERNAME_FIELD = "username"

    class Meta:
        app_label = "tenant"
        db_table = "tenant_user"

    @classmethod
    def register_user(cls, sender_id):
        user_profile_url = "https://graph.facebook.com/v2.6/{user_id}?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token={token}".format(user_id=sender_id, token=settings.PAGE_ACCESS_TOKEN)
        user_profile = requests.get(user_profile_url).json()

        user_name = user_profile["last_name"] + " " + user_profile["first_name"]
        user, created = TenantUser.objects.get_or_create(name=user_name, defaults={"sender_id": sender_id, "profile_img_url": user_profile["profile_pic"]})
        return user


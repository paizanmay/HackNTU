# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser


def generate_uuid():
    return str(uuid.uuid4())


class TenantUser(AbstractBaseUser):
    uuid = models.CharField(max_length=40L, default=generate_uuid)
    username = models.CharField(unique=True, max_length=100, null=True, blank=True)
    fb_id = models.CharField(max_length=100L, db_index=True, unique=True, null=True)
    sender_id = models.CharField(max_length=50L, db_index=True, null=True)
    profile_img_id = models.CharField(max_length=100L, db_index=True, null=True)
    live_room = models.ForeignKey("landlord.Room", null=True, on_delete=models.SET_NULL, related_name='tenant_user')

    USERNAME_FIELD = "username"

    class Meta:
        app_label = "tenant"
        db_table = "tenant_user"

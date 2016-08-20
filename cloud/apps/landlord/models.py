# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser


def generate_uuid():
    return str(uuid.uuid4())


class Room(models.Model):
    uuid = models.CharField(max_length=36L, default=generate_uuid)
    rental = models.IntegerField(null=True)
    name = models.CharField(max_length=100L, null=True, blank=True)
    address = models.TextField(null=True, blank=True)


    class Meta:
        app_label = "landlord"
        db_table = 'landlord_room'

# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager


def generate_uuid():
    return str(uuid.uuid4())


class LandlordUser(AbstractBaseUser):
    uuid = models.CharField(max_length=36L, default=generate_uuid)
    username = models.CharField(unique=True, max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    bank_account = models.CharField(max_length=100L, null=True, blank=True)

    USERNAME_FIELD = "username"

    objects = UserManager()

    class Meta:
        app_label = "landlord"
        db_table = "landlord_user"


class Room(models.Model):
    uuid = models.CharField(max_length=36L, default=generate_uuid)
    landlord_user = models.ForeignKey("LandlordUser", null=True, related_name='room')
    rental = models.IntegerField(null=True)
    name = models.CharField(max_length=100L, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    notification_date = models.IntegerField(null=True)
    deadline_date = models.IntegerField(null=True)

    class Meta:
        app_label = "landlord"
        db_table = "landlord_room"


class RoomOrder(models.Model):
    uuid = models.CharField(max_length=36L, default=generate_uuid)
    room = models.ForeignKey("Room", related_name='room_order')
    amount = models.IntegerField(default=0)
    deadline = models.DateTimeField(null=True)

    class Meta:
        app_label = "landlord"
        db_table = "room_order"


class RoomOrderPart(models.Model):
    uuid = models.CharField(max_length=36L, default=generate_uuid)
    room_order = models.ForeignKey("RoomOrder", related_name='room_order_part')
    tenant = models.ForeignKey("tenant.TenantUser", related_name="room_order_part")
    amount = models.IntegerField(default=0)
    card_number = models.CharField(max_length=20L, null=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        app_label = "landlord"
        db_table = "room_order_part"




# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import uuid

from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, UserManager
from enum import IntEnum

from apps.fb_bot.bot import bot
from apps.fb_bot.template import *


def generate_uuid():
    return str(uuid.uuid4())


class LandlordUser(AbstractBaseUser):
    uuid = models.CharField(max_length=36L, default=generate_uuid)
    username = models.CharField(unique=True, max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    bank_code = models.CharField(max_length=3L, null=True, blank=True)
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

    class OrderType(IntEnum):
        room = 0
        water = 1
        electric = 2
        internet = 3
        other = 4
    ORDER_TYPE_CHOICES = tuple((enum_item.value, enum_item.name) for enum_item in OrderType)

    uuid = models.CharField(max_length=36L, default=generate_uuid)
    room = models.ForeignKey("Room", related_name='room_order')
    name = models.CharField(max_length=50, blank=True, default="房租訂單")
    order_type = models.IntegerField(choices=ORDER_TYPE_CHOICES, default=OrderType.room.value)
    amount = models.IntegerField(default=0)
    deadline = models.DateTimeField(null=True, auto_now_add=True)

    paid_bank_code = models.CharField(max_length=3, blank=True, default="")
    paid_bank_account = models.CharField(max_length=50, blank=True, default="")

    create_user = None

    class Meta:
        app_label = "landlord"
        db_table = "room_order"

    @property
    def is_paid(self):
        return not self.room_order_part.filter(is_paid=False).exists()


class RoomOrderPart(models.Model):
    uuid = models.CharField(max_length=36L, default=generate_uuid)
    room_order = models.ForeignKey("RoomOrder", related_name='room_order_part')
    tenant = models.ForeignKey("tenant.TenantUser", related_name="room_order_part")
    replace_pay_user = models.ForeignKey("tenant.TenantUser", null=True)
    amount = models.IntegerField(default=0)
    card_number = models.CharField(max_length=20L, null=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        app_label = "landlord"
        db_table = "room_order_part"

@receiver(models.signals.pre_save, sender=RoomOrderPart)
def check_order_paid(instance, **signal_kwargs):
    if instance.pk is not None:
        previous_paid_status = RoomOrderPart.objects.get(pk=instance.pk).is_paid
        if previous_paid_status is False and instance.is_paid is True:  # 繳款成功
            is_paid_by_replace = instance.replace_pay_user is not None
            order_name = instance.room_order.name
            user_name = instance.tenant.name

            if is_paid_by_replace is False:
                success_msg = "{order_name}:付款成功".format(order_name=order_name)
                bot.send_text_message(instance.tenant.sender_id, success_msg)
            else:
                pay_user_name = instance.replace_pay_user.name
                success_msg = "{order_name}:{pay_user_name}已代替您繳款".format(order_name=order_name, pay_user_name=pay_user_name, user_name=user_name)
                bot.send_text_message(instance.tenant.sender_id, success_msg)
                replace_success_msg = "{order_name}:您已代替{user_name}繳款成功".format(order_name=order_name, user_name=user_name)
                bot.send_text_message(instance.replace_pay_user.sender_id, replace_success_msg)


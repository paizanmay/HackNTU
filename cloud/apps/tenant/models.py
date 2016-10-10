# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import uuid
import requests

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.dispatch import receiver
from django.conf import settings

from apps.fb_bot.bot import bot
from apps.fb_bot.template import *
from apps.fb_bot.libs import *


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
    live_room_amount = models.IntegerField(default=0)

    cust_id = models.CharField(max_length=30, default="C199063165", blank=True)
    bank_code = models.CharField(max_length=3L, default="822", blank=True)
    bank_account = models.CharField(max_length=50L, default="0000107549900069", blank=True)

    USERNAME_FIELD = "username"

    class Meta:
        app_label = "tenant"
        db_table = "tenant_user"

    @classmethod
    def register_user(cls, sender_id):
        user_profile_url = "https://graph.facebook.com/v2.6/{user_id}?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token={token}".format(user_id=sender_id, token=settings.PAGE_ACCESS_TOKEN)
        user_profile = requests.get(user_profile_url).json()

        if isEnglish(user_profile["last_name"]) is True:
            user_name = user_profile["first_name"] + " " + user_profile["last_name"]
        else:
            user_name = user_profile["last_name"] + user_profile["first_name"]

        user, created = TenantUser.objects.get_or_create(name=user_name, defaults={"sender_id": sender_id, "profile_img_url": user_profile["profile_pic"]})
        return user


@receiver(models.signals.pre_save, sender=TenantUser)
def change_live_room(instance, **signal_kwargs):
    if instance.pk is not None:
        old_room = TenantUser.objects.get(pk=instance.pk).live_room
        new_room = instance.live_room

        if new_room != old_room:
            if new_room is not None:
                for user in new_room.tenant_user.all().exclude(pk=instance.pk):
                    send_change_room_signal(instance, user, True)

            if old_room is not None:
                for user in old_room.tenant_user.all().exclude(pk=instance.pk):
                    send_change_room_signal(instance, user, False)


def send_change_room_signal(moved_user, leave_user, is_live_in):
    if is_live_in is True:
        return bot.send_generic_message(leave_user.sender_id, change_room_fee_for_other_in(moved_user, leave_user))
    else:
        return bot.send_generic_message(leave_user.sender_id, change_room_fee_for_other_out(moved_user, leave_user))


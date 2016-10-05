# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import urllib

from django.conf import settings
from django.db.models import Q
from pymessenger.bot import Bot
import requests

from apps.tenant.models import *
from apps.landlord.models import *
from apps.fb_bot.template import *
from apps.fb_bot.constant import *


bot = Bot(settings.PAGE_ACCESS_TOKEN)
SERVER_URL = settings.SERVER_URL


def send_create_order_signal(order):
    order_part_list = order.room_order_part.all()
    create_user_name = "" if order.create_user is None else order.create_user.name
    for order_part in order_part_list:
        part = RoomOrderPart.objects.get(pk=order_part.pk)
        bot.send_generic_message(order_part.tenant.sender_id, pay_new_order(part, create_user_name))

def send_account_link(sender_id):
    return bot.send_generic_message(sender_id, register_user_page(sender_id))

def send_payment_page(sender_id, room_uuid, user_uuid):
    return bot.send_button_message(sender_id, *welcome_page(room_uuid, user_uuid))

def send_change_room_fee_result(create_user, room):
    title, button = change_room_fee_result(create_user, room.tenant_user.all())

    for user in room.tenant_user.all():
        bot.send_button_message(user.sender_id, title, button)

    return True 

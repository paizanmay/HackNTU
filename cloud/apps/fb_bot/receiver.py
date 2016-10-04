# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import urllib
import logging

from django.conf import settings
from django.db.models import Q
from pymessenger.bot import Bot
import requests

from apps.tenant.models import *
from apps.landlord.models import *
from apps.fb_bot.template import *
from apps.fb_bot.constant import OrderImage
from apps.fb_bot.sender import *


bot = Bot(settings.PAGE_ACCESS_TOKEN)
SERVER_URL = settings.SERVER_URL
logger = logging.getLogger(__name__)

class Receiver(object):
    def __init__(self, event):
        self.user_sender_id = event["sender"]["id"]
        self.page_sender_id = event["recipient"]["id"]
        self.msg_time = event["timestamp"]

        self.user = TenantUser.objects.filter(sender_id=self.user_sender_id).first()

    def is_auth(self):
        return self.user is not None

    def has_room(self):
        return self.user.live_room is not None

    def register(self):
        self.user = TenantUser.register_user(self.user_sender_id)
        return self.user

    def livein(self):
        return bot.send_text_message(self.user_sender_id, "還未入住房間，請上傳房間QRCode來辦理入住")


class MessageReceiver(Receiver):
    def __init__(self, event):
        super(MessageReceiver, self).__init__(event)
        self.message = event["message"]
        self.is_echo = self.message.get("is_echo")
        self.message_text = self.message.get("text")
        self.message_attachments = self.message.get("attachments")
        self.quick_reply = self.message.get("quick_reply")

    def has_room(self):
        if self.message_attachments is not None:
            return True
        return super(MessageReceiver, self).has_room()

    def send(self):
        if self.is_echo:
            return

        if self.message_attachments is not None:
            qrcode_url = self.message_attachments[0]["payload"]["url"]
            safe_qrcode_url = urllib.quote_plus(qrcode_url)
            qrcode_decode = requests.get("http://api.qrserver.com/v1/read-qr-code/?fileurl=%s" % safe_qrcode_url)
            room_uuid = qrcode_decode.json()[0]["symbol"][0]["data"]
            print(room_uuid)
            room = Room.objects.filter(uuid=room_uuid).first()
            if room is None:
                return bot.send_text_message(self.user_sender_id, "QRCode 無法辨識，請重新拍照上傳")
            return bot.send_button_message(self.user_sender_id, *room_info_check(room))

        return send_payment_page(self.user_sender_id, self.user.live_room.uuid, self.user.uuid)


class AccountLinkReceiver(Receiver):
    def __init__(self, event):
        super(AccountLinkReceiver, self).__init__(event)
        self.status = event["account_linking"]["status"]
        self.auth_code = event["account_linking"]["authorization_code"]

    def send(self):
        user = TenantUser.objects.get(uuid=self.auth_code)
        user.sender_id = self.user_sender_id
        user.save()
        self.user = user
        return bot.send_text_message(self.user_sender_id, "註冊成功")

    def is_auth(self):
        return True

class PostBackReceiver(Receiver):
    def __init__(self, event):
        super(PostBackReceiver, self).__init__(event)
        self.postback_payload = event["postback"]["payload"]

    def has_room(self):
        if "LIVE_IN_ROOM" in self.postback_payload:
            return True
        return super(PostBackReceiver, self).has_room()

    def send(self):
        if self.postback_payload == "TENANT_WANT_TO_PAY_ORDER":
            orders = self.user.room_order_part.filter(is_paid=False)
            elements = []
            for order in orders:
                elements.append(rent_order_simple(order.room_order.name, order.room_order.deadline.date(), order))
            if len(elements) > 0:
                return bot.send_generic_message(self.user_sender_id, elements)
            return bot.send_text_message(self.user_sender_id, "費用已全數繳清")

        elif self.postback_payload == "DID_OTHER_PAY_ORDER":
            elements = []
            all_room_order = self.user.live_room.room_order.all()
            for room_order in all_room_order:
                someone_not_pay = room_order.room_order_part.filter(is_paid=False).exists()
                if someone_not_pay is True:
                    unpaid_order_list = room_order.room_order_part.filter(is_paid=False)
                    unpaid_name_list = ",".join([name[0] for name in unpaid_order_list.values_list("tenant__name")])
                    paid_order_list = room_order.room_order_part.filter(is_paid=True)
                    paid_name_list = ",".join([name[0] for name in paid_order_list.values_list("tenant__name")])
                    user_order = room_order.room_order_part.filter(tenant=self.user).first()
                    data = {
                        "title": room_order.name,
                        "paid_name": paid_name_list,
                        "unpaid_name": unpaid_name_list,
                        "deadline": room_order.deadline.date(),
                        "room_order_uuid": room_order.uuid,
                        "user_order_uuid": None if user_order is None else user_order.uuid,
                        "is_paid": paid_order_list.filter(tenant=self.user).exists(),
                        "order": room_order,
                    }
                    elements.append(rent_order_with_name(**data))
            if len(elements) > 0:
                return bot.send_generic_message(self.user_sender_id, elements)
            else:
                return bot.send_text_message(self.user_sender_id, "費用已全數繳清")

        elif "PAY_FOR_OTHER$" in self.postback_payload:
            room_order_uuid = self.postback_payload.split("$")[-1]
            room_order = RoomOrder.objects.get(uuid=room_order_uuid)
            others_unpaid_order = room_order.room_order_part.filter(is_paid=False)
            return bot.send_generic_message(self.user_sender_id, pay_for_others_order(room_order.name, others_unpaid_order, self.user.uuid))

        elif self.postback_payload == "LOGIN":
            return send_account_link(self.user_sender_id)

        elif "LIVE_IN_ROOM" in self.postback_payload:
            room_uuid = self.postback_payload.split("$")[-1]
            room = Room.objects.get(uuid=room_uuid)
            self.user.live_room = room
            self.user.save()
            bot.send_text_message(self.user_sender_id, "入住成功")
            return send_payment_page(self.user_sender_id, self.user.live_room.uuid, self.user.uuid)

        elif self.postback_payload == "PAY_RENT":
            return send_payment_page(self.user_sender_id, self.user.live_room.uuid, self.user.uuid)

        elif self.postback_payload == "SETTING_ACCOUNT":
            bot.send_button_message(self.user_sender_id, *settting_account(self.user.uuid))

        elif self.postback_payload == "CHANGE_ROOM_FEE":
            bot.send_generic_message(self.user_sender_id, change_room_fee_for_self(self.user))


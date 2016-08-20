# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf import settings
from django.db.models import Q
from pymessenger.bot import Bot
import requests

from apps.tenant.models import *
from apps.landlord.models import *


bot = Bot(settings.PAGE_ACCESS_TOKEN)
SERVER_URL = settings.SERVER_URL

class Receiver(object):
    def __init__(self, event):
        self.user_sender_id = event["sender"]["id"]
        self.page_sender_id = event["recipient"]["id"]
        self.msg_time = event["timestamp"]

        user = TenantUser.objects.filter(sender_id=self.user_sender_id).first()
        if user is not None:
            self.user = user


class MessageReceiver(Receiver):
    def __init__(self, event):
        super(MessageReceiver, self).__init__(event)
        self.message = event["message"]
        self.is_echo = self.message.get("is_echo")
        self.message_text = self.message.get("text")
        self.message_attachments = self.message.get("attachments")
        self.quick_reply = self.message.get("quick_reply")

    def send(self):
        if self.is_echo:
            return
        elif self.quick_reply:
            quick_reply_payload = self.quick_reply.get('payload')
            if quick_reply_payload == "TENANT_WANT_TO_PAY_ORDER":
                user_need_pay_order = self.user.room_order_part.all()
                elements = []
                for order in user_need_pay_order:
                    elements.append({
                        "title": "九月房租 | %s" % order.amount,
                        "subtitle": "繳交期限:%s" % str(order.room_order.deadline),
                        "image_url": SERVER_URL + "/static/imgs/Artboard Copy.jpg",
                        "buttons": [{
                            "type": "web_url",
                            "url": SERVER_URL + "/tenant/tenant_pay_order_page/" + order.uuid,
                            "title": "我要繳費"
                        }]
                    })
                bot.send_generic_message(self.user_sender_id, elements)

            return

        if u"註冊" in self.message_text:
            user_name = self.message_text.split(":")[-1]
            user = TenantUser.objects.filter(name__contains=user_name).first()
            user.sender_id = self.user_sender_id
            user.save()

            # buttons = [{
            #     "type": "postback",
            #     "title": "我要繳哪些錢",
            #     "payload": "TENANT_WANT_TO_PAY_ORDER"
            # }]
            title = "你的Rent交了嗎？\n\n我是小交，可以協助你繳交房租/水電/網路費用、查看繳費狀況哦！"
            msg = {
                "text": title,
                "metadata": "TENANT_FIRST_CHOICE",
                "quick_replies": [
                    {
                        "content_type":"text",
                        "title":"我要繳哪些錢",
                        "payload":"TENANT_WANT_TO_PAY_ORDER"
                    },
                    {
                        "content_type":"text",
                        "title":"我要調整設定",
                        "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_ADJUST_SETTING"
                    }
                ]
            }

            bot.send_message(self.user_sender_id, msg)
            return
        else:
            bot.send_text_message(self.user_sender_id, self.message_text)

        return

    def send_account_link(self):
        data = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "Welcome. Link your account.",
                    "buttons":[{
                        "type": "account_link",
                        "url": SERVER_URL + "/authorize"
                    }]
                }
            }
        }
        bot.send_message(self.user_sender_id, data)


class AccountLinkReceiver(Receiver):
    def __init__(self, event):
        super(AccountLinkReceiver, self).__init__(event)
        self.status = event["account_linking"]["status"]
        self.auth_code = event["account_linking"]["authorization_code"]


class PostBackReceiver(Receiver):
    def __init__(self, event):
        super(PostBackReceiver, self).__init__(event)
        self.postback_payload = event["postback"]["payload"]

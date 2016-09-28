# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from datetime import datetime

from django.conf import settings
from pymessenger.bot import Bot

from apps.fb_bot.constant import OrderImage

bot = Bot(settings.PAGE_ACCESS_TOKEN)
SERVER_URL = settings.SERVER_URL

def welcome_page(room_uuid, user_uuid):
    title = "你的Rent交了嗎？\n\n我是小交，可以協助你繳交房租/水電/網路費用、查看繳費狀況哦！"
    buttons = [
        {
            "type":"postback",
            "title":"我要繳哪些錢",
            "payload":"TENANT_WANT_TO_PAY_ORDER"
        },
        {
            "type":"postback",
            "title":"大家繳費了沒",
            "payload":"DID_OTHER_PAY_ORDER"
        },
        {
            "type":"web_url",
            "title":"新增待繳費用",
            "url": SERVER_URL + "/tenant/create_order_page/?room_uuid=%s&user_uuid=%s" % (room_uuid, user_uuid)
        }
    ]

    return title, buttons

def register_user_page():
    msg = {
        "title": "登記使用者資訊",
        "subtitle": "請先登記您的房客資訊，才能繼續使用",
        "image_url": OrderImage.logo,
        "buttons":[{
            "type": "account_link",
            "url": SERVER_URL + "/authorize"
        }]
    }

    return [msg]

def rent_order_simple(title, deadline, order):
    msg = {
        "title": title,
        "subtitle": "繳費期限:%s" % str(deadline),
        "image_url": OrderImage.get_img_url(order),
        "buttons": [{
            "type": "web_url",
            "url": SERVER_URL + "/tenant/tenant_pay_order_page/" + order.uuid,
            "title": "我要繳費"
        }]
    }
    return msg

def rent_order_with_name(title, paid_name, unpaid_name, deadline, room_order_uuid, user_order_uuid, is_paid, order):
    msg = {
        "title": title,
        "subtitle": "已繳名單:{paid_name} \n未繳名單:{unpaid_name} \n繳費期限:{deadline}".format(paid_name=paid_name, unpaid_name=unpaid_name, deadline=str(deadline)),
        "image_url": OrderImage.get_img_url(order),
        "buttons": [
            {
                "type":"postback",
                "title":"我要代繳",
                "payload":"PAY_FOR_OTHER$%s" % room_order_uuid
            }
        ]
    }
    if is_paid is False and user_order_uuid is not None:
        msg["buttons"].append(
            {
                "type": "web_url",
                "url": SERVER_URL + "/tenant/tenant_pay_order_page/" + user_order_uuid,
                "title": "我要繳費"
            }
        )

    return msg

def pay_for_others_order(title, others_order, replace_pay_user):
    msg = {
        "title": title,
        "image_url": OrderImage.get_img_url(others_order[0]),
        "buttons": []
    }

    for order in others_order:
        msg["buttons"].append(
            {
                "type": "web_url",
                "title": "{name} ${price}".format(name=order.tenant.name, price=order.amount),
                "url": SERVER_URL + "/tenant/tenant_pay_order_page/" + order.uuid + "?pay_user_uuid=" + replace_pay_user
            }
        )
    return [msg]

def pay_new_order(order, create_user):
    msg = {
        "title": "新增應繳費用 | %s" % order.room_order.name,
        "subtitle": "新增人: {create_user} \n 費用名稱: {order_name} \n 應繳總額: {amount} \n 繳費期限: {deadline}".format(create_user=create_user, order_name=order.room_order.name, amount=order.amount, deadline=str(order.room_order.deadline)[:10]),
        "image_url": OrderImage.get_img_url(order),
        "buttons": [
            {
                "type":"web_url",
                "title":"前往繳費 $%s" % order.amount,
                "url": SERVER_URL + "/tenant/tenant_pay_order_page/%s" % order.uuid
            }
        ]
    }

    return [msg]

def room_info_check(room):
    title = "請確認是否要入住以下房間 \n 名稱: {name} \n 租金: {rent} \n 地址: {address}".format(name=room.name, rent=room.rental, address=room.address)
    buttons = [
        {
            "type": "postback",
            "title": "確認住房",
            "payload": "LIVE_IN_ROOM$%s" % room.uuid
        },
        {
            "type": "postback",
            "title": "取消住房",
            "payload": "UNDEFINED"
        }
    ]

    return title, buttons





# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from datetime import datetime

from django.conf import settings
from pymessenger.bot import Bot

from apps.fb_bot.constant import OrderImage

bot = Bot(settings.PAGE_ACCESS_TOKEN)
SERVER_URL = settings.SERVER_URL

def intro_page(user):
    title = "%s您好，歡迎使用懶交！ \n您已入住成功，請先設定你的銀行帳號才可以繳款喔！" % user.name
    buttons = [
        {
            "type":"web_url",
            "title":"💰設定銀行帳號",
            "url": SERVER_URL + "/tenant/setting_account_page?user_uuid=" + user.uuid
        }
    ]
    return title, buttons

def welcome_page(room_uuid, user_uuid):
    title = "你的Rent交了嗎？\n\n我是小交，可以協助你繳交房租/水電/網路費用、查看繳費狀況哦！"
    buttons = [
        {
            "type":"postback",
            "title":"💵 我要繳哪些錢",
            "payload":"TENANT_WANT_TO_PAY_ORDER"
        },
        {
            "type":"postback",
            "title":"🔎 大家繳費了沒",
            "payload":"DID_OTHER_PAY_ORDER"
        },
        {
            "type":"web_url",
            "title":"✚ 新增待繳費用",
            "url": SERVER_URL + "/tenant/create_order_page/?room_uuid=%s&user_uuid=%s" % (room_uuid, user_uuid)
        }
    ]

    return title, buttons

def settting_account(user_uuid):
    title = "請點擊設定銀行帳號"
    buttons = [
        {
            "type":"web_url",
            "title":"設定帳號",
            "url": SERVER_URL + "/tenant/setting_account_page?user_uuid=" + user_uuid
        }
    ]
    return title, buttons

def register_user_page(sender_id):
    msg = {
        "title": "登記使用者資訊",
        "subtitle": "請先登記您的房客資訊，才能繼續使用",
        "image_url": OrderImage.logo,
        "buttons":[{
            "type": "account_link",
            "url": SERVER_URL + "/authorize/"+ sender_id
        }]
    }

    return [msg]

def rent_order_simple(order):
    msg = {
        "title": "%s | %s" % (order.room_order.name, order.amount),
        "subtitle": "繳費期限:%s" % str(order.room_order.deadline.date()),
        "image_url": OrderImage.get_img_url(order),
        "buttons": [{
            "type": "web_url",
            "url": SERVER_URL + "/tenant/tenant_pay_order_page/" + order.uuid,
            "title": "💳 我要繳費"
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
                "title":"👼 我要代繳",
                "payload":"PAY_FOR_OTHER$%s" % room_order_uuid
            }
        ]
    }
    if is_paid is False and user_order_uuid is not None:
        msg["buttons"].append(
            {
                "type": "web_url",
                "url": SERVER_URL + "/tenant/tenant_pay_order_page/" + user_order_uuid,
                "title": "💳 我要繳費"
            }
        )

    return msg

def pay_for_others_order(room_order, others_order, replace_pay_user):
    msg = {
        "title": "%s | $%s" % (room_order.name, room_order.amount),
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
    }

    if order.is_paid is False:
        msg["buttons"] = [
            {
                "type":"web_url",
                "title":"💳 前往繳費 $%s" % order.amount,
                "url": SERVER_URL + "/tenant/tenant_pay_order_page/%s" % order.uuid
            }
        ]

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

def change_room_fee_for_other_in(moved_user, leave_user):
    title = "{name}已入住，請問要調整房間費用分配嗎？".format(name=moved_user.name)
    msg = {
        "title": title,
        "image_url": moved_user.profile_img_url,
        "buttons": [
            {
                "type":"web_url",
                "title":"🔎 我要調整",
                "url":SERVER_URL + "/tenant/change_room_fee_page/?room_uuid=%s&user_uuid=%s" % (leave_user.live_room.uuid, leave_user.uuid)
            }
        ]
    }

    return [msg]

def change_room_fee_for_other_out(moved_user, leave_user):
    title = "{name}已搬離，請問要調整房間費用分配嗎？".format(name=moved_user.name)
    msg = {
        "title": title,
        "image_url": moved_user.profile_img_url,
        "buttons": [
            {
                "type":"web_url",
                "title":"🔎 我要調整",
                "url":SERVER_URL + "/tenant/change_room_fee_page/?room_uuid=%s&user_uuid=%s" % (leave_user.live_room.uuid, leave_user.uuid)
            }
        ]
    }

    return [msg]

def change_room_fee_for_self(user):
    title = "請問要調整房間費用分配嗎？"
    msg = {
        "title": title,
        "image_url": user.profile_img_url,
        "buttons": [
            {
                "type":"web_url",
                "title":"🔎 我要調整",
                "url":SERVER_URL + "/tenant/change_room_fee_page/?room_uuid=%s&user_uuid=%s" % (user.live_room.uuid, user.uuid)
            }
        ]
    }

    return [msg]

def change_room_fee_result(create_user, user_list):
    title = "%s已更動房間費用分配 \n房間分配費用結果：\n\n" % create_user.name
    idx = 1
    for user in user_list:
        title += "%s. %s: $%s \n" % (idx, user.name, user.live_room_amount)
        idx += 1

    title += "\n請問您需要再次調整費用嗎？"

    buttons = [
        {
            "type":"web_url",
            "title":"🔎 我要調整",
            "url":SERVER_URL + "/tenant/change_room_fee_page/?room_uuid=%s&user_uuid=%s" % (create_user.live_room.uuid, create_user.uuid)
        }
    ]
    return title, buttons




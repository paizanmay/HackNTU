# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import urllib

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import requests

from apps.tenant.models import TenantUser
from apps.landlord.models import *

def register_room(request):
    user_id = request.GET.get("user_id")
    user_name = request.GET.get("user_name")
    room_id = request.GET.get("room_id")

    tenant_user, created = TenantUser.objects.get_or_create(fb_id=user_id, defaults={"name": user_name})
    want_live_room = Room.objects.get(uuid=room_id)

    return_data = {
        "room_id": want_live_room.uuid,
        "room_name": want_live_room.name,
        "room_address": want_live_room.address,
        "room_rental": want_live_room.rental,
        "tenant_id": tenant_user.uuid
    }

    return render_to_response("tenant/register_room.html", return_data)

def login_user(request):
    room_id = request.GET.get("room_id")
    account_linking_token = request.GET.get("account_linking_token")

    return_data = {"room_id": room_id, "account_linking_token": account_linking_token}
    return render_to_response("tenant/login_user.html", return_data)

def register_user(request):
    user_id = request.GET.get("user_id")
    user_name = request.GET.get("user_name")
    account_linking_token = request.GET.get("account_linking_token")

    get_psid_url_params = {
        "access_token": settings.PAGE_ACCESS_TOKEN,
        "fields": "recipient",
        "account_linking_token": account_linking_token
    }
    get_psid_url = "https://graph.facebook.com/v2.6/me?" + urllib.urlencode(get_psid_url_params)
    psid_response = requests.get(get_psid_url).json()
    psid = psid_response["recipient"]

    tenant_user, created = TenantUser.objects.get_or_create(fb_id=user_id, defaults={"name": user_name, "sender_id": psid})



    # return_data = {
    #     "room_id": want_live_room.uuid,
    #     "room_name": want_live_room.name,
    #     "room_address": want_live_room.address,
    #     "room_rental": want_live_room.rental,
    #     "tenant_id": tenant_user.uuid
    # }

    return HttpResponse("OK")

def tenant_pay_order_page(request, order_part_uuid):
    replace_pay_user = request.GET.get("pay_user_uuid")
    order_part = RoomOrderPart.objects.get(uuid=order_part_uuid)

    return_data = {
        "amount": order_part.amount,
        "user_name": order_part.tenant.name,
        "deadline": str(order_part.room_order.deadline.date()),
        "order_part_uuid": order_part_uuid,
        "replace_pay_user_uuid": replace_pay_user
    }

    if order_part.is_paid is True:
        return render_to_response("tenant/tenant_pay_order_success.html", return_data)

    return render_to_response("tenant/tenant_pay_order.html", return_data)

@csrf_exempt
def tenant_pay_order_success(request):
    order_part_uuid = request.POST.get("order_part_uuid")
    card_number = request.POST.get("card_number")
    replace_pay_user_uuid = request.POST.get("replace_pay_user_uuid")
    order_part = RoomOrderPart.objects.get(uuid=order_part_uuid)
    order_part.is_paid = True
    order_part.card_number = card_number[:4] + "********" + card_number[-4:]
    if replace_pay_user_uuid != "None":
        replace_pay_user = TenantUser.objects.get(uuid=replace_pay_user_uuid)
        order_part.replace_pay_user = replace_pay_user
    order_part.save()

    return_data = {
        "amount": order_part.amount,
        "user_name": order_part.tenant.name,
        "card_number": order_part.card_number,
        "order_part_uuid": order_part_uuid
    }

    return render_to_response("tenant/tenant_pay_order_success.html", return_data)


def create_order_page(request):
    user_uuid = request.GET.get("user_uuid")
    room_uuid = request.GET.get("room_uuid")
    room = Room.objects.get(uuid=room_uuid)
    room_tenant_list = room.tenant_user.all()

    return_data = {
        "room_uuid": room_uuid,
        "user_uuid": user_uuid,
        "room_tenant_list": room_tenant_list
    }    

    return render_to_response("tenant/create_order.html", return_data)

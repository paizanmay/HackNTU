# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

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

    return_data = {"room_id": room_id}
    return render_to_response("tenant/login_user.html", return_data)

def tenant_pay_order_page(request):
    order_part_uuid = request.GET.get("order_part_uuid")
    order_part = RoomOrderPart.objects.get(uuid=order_part_uuid)

    return_data = {
        "amount": order_part.amount,
        "user_name": order_part.tenant.name,
        "deadline": str(order_part.room_order.deadline.date()),
        "order_part_uuid": order_part_uuid
    }
    return render_to_response("tenant/tenant_pay_order.html", return_data)

@csrf_exempt
def tenant_pay_order_success(request):
    order_part_uuid = request.POST.get("order_part_uuid")
    card_number = request.POST.get("card_number")
    order_part = RoomOrderPart.objects.get(uuid=order_part_uuid)
    order_part.is_paid = True
    order_part.card_number = card_number[:4] + "********" + card_number[-4:]
    order_part.save()

    return_data = {
        "amount": order_part.amount,
        "user_name": order_part.tenant.name,
        "card_number": order_part.card_number,
        "order_part_uuid": order_part_uuid
    }

    return render_to_response("tenant/tenant_pay_order_success.html", return_data)




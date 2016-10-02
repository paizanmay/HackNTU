# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response

from apps.landlord.apis.serializers import RoomSerializer, RoomDetailSerializer
from apps.landlord.models import *
from apps.tenant.models import TenantUser
from apps.fb_bot.sender import *


class MultiSerializerViewSet(viewsets.ModelViewSet):
    serializers = {
        'default': None,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])


class RoomViewSet(MultiSerializerViewSet):
    """
    for MenuItemCategory all method
    """
    queryset = Room.objects.all()
    serializers = {
        'list': RoomSerializer,
        'create': RoomSerializer,
        'default': RoomDetailSerializer,
    }
    lookup_field = 'uuid'


class RoomOrderViewSet(APIView):

    def post(self, request):
        order_detail = request.data.get("order_detail")
        tenant_allocation = request.data.get("tenant_allocation")
        user_uuid = request.data.get("user_uuid")

        room = Room.objects.get(uuid=order_detail["room"])
        order_detail["room"] = room
        create_user = TenantUser.objects.get(uuid=user_uuid)
        order = RoomOrder(**order_detail)
        order.create_user = create_user
        order.save()

        for tenant in tenant_allocation:
            tenant_user = TenantUser.objects.get(uuid=tenant["uuid"])
            is_paid = create_user == tenant_user
            if int(tenant["amount"]) > 0:
                order_part = RoomOrderPart.objects.create(room_order=order, tenant=tenant_user, amount=tenant["amount"], is_paid=is_paid)

        send_create_order_signal(order)

        return Response("OK")





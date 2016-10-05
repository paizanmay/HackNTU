# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from apps.tenant.models import TenantUser
from apps.tenant.apis.serializers import TenantUserSerializer, TenantUserSimpleSerializer
from apps.landlord.models import Room
from apps.landlord.apis.serializers import RoomDetailSerializer
from apps.fb_bot.sender import *


class RegisterRoom(APIView):

    def post(self, request):
        tenant_id = request.data.get("tenant_id")
        room_id = request.data.get("room_id")

        live_room = Room.objects.get(uuid=room_id)
        tenant_user = TenantUser.objects.get(uuid=tenant_id)
        tenant_user.live_room = live_room
        tenant_user.save()
        
        serializer = TenantUserSerializer(tenant_user)
        return Response(data=serializer.data)

class RegisterTenantUser(APIView):

    def post(self, request):
        name = request.data.get("name")
        user = TenantUser.objects.create(name=name)
        user.save()

        serializer = TenantUserSimpleSerializer(user)
        return Response(data=serializer.data)


class TenantUserViewSet(viewsets.ModelViewSet):
    queryset = TenantUser.objects.all()
    serializer_class = TenantUserSerializer
    lookup_field = 'uuid'


class ChangeRoomFeeView(APIView):

    def post(self, request):
        room = request.data.get("room")
        create_user_uuid = request.data.get("user_uuid")
        user_list = room["tenant_user"]

        create_user = TenantUser.objects.get(uuid=create_user_uuid)

        for user in user_list:
            change_user = TenantUser.objects.get(uuid=user["uuid"])
            change_user.live_room_amount = user["live_room_amount"]
            change_user.save()

        result_room = Room.objects.get(uuid=room["uuid"])

        serializer = RoomDetailSerializer(result_room)

        send_change_room_fee_result(create_user, result_room)

        return Response(data=serializer.data)


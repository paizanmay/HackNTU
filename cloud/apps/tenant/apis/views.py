# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response

from apps.tenant.models import TenantUser
from apps.tenant.apis.serializers import TenantUserSerializer
from apps.landlord.models import Room


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
        fb_id = request.data.get("fb_id")
        user = TenantUser.objects.create()
        user.fb_id = fb_id
        user.save()

        serializer = TenantUserSerializer(tenant_user)
        return Response(data=serializer.data)

# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from apps.tenant.models import TenantUser
from apps.tenant.apis.serializers import TenantUserSerializer, TenantUserSimpleSerializer
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
        name = request.data.get("name")
        user = TenantUser.objects.create(name=name)
        user.save()

        serializer = TenantUserSimpleSerializer(user)
        return Response(data=serializer.data)


class TenantUserViewSet(viewsets.ModelViewSet):
    queryset = TenantUser.objects.all()
    serializer_class = TenantUserSerializer
    lookup_field = 'uuid'


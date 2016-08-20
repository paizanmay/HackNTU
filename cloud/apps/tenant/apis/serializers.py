# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from rest_framework import serializers

from apps.tenant.models import TenantUser
from apps.landlord.apis.serializers import RoomSerializer


class TenantUserSerializer(serializers.ModelSerializer):
    live_room = RoomSerializer()
    
    class Meta:
        model = TenantUser
        fields = ("uuid", "live_room", )


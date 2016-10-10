# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from rest_framework import serializers

from apps.tenant.models import TenantUser
from apps.landlord.models import Room


class RoomSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Room
        fields = ("uuid", "rental", "name", "address", )


class TenantUserSerializer(serializers.ModelSerializer):
    live_room = RoomSerializer()
    
    class Meta:
        model = TenantUser
        fields = ("uuid", "name", "live_room", "cust_id", "bank_code", "bank_account", "live_room_amount")

class TenantUserSimpleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TenantUser
        fields = ("uuid", "name", )


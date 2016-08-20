# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from rest_framework import serializers

from apps.landlord.models import Room
from apps.tenant.models import TenantUser
from apps.tenant.apis.serializers import TenantUserSimpleSerializer


class RoomSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Room
        fields = ("uuid", "rental", "name", "address", )


class RoomDetailSerializer(serializers.ModelSerializer):
    tenant_user = TenantUserSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ("uuid", "rental", "name", "address", "tenant_user", "notification_date", "deadline_date", )

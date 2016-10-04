# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from rest_framework import serializers

from apps.landlord.models import Room, LandlordUser
from apps.tenant.models import TenantUser
from apps.tenant.apis.serializers import TenantUserSimpleSerializer, TenantUserSerializer


class LandlordUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = LandlordUser
        fields = ("uuid", "name", "bank_code", "bank_account", )


class RoomSerializer(serializers.ModelSerializer):
    landlord_user = serializers.SlugRelatedField(slug_field="uuid", queryset=LandlordUser.objects.all())

    class Meta:
        model = Room
        fields = ("uuid", "rental", "name", "address", "landlord_user", )


class RoomDetailSerializer(serializers.ModelSerializer):
    tenant_user = TenantUserSerializer(many=True, read_only=True)
    landlord_user = LandlordUserSerializer()

    class Meta:
        model = Room
        fields = ("uuid", "rental", "name", "address", "tenant_user", "notification_date", "deadline_date", "landlord_user", )

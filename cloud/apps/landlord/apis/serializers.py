# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from rest_framework import serializers

from apps.landlord.models import *
from apps.tenant.models import TenantUser
from apps.tenant.apis.serializers import TenantUserSimpleSerializer, TenantUserSerializer


class LandlordUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = LandlordUser
        fields = ("uuid", "name", "bank_code", "bank_account", )


class RoomSerializer(serializers.ModelSerializer):
    landlord_user = serializers.SlugRelatedField(slug_field="uuid", queryset=LandlordUser.objects.all())
    is_paid = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Room
        fields = ("uuid", "rental", "name", "address", "landlord_user", "is_paid")

    def get_is_paid(self, obj):
        order_paid_list = [order.is_paid for order in obj.room_order.all()]
        return all(order_paid_list) and len(order_paid_list) > 0


class RoomDetailSerializer(serializers.ModelSerializer):
    tenant_user = TenantUserSerializer(many=True, read_only=True)
    landlord_user = LandlordUserSerializer(read_only=True)
    is_paid = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Room
        fields = ("uuid", "rental", "name", "address", "tenant_user", "notification_date", "deadline_date", "landlord_user", "is_paid")

    def get_is_paid(self, obj):
        order_paid_list = [order.is_paid for order in obj.room_order.all()]
        return all(order_paid_list) and len(order_paid_list) > 0


class RoomOrderSerializer(serializers.ModelSerializer):
    is_paid = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RoomOrder
        fields = ("uuid", "name", "order_type", "amount", "deadline", "paid_bank_code", "paid_bank_account", "is_paid")

    def get_is_paid(self, obj):
        return obj.is_paid






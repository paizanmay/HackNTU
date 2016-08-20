# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from rest_framework import serializers

from apps.landlord.models import Room


class RoomSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Room
        fields = ("uuid", "rental", "name", "address", )

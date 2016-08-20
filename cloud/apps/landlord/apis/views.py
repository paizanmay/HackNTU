# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response

from apps.landlord.apis.serializers import RoomSerializer, RoomDetailSerializer
from apps.landlord.models import Room


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

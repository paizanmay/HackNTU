# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register(r'tenant_user', TenantUserViewSet)

urlpatterns = [
    # url(r'^test/$', test.as_view()),
    url(r'^', include(router.urls)),
    url(r'^register_room/', RegisterRoom.as_view()),
    url(r'^register_user', RegisterTenantUser.as_view()),
    url(r'^change_room_fee', ChangeRoomFeeView.as_view()),
]

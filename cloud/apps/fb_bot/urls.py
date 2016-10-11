# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
# router.register(r'room', RoomViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^webhook', BotWebhook.as_view()),
    url(r'^authorize/(?P<sender_id>[-\w]+)', login_user),
    url(r'^reset', reset_view),
]

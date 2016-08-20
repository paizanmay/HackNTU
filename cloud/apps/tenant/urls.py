# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf.urls import url, include

from .template_views import register_room

urlpatterns = [
    url(r'^api/', include("apps.tenant.apis.urls", namespace="tenant_api")),
    url(r'^register_room/', register_room, name="register_room_page")
]

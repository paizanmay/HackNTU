# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf.urls import url, include

from apps.landlord.template_views import manage_room, login_user

urlpatterns = [
    url(r'^api/', include("apps.landlord.apis.urls", namespace="landlord_api")),
    url(r'^manage_room/', manage_room, name="manage_room_page"),
    url(r'^login_user/', login_user, name="login_user_page")
]

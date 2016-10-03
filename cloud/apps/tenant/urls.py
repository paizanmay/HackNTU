# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf.urls import url, include

from .template_views import *

urlpatterns = [
    url(r'^api/', include("apps.tenant.apis.urls", namespace="tenant_api")),
    url(r'^register_room/', register_room, name="register_room_page"),
    url(r'^register_user', register_user, name="register_user_page"),
    url(r'^login_user/', login_user, name="login_user_page"),
    url(r'^tenant_pay_order_page/(?P<order_part_uuid>[-\w]+)$', tenant_pay_order_page, name="tenant_pay_order_page"),
    url(r'^tenant_pay_order_success/$', tenant_pay_order_success, name="tenant_pay_order_success"),
    url(r'^create_order_page/$', create_order_page, name="create_order_page"),
    url(r'^setting_account_page$', setting_account_page, name="setting_account_page"),
]

# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^tenant/', include("apps.tenant.urls", namespace="tenant")),
    url(r'^landlord/', include("apps.landlord.urls", namespace="landlord")),
    url(r'^', include("apps.fb_bot.urls", namespace="fb_bot")),
]

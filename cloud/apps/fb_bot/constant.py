# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf import settings

from apps.landlord.models import *

SERVER_URL = settings.SERVER_URL

class OrderImage(object):
    base = SERVER_URL + "/static/imgs/"
    logo = base + "Artboard.jpg"
    room = base + "rent_order.jpg"
    water = base + "water.jpg"
    electric = base + "electric.jpg"
    internet = base + "internet.jpg"
    other = base + "rent_order.jpg"

    @classmethod
    def get_img_url(cls, order):
        order_model = getattr(order, "room_order", order)
        return getattr(cls, order_model.get_order_type_display())

# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.shortcuts import render_to_response

def register_room(request):
    return render_to_response("tenant/register_room.html")

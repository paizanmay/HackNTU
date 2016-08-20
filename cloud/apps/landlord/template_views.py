# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

from apps.tenant.models import TenantUser
from apps.landlord.models import LandlordUser, Room


class login_require(object):

    def __init__(self, func):
        self.func = func

    def __call__(self, request, *args, **kwargs):
        user_uuid = request.session['user_id']
        user = LandlordUser.objects.get(uuid=user_uuid)
        request.user = user
        return self.func(request, *args, **kwargs)

@login_require
def manage_room(request):
    return_data = {
        "host": request.META['HTTP_HOST']
    }
    print('testestse')
    return render_to_response("landlord/manage_room.html", return_data)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password, request=request)
        if user is not None:
            user = LandlordUser.objects.get(username=user)
            request.session['user_id'] = user.uuid
            return HttpResponseRedirect("/landlord/manage_room/")

    return render_to_response("landlord/login_user.html")

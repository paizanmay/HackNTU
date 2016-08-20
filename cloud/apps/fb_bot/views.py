# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf import settings
from pymessenger.bot import Bot
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.tenant.models import TenantUser
from apps.tenant.apis.serializers import TenantUserSerializer
from apps.landlord.models import Room
from .receiver import *

TOKEN = settings.PAGE_ACCESS_TOKEN
bot = Bot(TOKEN)

class BotWebhook(APIView):

    def get(self, request):
        return Response(data=request.GET.get("hub.challenge"))

    def post(self, request):
        output = request.data
        events = output['entry'][0]['messaging']
        for event in events:
            print(event)
            if event.get("message") is not None:
                sender = MessageReceiver(event)
                sender.send()
            elif event.get("postback") is not None:
                sender = PostBackReceiver(event)
                sender.send()
            elif event.get("account_linking") is not None:
                sender = AccountLinkReceiver(event)
                sender.send()

        return Response(data="success")

class RegisterUser(APIView):

    def get(self, request):
        account_linking_token = request.GET.get("account_linking_token")
        redirect_uri = request.GET.get("redirect_uri")

        return_data = {
            "accountLinkingToken": account_linking_token,
            "redirectURI": redirect_uri,
            "redirectURISuccess": redirect_uri
        }

        return Response(data=return_data)


# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import json
import traceback
import logging

from django.conf import settings
from django.shortcuts import render_to_response
from pymessenger.bot import Bot
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.tenant.models import TenantUser
from apps.tenant.apis.serializers import TenantUserSerializer
from apps.landlord.models import Room
from .receiver import *

TOKEN = settings.PAGE_ACCESS_TOKEN
bot = Bot(TOKEN)
logger = logging.getLogger(__name__)
logging.basicConfig()

class BotWebhook(APIView):

    def get(self, request):
        return Response(data=int(request.GET.get("hub.challenge")))

    def post(self, request):
        try:
            output = request.data
            result = "no reuslt"
            print(json.dumps(output, indent=2))
            events = output['entry'][0]['messaging']
            for event in events:
                if event.get("message") is not None:
                    sender = MessageReceiver(event)
                elif event.get("postback") is not None:
                    sender = PostBackReceiver(event)
                elif event.get("account_linking") is not None:
                    sender = AccountLinkReceiver(event)
                    result = sender.send()

                if sender.is_auth() is False:
                    result = sender.register()
                
                if sender.has_room() is False:
                    result = sender.livein()
                else:
                    result = sender.send()
                logger.info("FB Bot result:", )
        except Exception as e:
            logger.error(e)
            traceback.print_exc()

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

def login_user(request, sender_id):
    account_linking_token = request.GET.get("account_linking_token")
    redirect_uri = request.GET.get("redirect_uri")
    return render_to_response("tenant/login.html", dict(redirect_uri=redirect_uri))



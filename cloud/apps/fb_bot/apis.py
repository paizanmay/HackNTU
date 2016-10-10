# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import locale

import requests

BASE_URL = "http://52.69.27.105:8080/hackathon"

class CtbcAPI(object):

    def __init__(self, user):
        self.user = user

        login_data = {
            "CustID": user.cust_id,
            "UserID": user.cust_id,
            "PIN": user.cust_id[-4:],
            "Token": "123456789"
        }

        login_url = BASE_URL + "/login"
        login_result = requests.post(login_url, json=login_data)
        self.token = login_result.json()["Token"]

    def login(self, data):
        data.update({"Token": self.token})
        return data

    def get_account_amount(self):
        data = self.login({
            "CustID": self.user.cust_id,
        })
        amount_url = BASE_URL + "/SavingAcctInq"
        amount_req = requests.post(amount_url, json=data)
        result = amount_req.json()["SavingAcctInq"][0]["Balance"]
        locale.setlocale(locale.LC_ALL, '')
        amount = locale.currency(int(result), grouping=True)
        return amount

    def transfer(self, to_user, amount, memo=""):
        data = self.login({
            "CustID": self.user.cust_id,
            "PayerBankNO": self.user.bank_code,
            "PayerAcctNO": self.user.bank_account,
            "PayeeBankNO": to_user.bank_code,
            "PayeeAcctNO": to_user.bank_account,
            "TranAmt": str(amount),
            "Memo": memo
        })

        transfer_url = BASE_URL + "/Transfer"
        transfer_req = requests.post(transfer_url, json=data)
        result = transfer_req.json()
        print(result)
        return result






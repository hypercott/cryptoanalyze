#!/usr/bin/env python3

# make sure you provide your
# coinbase api key and api secret in credentials.py
from credentials import *

from coinbase.wallet.client import Client
import time
from datetime import datetime

currency_code = 'USD'
client = Client(api_key,api_secret)

# enter entry value and coins you own
base_data = {}
base_data['BTC'] = 100.0/1.0
base_data['LTC'] = 100.0/1.0
base_data['ETH'] = 100.0/1.0
stop_loss_factor = 0.8


def get_status(client):

    accounts = client.get_accounts()
    print("-"*79)
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for account in accounts.data:
        balance = account.balance
        if account.currency != 'USD':
            cpairs = balance.currency+'-USD'
            pricedata = client.get_spot_price(currency_pair = cpairs)
            value = float(balance.amount) * float(pricedata.amount)
            change = ( (float(pricedata.amount) - base_data[account.currency])\
                       / float(pricedata.amount) ) * 100.0
            print("%s: %s %s %8s %8.2f %+8.2f" % (account.name, balance.amount,
                                              balance.currency,pricedata.amount,
                                              value,change))
        else:
            print("%s: %s %s" % (account.name, balance.amount, balance.currency))

while True:
    get_status(client)
    time.sleep(120)

#!/usr/bin/env python3

from credentials import *

from coinbase.wallet.client import Client
import time
from datetime import datetime

currency_code = 'USD'
client = Client(api_key,api_secret)

# enter entry value and coins you own
base_data = {}
base_data['BTC'] = 
base_data['LTC'] = 
base_data['ETH'] = 
stop_loss_factor = 0.8


def get_status(client):

    accounts = client.get_accounts()
    print("-"*79)
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for account in accounts.data:
        balance = account.balance
        if account.currency != 'USD':
            cpairs = balance.currency+'-USD'
            try:
                pricedata = client.get_spot_price(currency_pair = cpairs)
            except:
                print("Ups!")
                return 1
            value = float(balance.amount) * float(pricedata.amount)
            change = ( (float(pricedata.amount) - base_data[account.currency])\
                       / float(pricedata.amount) ) * 100.0
            print("%s: %s %s %8s %8.2f %+8.2f" % (account.name, balance.amount,
                                              balance.currency,pricedata.amount,
                                              value,change))
        else:
            print("%s: %s %s" % (account.name, balance.amount, balance.currency))
    return 0

            
while True:
    retval = get_status(client)
    if retval == 0:
        time.sleep(120)
    else:
        time.sleep(20)
    

#!/usr/bin/env python3
import sys
import sqlite3
import datetime
import time

#########################################
# coinbase API

from credentials import *
from coinbase.wallet.client import Client
client = Client(api_key,api_secret)


###############################################################################

accounts = client.get_accounts()
payment_methods = client.get_payment_methods()

###############################################################################
# get current balance in BTC
balance = 0.0
accid = -1
for acc in accounts.data:
    if('BTC' in acc.name):
        bal = acc.balance
        balance = float(bal.amount)
        accid = acc.id
        
###############################################################################
# get payment ID
method = "USD Wallet"
payid = -1

for pm in payment_methods.data:
    if pm.name == method:
        payid = pm.id
###############################################################################
sell_price = client.get_sell_price(currency_pair='BTC-USD')
print(sell_price.amount)

sp = float(sell_price.amount)
sell_value = 15.0
sell_amount = sell_value / sp
print(balance,sell_amount)

samount = "%f" % (sell_amount)

print(accid)

acc = client.get_account(accid)
txs = client.get_transactions(accid)

print(txs.data[0])


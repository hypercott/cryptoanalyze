#!/usr/bin/env python3
import sys
import sqlite3
import datetime
import time
import pytz
import mycoin_get_average as mga
import numpy as np

def get_time():
    itime = int(datetime.datetime.now(tz=pytz.utc).timestamp())
    return itime

#########################################
# coinbase API

from credentials import *
from coinbase.wallet.client import Client
client = Client(api_key,api_secret)

# get payment ID
method = "USD Wallet"
payid = "-1"

payment_methods = client.get_payment_methods()
for pm in payment_methods.data:
    if pm.name == method:
        payid = pm.id

#########################################
# sqlite3

sqlite_file = 'my_coin_db.sqlite'

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
#########################################
# trading definitions

coins = ['BTC','LTC','ETH']
curr = 'USD'

stoploss_frac0 = 0.7
stoploss_frac  = 0.7

#sell_thr = 0.1
#sell_keep = 0.04


sell_thr = 0.15
sell_keep = 0.05


########################################
class crypto:
    def __init__(self,name,c):
        self.name = name
        cstring = "SELECT USDbase FROM '%s' WHERE ID=1" % \
                  (self.name)
        c.execute(cstring)
        res = c.fetchone()
        self.costbasis0 = res[0]
        # get last entry
        cstring = "SELECT MAX(ID) from '%s'" % \
                  (self.name)
        c.execute(cstring)
        lastid = c.fetchone()[0]
        # get data 
        cstring = "SELECT TimeStamp,Balance,USDbase FROM '%s' WHERE ID=%d" % \
                  (self.name,lastid)
        c.execute(cstring)
        res = c.fetchone()
        self.costbasis = res[2]
        self.lastupdate = res[0]
        self.balance = res[1]
        # ask coinbase about the account ID
        accounts = client.get_accounts()
        accid = "-1"
        for acc in accounts.data:
            if(self.name in acc.name):
                self.accid = acc.id

########################################

def sell_all(coin):
    print("Sell all of %s!!!" % coin.name)
    coins_to_sell = coin.balance
    # get account for sell
    acc = client.get_account(coin.accid)
    coins_to_sell = min(np.float64(acc.balance.amount),coins_to_sell)
    samount = "%g" % (coins_to_sell)
    print(coins_to_sell,samount,acc.balance.amount)
    #sell = acc.sell(amount=samount,
    #                currency=coin.name,
    #                payment_method=payid)

    change = -coins_to_sell
    istime = get_time()
    cstring = "INSERT INTO %s ('TimeStamp','Change','Balance','USDbase') VALUES (%d,%.14f,%.14f,%f)" % \
              (coin.name,istime,change,coin.balance,coin.costbase)
    c.execute(cstring)
    conn.commit()
    
    
def watch(client,coin):
    cpairs = coin.name+'-'+curr
    try:
        pricedata = client.get_sell_price(currency_pair = cpairs)
    except:
        print("Ups!")
        return 1

    #### balance check database vs. coinbase
    acc = client.get_account(coin.accid)
    cb_balance = np.float64(acc.balance.amount)
    if (abs(coin.balance-cb_balance) > 1.0e-7):
        print("WARNING! Balance issue!!! Account: %s",coin.name)
        print("Database: %13.8g" % coin.balance)
        print("Coinbase: %13.8g" % cb_balance)
        return 1
        
    
    price = np.float64(pricedata.amount)
    #### experiment:
    #### price = coin.costbasis0 / coin.balance * 1.15
    value = coin.balance * price
    perc = (value - coin.costbasis) / coin.costbasis

    avg = mga.get_average(coin.name,3600)
    
    print("%s: %8.2f %8.2f %13.8f %8.2f %8.2f %+8.3f" % \
          (coin.name,price,avg,coin.balance,value,coin.costbasis,perc))

    if(avg > 0):
    # stop loss is first, make sure the average over the last
    # hour is also trending this way
        if value <= coin.costbasis0 * stoploss_frac0 \
           and avg <= coin.costbasis0 * (stoploss_frac0 + 0.02):
            sell_all(coin)
            return

            if value <= coin.costbasis * stoploss_frac \
               and avg <= coin.costbasis * (stoploss_frac + 0.02):
                sell_all(coin)
            return
    else:
    # this is when our call to our database fails
        if value <= coin.costbasis0 * stoploss_frac0: 
            sell_all(coin)
            return

        if value <= coin.costbasis * stoploss_frac:
            sell_all(coin)
            return
    
    if value >= coin.costbasis * (1.0 + sell_thr):
        
        value_to_sell = coin.costbasis * (sell_thr - sell_keep)
        coins_to_sell = value_to_sell / price
        print("Selling %s!" % (coin.name))
        print(value_to_sell,coins_to_sell,coin.balance)

        # update coin data
        coin.balance = coin.balance - coins_to_sell
        coin.costbase = value - value_to_sell

        if(coin.balance < 0):
            print("Something is wrong with %s" % (coin.name))
            print("Exiting!")
            sys.exit()

        # get account for sell
        acc = client.get_account(coin.accid)
        samount = "%g" % (coins_to_sell)

        # at this point, do this only for BTC
        if(coin.name == 'BTC'):
            #sell = acc.sell(amount=samount,
            #                currency=coin.name,
            #                payment_method=payid)

            # update database
            change = -coins_to_sell
            istime = get_time()
            cstring = "INSERT INTO %s ('TimeStamp','Change','Balance','USDbase') VALUES (%d,%.14f,%.14f,%f)" % \
                      (coin.name,istime,change,coin.balance,coin.costbase)
            c.execute(cstring)
            conn.commit()

        return

    
        
myBTC = crypto('BTC',c)
myLTC = crypto('LTC',c)
myETH = crypto('ETH',c)

coins = [myBTC,myLTC,myETH]


while True:
    print("-"*79)
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for coin in coins:
        watch(client,coin)
    time.sleep(120)
        
    
#cstring = "SELECT * from BTC"
#c.execute(cstring)
#res = c.fetchall()
#print(res)


conn.close()

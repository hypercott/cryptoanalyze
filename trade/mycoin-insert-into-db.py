#!/usr/bin/env python3
import sys
import sqlite3
import datetime
import time
import pytz
import numpy as np

def get_time():
    itime = int(datetime.datetime.now(tz=pytz.utc).timestamp())
    return itime

#########################################
# sqlite3

sqlite_file = 'my_coin_db.sqlite'

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
#########################################

name = "ETH"
change = +1.06285277
balance = 1.1487485+change
costbasis = 526.76 + 500.0

istime = get_time()
cstring = "INSERT INTO %s ('TimeStamp','Change','Balance','USDbase') VALUES (%d,%.14f,%.14f,%f)" % \
              (name,istime,change,balance,costbasis)
c.execute(cstring)
conn.commit()
conn.close()

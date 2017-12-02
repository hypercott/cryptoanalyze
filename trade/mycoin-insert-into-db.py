#!/usr/bin/env python3
import sys
import sqlite3
import datetime
import time
import numpy as np

def get_time():
    itime = int(datetime.datetime.utcnow().timestamp())
    return itime

#########################################
# sqlite3

sqlite_file = 'my_coin_db.sqlite'

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
#########################################

name = "ETH"
change = 
balance = +change
costbasis = 

istime = get_time()
cstring = "INSERT INTO %s ('TimeStamp','Change','Balance','USDbase') VALUES (%d,%.14f,%.14f,%f)" % \
              (name,istime,change,balance,costbasis)
c.execute(cstring)
conn.commit()
conn.close()

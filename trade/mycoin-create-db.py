#!/usr/bin/env python3

import sys
import sqlite3
import datetime

def get_time():
    itime = int(datetime.datetime.utcnow().timestamp())
    return itime

# sql stuff
sqlite_file = 'my_coin_db.sqlite'

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
#####################################

cstring = "CREATE TABLE %s ('ID' 'INTEGER' PRIMARY KEY, 'TimeStamp' 'INTEGER' NOT NULL, 'Change' 'REAL' NOT NULL, 'Balance' 'REAL' NOT NULL, 'USDbase' 'REAL' NOT NULL)" % \
          ('BTC')
c.execute(cstring)

cstring = "CREATE TABLE %s ('ID' 'INTEGER' PRIMARY KEY, 'TimeStamp' 'INTEGER' NOT NULL, 'Change' 'REAL' NOT NULL, 'Balance' 'REAL' NOT NULL, 'USDbase' 'REAL' NOT NULL)" % \
          ('ETH')
c.execute(cstring)

cstring = "CREATE TABLE %s ('ID' 'INTEGER' PRIMARY KEY, 'TimeStamp' 'INTEGER' NOT NULL, 'Change' 'REAL' NOT NULL, 'Balance' 'REAL' NOT NULL, 'USDbase' 'REAL' NOT NULL)" % \
          ('LTC')
c.execute(cstring)

conn.commit()

# insert starting balances
itime = get_time()
change = 
balance = change
usdbase = 
cstring = "INSERT INTO %s ('TimeStamp','Change','Balance','USDbase') VALUES (%d,%.14f,%.14f,%f)" % \
          ('LTC',itime,change,balance,usdbase)
c.execute(cstring)

change = 
balance = change
usdbase = 
cstring = "INSERT INTO %s ('TimeStamp','Change','Balance','USDbase') VALUES (%d,%.14f,%.14f,%f)" % \
          ('ETH',itime,change,balance,usdbase)
print(cstring)
c.execute(cstring)


change = 
balance = change
usdbase = 
cstring = "INSERT INTO %s ('TimeStamp','Change','Balance','USDbase') VALUES (%d,%.14f,%.14f,%f)" % \
          ('BTC',itime,change,balance,usdbase)
print(cstring)
c.execute(cstring)




#cstring = "SELECT * from LTC"
#c.execute(cstring)
#res = c.fetchall()
#print(res)

conn.commit()
conn.close()
          

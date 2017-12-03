#!/usr/bin/env python3

import sys
import sqlite3
import datetime
import pytz

def get_time():
    itime = int(datetime.datetime.now(tz=pytz.utc).timestamp())
    return itime

# sql stuff
sqlite_file = 'my_coin_db.sqlite'

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
#####################################

#c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY,)' \
#          .format(tn=table_name1,nf='ID', ft='INTEGER'))

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
change = 5.00397579
balance = change
usdbase = 501.40
cstring = "INSERT INTO %s ('TimeStamp','Change','Balance','USDbase') VALUES (%d,%.14f,%.14f,%f)" % \
          ('LTC',itime,change,balance,usdbase)
c.execute(cstring)

change = 1.14874849
balance = change
usdbase = 526.76
cstring = "INSERT INTO %s ('TimeStamp','Change','Balance','USDbase') VALUES (%d,%.14f,%.14f,%f)" % \
          ('ETH',itime,change,balance,usdbase)
print(cstring)
c.execute(cstring)


change = 0.02688770
balance = change
usdbase = 295.61
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
          

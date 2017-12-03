#!/usr/bin/env python
import sys
import json
import urllib.request
import numpy as np
import datetime
import pytz

def get_time():
    itime = int(datetime.datetime.now(tz=pytz.utc).timestamp())
    return itime

def mean_last(time,data,lastsecs=1000):
    mysum = 0.0;
    tsum = 0.0;
    stime = time[-1]
    i=len(time)-1
    while( i > 1 and time[i] > stime-lastsecs):
        dt = time[i] - time[i-1]
        mysum += dt * data[i]
        tsum += dt
        i -= 1
    return (mysum/tsum)

    
def get_average(coinname,lastsecs):

    if lastsecs > 48*3600:
        raise ValueError("Can't use lastsecs more than 48 hours")
    
    data = {'currency_pair': '',
            'startdate':'',
            'enddate':''
        }

    # how much data to get
    ctime = get_time()
    stime = ctime - lastsecs*2  
    etime = ctime - 60

    data['startdate'] = repr(stime)
    data['enddate'] = repr(etime)
    data['currency_pair'] = coinname+'USD'

    req = urllib.request.Request('YourURL')
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(data)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))

    try:
        response = urllib.request.urlopen(req, jsondataasbytes)
    except:
        return -1
        
    jsondata=json.loads(response.read().decode('utf8'))

    myBTC = np.zeros(len(jsondata))
    time = np.zeros(len(jsondata),dtype=np.int)


    for i in range(len(jsondata)):
        myBTC[i] = jsondata[i]["Value"]
        time[i] = jsondata[i]["TimeStamp"]

        
    time = time - time[-1]

    return mean_last(time,myBTC,lastsecs)

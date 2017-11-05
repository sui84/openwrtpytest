#!/mnt/sda1/opkg/usr/bin/python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import threadpool
from threading import Thread
import timehelper
import traceback
import itertools

'''

'''
class ThreadHelper(object):
    def __init__(self):
        self.threadnum = 10

    #多线程
    def WorkWithMultipleThreads(self,func,data):
        pool = threadpool.ThreadPool(self.threadnum)
        reqs = threadpool.makeRequests(func, data)
        [pool.putRequest(req) for req in reqs]
        pool.wait()


    #多进程
    #@timehelper.elapsedtimedeco(True)
    def MultiExecute(self,func,args):
        try:
            print self.threadnum
            from multiprocessing import Pool
            pool = Pool(processes = self.threadnum)
            #PicklingError: Can't pickle <type 'instancemethod'>: attribute lookup __builtin__.instancemethod failed
            pool.map(func,args)
            #pool.apply_async(func,args)
            #pool.map(func, itertools.izip(arg1, itertools.repeat(arg2)))
            pool.close()
            pool.join()
        except Exception,e:
            print  'Error:',e.message,'\n',traceback.format_exc()

    #多线程
     #@timehelper.elapsedtimedeco(True)
    def MultiThreadExecute(self,func,args):
        try:
            print self.threadnum
            from multiprocessing.dummy import Pool
            pool = Pool(processes = self.threadnum)
            pool.map(func,args)
            pool.close()
            pool.join()
        except Exception,e:
            print  'Error:',e.message,'\n',traceback.format_exc()

    #协程
    def MultiGEventExecute(self,func,args):
         from gevent.pool import Pool
         pool = Pool(self.threadnum)
         return pool.map(func,args)

import time, functools

import requests, trip

def timeit(fn):
    start_time = time.time()
    fn()
    return time.time() - start_time

url = 'http://httpbin.org/get'
times = 10 # 100 changed for inland network delay

def fetch():
    r = [requests.get(url) for i in range(times)]
    return r

@trip.coroutine
def async_fetch():
    r = yield [trip.get(url) for i in range(times)]
    raise trip.Return(r)

print('Non-trip cost: %ss' % timeit(fetch))
print('Trip cost: %ss' % timeit(functools.partial(trip.run, async_fetch)))

# Result:
# Non-trip cost: 17.90799999237s
# Trip cost: 0.172300004959s

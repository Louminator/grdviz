# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 17:25:50 2013

@author: rossi
"""

from multiprocessing.connection import Client

from multiprocessing import Process,Pipe

from scipy import *

import pickle

#import thread
#import threading

def waiting():
    print 'waiting...'
    conn = None

def TryToConnect(child):
    address = ('jeremyfisher.math.udel.edu', 6000)
    #address = ('nutkin', 6000)
    conn = Client(address, authkey='secret password')
#    conn.send('hi')
    n = 2
    conn.send(pickle.dumps(n,pickle.HIGHEST_PROTOCOL))
    vdata = pickle.loads(conn.recv())
    conn.send('close')
    print len(vdata)
    # can also send arbitrary objects:
    # conn.send(['a', 2.5, None, int, sum])
    conn.close()
    child.send('All done')

#timer = threading.Timer(10.0, waiting)
#timer = threading.Timer(10.0,thread.interrupt_main)
parent_conn,child_conn = Pipe()
proc = Process(target=TryToConnect,args=(child_conn,))
proc.start()

waitingcount = 0
while (not parent_conn.poll()):
    waitingcount += 1
parent_conn.recv()
print "Success"
print waitingcount

#timer.start()
#ConnectSuccess = False



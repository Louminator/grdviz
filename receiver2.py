# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 17:25:24 2013

@author: rossi
"""

from multiprocessing.connection import Listener
from array import array

import thread
import threading

def waiting():
    print 'waiting...'

address = ('jeremyfisher.math.udel.edu', 6000)     # family is deduced to be 'AF_INET'
listener = Listener(address, authkey='secret password')
timer = threading.Timer(10.0, waiting)
try:
    timer.start()
    conn = listener.accept()
except:
    pass
timer.cancel()

print 'connection accepted from', listener.last_accepted
while True:
    
    print conn.poll()
    if conn.poll(1):
        msg = conn.recv()
        print msg
        # do something with msg
        if msg == 'close':
            conn.close()
            break
    else:
        print "Waiting for something to happen."
listener.close()

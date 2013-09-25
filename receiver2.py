# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 17:25:24 2013

@author: rossi
"""

from multiprocessing.connection import Listener
from array import array

listener = Listener(address, authkey='secret password')

while True:
    conn = listener.accept()
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

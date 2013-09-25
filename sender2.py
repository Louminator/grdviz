# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 17:25:50 2013

@author: rossi
"""

from multiprocessing.connection import Client
from array import array

import thread
import threading

def waiting():
    print 'waiting...'
    conn = None

timer = threading.Timer(10.0, waiting)
#timer = threading.Timer(10.0,thread.interrupt_main)
timer.start()


#address = ('jeremyfisher.math.udel.edu', 6000)
address = ('nutkin', 6000)
conn = Client(address, authkey='secret password')
conn.send('hi')
conn.send('close')
# can also send arbitrary objects:
# conn.send(['a', 2.5, None, int, sum])
conn.close()

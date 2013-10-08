# -*- coding: utf-8 -*-
"""
Created on November 2013

@author: Lou Rossi
"""

from multiprocessing.connection import Listener
from array import array
import pickle
from scipy import *
from string import split,atof,atoi

address = ('jeremyfisher.math.udel.edu', 6000)
listener = Listener(address, authkey='secret password')

#name = '/home/rossi/Research/Oseen-explorations/lamb-dipole-perturb-B/lamb-perturb-B'
#vtxname = name+'{0:04d}'.format(n)+'.vtx'
#try:
#    f = open(vtxname,'r')
#    txt = f.read()
#    f.close()
#    vs = split(txt)
#    vdata = map(atof,vs)
#    vdata = reshape(vdata,(len(vdata)/6,6))
#    num_vorts = len(vdata)
#except IOError:
#    print "No vtx file found."
#    self.GridStatus = -1

while True:
    conn = listener.accept()
    print 'connection accepted from', listener.last_accepted
    while True:
        print conn.poll()
        if conn.poll(1):
            msg = conn.recv()
            # do something with msg
            if msg == 'close':
                conn.close()
                break
            else:
                n = pickle.loads(msg)
                name = '/home/rossi/Research/Oseen-explorations/lamb-dipole-perturb-B/lamb-perturb-B'
                vtxname = name+'{0:04d}'.format(n)+'.vtx'
                try:
                    f = open(vtxname,'r')
                    txt = f.read()
                    f.close()
                    vs = split(txt)
                    vdata = map(atof,vs)
                    vdata = reshape(vdata,(len(vdata)/6,6))
                    num_vorts = len(vdata)
                    conn.send(pickle.dumps(vdata,pickle.HIGHEST_PROTOCOL))
                except IOError:
                    print "No vtx file found."
                    self.GridStatus = -1
        else:
            print "Waiting for something to happen."

listener.close()

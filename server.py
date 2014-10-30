#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Server for BlobFlow Explorer

Created on November 2013

@author: Louis Rossi

"""

from multiprocessing.connection import Listener
from array import array
import pickle
from scipy import *
from string import split,atof,atoi

import os.path

import sys, getopt

#os.path.isfile(file_path)


try:
    opts, args = getopt.getopt(sys.argv[1:],"h:p:",["help","host=","port="])
except getopt.GetoptError:
    print 'server.py -h <host> -p <port>'
    sys.exit(2)
    
for opt,arg in opts:
    if opt == "--help":
        print 'server.py -h <host> -p <port>'
        sys.exit()
    if opt in ("-h","--host"):
        host = arg
    if opt in ("-p","--port"):
        port = atoi(arg)

try:
    address = (host,port)
except:
    print "No host specified. Trying localhost."
    host = 'localhost'
    port = 6000
    address = ('localhost', 6000)

#address = ('jeremyfisher.math.udel.edu', 6000)
listener = Listener(address, authkey='secret password',backlog=500)

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

print ""
print "+-----------------------------------------+"
print "+ BlobFlow vorticity visualization server +"
print "+ Louis F. Rossi                          +"
print "+ Mathematical Sciences                   +"
print "+ University of Delaware                  +"
print "+                                         +"
print "+ November 2013                           +"
print "+-----------------------------------------+"
print ""

while True:
    conn = listener.accept()
    print 'connection accepted from', listener.last_accepted
    while True:
        if conn.poll(1):
            msg = conn.recv()
            # do something with msg
            if msg == 'close':
                conn.close()
                break
            elif msg == 'inv':
                upperlim = 0
                name = '/home/rossi/Research/Oseen-explorations/lamb-dipole-perturb-B/lamb-perturb-B'
                vtxname = name+'{0:04d}'.format(upperlim)+'.vtx'
                while os.path.isfile(vtxname):
                    upperlim += 1
                    vtxname = name+'{0:04d}'.format(upperlim)+'.vtx'
                    if not os.path.isfile(vtxname):
                        conn.send(pickle.dumps(upperlim,pickle.HIGHEST_PROTOCOL))
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
                    print 'Sending frame {0:d} with {1:d} vortices.'.format(n,len(vdata))
                except IOError:
                    print "No vtx file found."
                    vdata = []
                    conn.send(pickle.dumps(vdata,pickle.HIGHEST_PROTOCOL))
        else:
            print "Waiting for something to happen."

listener.close()

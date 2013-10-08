# -*- coding: utf-8 -*-
"""
Class definition for vorticity data.

Created on Fri Aug  2 20:46:35 2013

@author: rossi
"""

from scipy import *
from string import split,atof
#import matplotlib.pylab as plt
from PyQt4 import QtCore, QtGui

from multiprocessing import Process,Pipe
from multiprocessing.connection import Client

# Read in from the file.

n = 1

class Vorticity_Frame():
    
    def __init__(self,n):
        
        self.FrameNumber = n

        self.x0 = -2.
        self.y0 = -2.

        self.x1 = 2.
        self.y1 = 2.
        
        # GridStatus: 0=no grid, 1=working on grid, 2=grid created
        # GridStatus: -1 = no data at all.
        self.GridStatus = 0

        self.timer = QtCore.QTimer()
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.MeshReady)
        
        name = '/home/rossi/Research/Oseen-explorations/lamb-dipole-perturb-B/lamb-perturb-B'
        vtxname = name+'{0:04d}'.format(n)+'.vtx'
        try:
            f = open(vtxname,'r')
            txt = f.read()
            f.close()
            vs = split(txt)
            vdata = map(atof,vs)
            self.vdata = reshape(vdata,(len(vdata)/6,6))
            self.num_vorts = len(vdata)
        except IOError:
            print "No vtx file found."
            self.GridStatus = -1

# mesh it.

    def mesh(self,nmesh):

#        nmesh = 200

        x = r_[self.x0:self.x1:nmesh*1j]
        y = r_[self.y0:self.y1:nmesh*1j]

        [self.xm,self.ym] = meshgrid(x,y)

        xtmp = self.xm.reshape(size(self.xm),)
        ytmp = self.ym.reshape(size(self.ym),)

        w = zeros(size(self.xm))

        for k in range(len(self.vdata)):
            dx = xtmp-self.vdata[k,0]
            dy = ytmp-self.vdata[k,1]
            c = cos(self.vdata[k,5])
            s = sin(self.vdata[k,5])
            r2 = dx**2 + dy**2
            idx = (r2/self.vdata[k,3]>1.0e-10)
            
            tmp = -(dx[idx]**2/(c**2/self.vdata[k,4] + s**2/self.vdata[k,4])+ \
            dy[idx]**2/(s**2/self.vdata[k,4] + c**2/self.vdata[k,4]) + \
            2.*dx[idx]*dy[idx]*c*s*(1./self.vdata[k,4]+self.vdata[k,4]))/4./self.vdata[k,3]        
            w[idx] += self.vdata[k,2]*exp(tmp)/2./self.vdata[k,3]
    
        print 'done'
        self.wm = w.reshape((len(x),len(y)))

    def meshthread(self,nmesh,conn):

        x = r_[self.x0:self.x1:nmesh*1j]
        y = r_[self.y0:self.y1:nmesh*1j]

        [xm,ym] = meshgrid(x,y)

        xtmp = xm.reshape(size(xm),)
        ytmp = ym.reshape(size(ym),)

        w = zeros(size(xm))

        for k in range(len(self.vdata)):
            dx = xtmp-self.vdata[k,0]
            dy = ytmp-self.vdata[k,1]
            c = cos(self.vdata[k,5])
            s = sin(self.vdata[k,5])
            r2 = dx**2 + dy**2
            idx = (r2/self.vdata[k,3]>1.0e-10)
            
            tmp = -(dx[idx]**2/(c**2/self.vdata[k,4] + s**2/self.vdata[k,4])+ \
            dy[idx]**2/(s**2/self.vdata[k,4] + c**2/self.vdata[k,4]) + \
            2.*dx[idx]*dy[idx]*c*s*(1./self.vdata[k,4]+self.vdata[k,4]))/4./self.vdata[k,3]        
            w[idx] += self.vdata[k,2]*exp(tmp)/2./self.vdata[k,3]
    
        wm = w.reshape((len(x),len(y)))
        conn.send((xm,ym,wm))

    def SpawnMesh(self,nmesh,AlertFcn):
        self.parent_conn,self.child_conn = Pipe()
        self.proc = Process(target=self.meshthread,args=(nmesh,self.child_conn))
        self.proc.start()
        self.timer.start(1000)
        self.GridStatus = 1
        self.alert = AlertFcn

        
    def GrabMesh(self):
        if (self.parent_conn.poll()):
            self.xm,self.ym,self.wm = self.parent_conn.recv()
            self.GridStatus=2

    def MeshReady(self):
        if (self.GridStatus == 1):
            if (self.parent_conn.poll()):
                self.GrabMesh()
                self.timer.stop()
                self.alert(self.FrameNumber)
        return(self.GridStatus)
            
bigv = {}

parent_conn = {}
child_conn = {}
p = {}

for k in range(4):
    bigv[k] = Vorticity_Frame(k)
#    parent_conn[k],child_conn[k] = Pipe()
#    p[k] = Process(target=bigv[k].meshthread,args=(100,child_conn[k],))
#    p[k].start()

#working = True
#while (working):
#    working = False
#    for k in range(4):
#        print working
#        print (k,parent_conn[k].poll())
#        if (not parent_conn[k].poll()):
#            working = True
#    raw_input()
#print 'Everyone is done.'
#
#for k in range(4):
#    print child_conn[k].poll()
#    bigv[k].xm,bigv[k].ym,bigv[k].wm = parent_conn[k].recv()
#    print child_conn[k].poll()

#for k in range(4):
#    p[k].join()
#    print p[k].is_alive()

#bigv[0].mesh(200)

#plt.ion()
#plt.pcolormesh(bigv[0].xm,bigv[0].ym,bigv[0].wm)
#plt.show()

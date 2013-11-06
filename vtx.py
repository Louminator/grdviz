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
import pickle

# Read in from the file.

class Vorticity_Frame():
    
    def __init__(self,n,AlertFcn):
                
        self.FrameNumber = n

        self.alert = AlertFcn

        self.x0 = -2.
        self.y0 = -2.

        self.x1 = 2.
        self.y1 = 2.
        self.vdata = []
        
        # GridStatus:
        # -1 = uploading
        # 0 = data arrived, no grid
        # 1 = working on grid
        # 2 = grid created

        self.GridStatus = -1
        
        self.UploadWait = 0

        self.parent_conn,self.child_conn = Pipe()
        self.UploadProc = Process(target=self.TryToConnect,args=(self.child_conn,self.FrameNumber))
        self.UploadProc.start()
        
        self.uploadTimer  = QtCore.QTimer()
        QtCore.QObject.connect(self.uploadTimer, QtCore.SIGNAL("timeout()"), self.DataArrived)
        self.uploadTimer.start(500)

        self.meshTimer = QtCore.QTimer()
        QtCore.QObject.connect(self.meshTimer, QtCore.SIGNAL("timeout()"), self.MeshReady)

    def TryToConnect(self,child,n):
        address = ('localhost', 6000)
        address = ('jeremyfisher.math.udel.edu', 6000)
        #address = ('nutkin', 6000)
        conn = Client(address, authkey='secret password')
        conn.send(pickle.dumps(n,pickle.HIGHEST_PROTOCOL))
        vdata = pickle.loads(conn.recv())
        conn.send('close')
        conn.close()
        child.send(vdata)
            
    def DataArrived(self):
        if (self.GridStatus == -1):
            if (self.parent_conn.poll()):
                try:
                    self.vdata = self.parent_conn.recv()
                    self.UploadProc.join()
    #                self.UploadProc.terminate()
                    self.num_vorts = len(self.vdata)
                    self.uploadTimer.stop()
                    self.GridStatus = 0
                    self.alert(self.FrameNumber)
                except IOError:
                    print "Ouch!"
                    self.UploadProc.terminate()
                    self.parent_conn,self.child_conn = Pipe()
                    self.UploadProc = Process(target=self.TryToConnect,args=(self.child_conn,self.FrameNumber))
                    self.UploadProc.start()
            else:
                #print "UploadWaitCounter {0:d} {1:d}".format(self.FrameNumber,self.UploadWait)
                self.UploadWait += 1
# Probably do not need this.
#                if (self.UploadWait > 40000):
#                    # Transmission lost... Try again.
#                    print "Trying again {0:d} {1:d}".format(self.FrameNumber,self.UploadWait)
##                    self.UploadProc.join()
#                    self.UploadProc.terminate()
#                    self.UploadWait = 0
#                    self.parent_conn,self.child_conn = Pipe()
#                    self.UploadProc = Process(target=self.TryToConnect,args=(self.child_conn,self.FrameNumber))
#                    self.UploadProc.start()
                    
# mesh it.

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

    def SpawnMesh(self,nmesh):
        self.parent_conn,self.child_conn = Pipe()
        self.proc = Process(target=self.meshthread,args=(nmesh,self.child_conn))
        self.proc.start()
        self.meshTimer.start(1000)
        self.GridStatus = 1
        self.alert(self.FrameNumber)
        
    def GrabMesh(self):
        if (self.parent_conn.poll()):
            self.xm,self.ym,self.wm = self.parent_conn.recv()
            self.proc.join()
            self.proc.terminate()
            self.GridStatus=2
            self.alert(self.FrameNumber)

    def MeshReady(self):
        if (self.GridStatus == 1):
            if (self.parent_conn.poll()):
                self.GrabMesh()
                self.meshTimer.stop()
        return(self.GridStatus)
            

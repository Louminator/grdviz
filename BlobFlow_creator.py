# -*- coding: utf-8 -*-
"""
GUI for creating vorticity initial conditions for BlobFlow.

Created on Sun Mar 30 17:58:59 2014

@author: Louis Rossi
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QWidget

import sys

from initializer import Ui_BlobFlow_creator
from matplotlibwidget import *

from scipy import *
import numpy
from scipy.linalg import toeplitz,kron
import os
from string import join


class Plot_Widget(QWidget,Ui_BlobFlow_creator):
    def __init__(self, data2plot=None, parent = None):
        
        QWidget.__init__(self)
        
        super(Plot_Widget, self).__init__(parent)
        self.setupUi(self)

        self.str_start = "def f(x,y):\n    w=numpy.empty_like (x)\n"
        self.str_end = "    return(w)"

        self.xMin = self.xDomainMin.text().toDouble()[0]
        self.xMax = self.xDomainMax.text().toDouble()[0]
        self.yMin = self.yDomainMin.text().toDouble()[0]
        self.yMax = self.yDomainMax.text().toDouble()[0]
        self.nBlob = self.nMesh.text().toInt()[0]
        self.InterpPopControl = self.interpPopControl.text().toDouble()[0]
                
        self.plot(self.mplwidget.axes)        

    def plot(self,axes):
        
# Update with the latest values.        
        
        self.xMin = self.xDomainMin.text().toDouble()[0]
        self.yMin = self.yDomainMin.text().toDouble()[0]
        self.xMax = self.xDomainMax.text().toDouble()[0]
        self.yMax = self.yDomainMax.text().toDouble()[0]

        x = r_[self.xMin:self.xMax:500j]
        y = r_[self.yMin:self.yMax:500j]

        [xm,ym] = meshgrid(x,y)

        xtmp = xm.reshape(size(xm),)
        ytmp = ym.reshape(size(ym),)

        w = zeros(size(xm))
        msg = self.plainTextEdit.toPlainText()
                
        try:
            code_obj = compile(str(self.str_start+msg+'\n'+self.str_end), '<string>', 'single')
            exec code_obj
            w = f(xtmp,ytmp)       
            wm = w.reshape((len(x),len(y)))
                    
# We have to wipe and redraw the whole figure because the colorbar
# keeps sucking up space when replotting.
            self.mplwidget.figure.clf()
            axes=self.mplwidget.figure.add_subplot(111)
                    
            axes2 = axes.pcolormesh(xm,ym,wm,edgecolors='None',shading='None',rasterized=True)
    
            self.mplwidget.figure.colorbar(axes2)
            self.mplwidget.draw()
            
        except IndentationError,e:
            print "Check your indentation"
            print e
        
    def xMinChanged(self,msg):
        self.xMin = msg.toDouble()[0]
        self.mplwidget.figure.clf()
        self.mplwidget.draw()
        self.projectPreview.figure.clf()
        self.projectPreview.draw()
        
    def xMaxChanged(self,msg):
        self.xMax = msg.toDouble()[0]
        self.mplwidget.figure.clf()
        self.mplwidget.draw()
        self.projectPreview.figure.clf()
        self.projectPreview.draw()
        
    def yMinChanged(self,msg):
        self.yMin = msg.toDouble()[0]
        self.mplwidget.figure.clf()
        self.mplwidget.draw()
        self.projectPreview.figure.clf()
        self.projectPreview.draw()
        
    def yMaxChanged(self,msg):
        self.yMax = msg.toDouble()[0]
        self.mplwidget.figure.clf()
        self.mplwidget.draw()
        self.projectPreview.figure.clf()
        self.projectPreview.draw()
                        
    def nMeshChanged(self,msg):
        self.nBlob = msg.toInt()[0]
        self.projectPreview.figure.clf()
        self.projectPreview.draw()
        
    def interpPopControlChanged(self,msg):
        self.InterpPopControl = msg.toDouble()[0]
        self.projectPreview.figure.clf()
        self.projectPreview.draw()
        
    def plotFunction(self):            
        self.plot(self.mplwidget.axes)
        
    def saveFunction(self):
        fname = QtGui.QFileDialog.getOpenFileName(self,'Open file',os.getcwd())
        
        if (fname[-4:] != ".fun"):
            fname = fname+".fun"
        funFile = open(fname,"w")
        funFile.write(self.plainTextEdit.toPlainText())
        funFile.close()
        
    def loadFunction(self):
        fname = QtGui.QFileDialog.getOpenFileName(self,'Open file',os.getcwd())
        
        funFile = open(fname,"r")
        str=funFile.readlines()
        self.plainTextEdit.setPlainText(QtCore.QString(''.join(str)))
        funFile.close()
        self.mplwidget.figure.clf()
        self.mplwidget.draw()
        self.projectPreview.figure.clf()
        self.projectPreview.draw()
        
    def saveDataFile(self):
        fname = QtGui.QFileDialog.getOpenFileName(self,'Open file',os.getcwd())

        if (fname[-4:] != ".grd"):
            fname = fname+".grd"
        
        meshFile = open(fname,"w")
        x = r_[self.xMin:self.xMax:self.nBlob*1j]
        y = r_[self.yMin:self.yMax:self.nBlob*1j]
        [xm,ym] = meshgrid(x,y)

        xtmp = xm.reshape(size(xm),)
        ytmp = ym.reshape(size(ym),)
        msg = self.plainTextEdit.toPlainText()
        
        try:
            code_obj = compile(str(self.str_start+msg+'\n'+self.str_end), '<string>', 'single')
            exec code_obj
        except Error,e:
            print "error"
            print e

#        w = zeros(size(xm))
        w = f(xtmp,ytmp)  

        for i in range(0,len(w)):
            meshFile.write("{0:12.8e}\n".format(w[i]))        
        meshFile.close()
        
        simName = fname[:-3] + "sim"
        simFile = open(simName,"w")
        simFile.write("FrameStep: \n")
        simFile.write("EndTime: \n")
        simFile.write("Viscosity: \n")
        simFile.write("GrdInit: " + fname + "\n")
        simFile.write("GrdX0: {0:12.8e}\n".format(self.xMin))
        simFile.write("GrdX1: {0:12.8e}\n".format(self.xMax))
        simFile.write("GrdY0: {0:12.8e}\n".format(self.yMin))
        simFile.write("GrdY1: {0:12.8e}\n".format(self.yMax))
        simFile.write("GrdNumPts: {0:d}\n".format(self.nBlob))
        simFile.close()

        ctlName = fname[:-3] + "ctl"
        ctlFile = open(ctlName,"w")
        ctlFile.write("TimeStep: " + "\n")
        ctlFile.write("InterpStep: " + "\n")
        ctlFile.write("InterpPopulationControl: {0:12.8e}\n".format(self.InterpPopControl))
        ctlFile.write("InterpVar: {0:12.8e}\n".format(((self.xMax-self.xMin)/(self.nBlob))**2))
        ctlFile.close()
        
    def quitGUI(self):
        self.close()
        
    def squareDomain(self):
        maxAspect = max([(self.xMax-self.xMin)/(self.yMax-self.yMin),(self.yMax-self.yMin)/(self.xMax-self.xMin)])
        deltaDim = abs((self.xMax-self.xMin) - (self.yMax - self.yMin))
        if (maxAspect-1.0 > 1.0e-10):
            if (self.xMax-self.xMin) > (self.yMax-self.yMin):
                self.yMax += deltaDim/2.
                self.yMin -= deltaDim/2.
                self.yDomainMax.setText("{0:4.4f}".format(self.yMax))
                self.yDomainMin.setText("{0:4.4f}".format(self.yMin))
            else:
                self.xMax += deltaDim/2.
                self.xMin -= deltaDim/2.
                self.xDomainMax.setText("{0:4.4f}".format(self.xMax))
                self.xDomainMin.setText("{0:4.4f}".format(self.xMin))
        self.plotFunction()
                
    def plotProject(self):
        self.squareDomain()
#        self.nBlob = self.nMesh.text().toInt()[0]
        x = r_[self.xMin:self.xMax:self.nBlob*1j]
        y = r_[self.yMin:self.yMax:self.nBlob*1j]
        
        dx = x[1]-x[0]
        dy = y[1]-y[0]
        [xm,ym] = meshgrid(x,y)

        xcoarse = xm.reshape(size(xm),)
        ycoarse = ym.reshape(size(ym),)
        msg = self.plainTextEdit.toPlainText()
        
        try:
            code_obj = compile(str(self.str_start+msg+'\n'+self.str_end), '<string>', 'single')
            exec code_obj
        except Error,e:
            print "error"
            print e

        wcoarse = f(xcoarse,ycoarse)  
        g = self.RHE(x,y,wcoarse,1.)
        
        ind = (abs(g) > self.InterpPopControl*dx*dy)
        
        g       = g[ind]
        xcoarse = xcoarse[ind]
        ycoarse = ycoarse[ind]
        
        xfine = r_[self.xMin:self.xMax:500j]
        yfine = r_[self.yMin:self.yMax:500j]

        [xm,ym] = meshgrid(xfine,yfine)

        xfinem = xm.reshape(size(xm),)
        yfinem = ym.reshape(size(ym),)

        wm = self.project(xfinem,yfinem,xcoarse,ycoarse,g,(x[1]-x[0])**2)
        wex = f(xfinem,yfinem)
        err = max(abs(wm-wex))
        self.Log.appendPlainText('Field interpolation error {1:12.4e} with {0:d} basis functions'.format(len(g),err))
        
        wm = wm.reshape(len(xfine),len(yfine))
        self.projectPreview.figure.clf()
        axes=self.projectPreview.figure.add_subplot(111)
                    
        axes2 = axes.pcolormesh(xm,ym,wm,edgecolors='None',shading='None',rasterized=True)
    
        self.projectPreview.figure.colorbar(axes2)
        axes.plot(xcoarse,ycoarse,'k.',markersize=1)
        self.projectPreview.draw()
        
    def RHE(self,x,y,w,alpha):
        
# Only works when dx = dy.
        
        n = len(x)
        m = len(y)
        dx = x[1]-x[0]
        dy = y[1]-y[0]
        g = w*dx*dy
        
        r = concatenate(([-60., 16., -1.],zeros(n-3)))/12.
        r = concatenate(([-980., 270.,-27., 2.],zeros(n-4)))/180.
        c = r
        A = toeplitz(r,c)
        B = eye(n)
        r = concatenate(([0., 16., -1.],zeros(m-3)))/12.
        r = concatenate(([0., 270.,-27., 2.],zeros(n-4)))/180.
        c = r
        C = toeplitz(r,c)
        M = kron(eye(m),A)+kron(C,B)
        
        k1    = -alpha*dot(M,g)
        wtmp1 = g + 0.5*k1
        k2    = -alpha*dot(M,wtmp1)
        wtmp2 = g + 0.5*k2
        k3    = -alpha*dot(M,wtmp2)
        wtmp3 = g + k3
        k4    = -alpha*dot(M,wtmp3)
        
        return(g + k1/6. + k2/3. + k3/3. + k4/6.)
        
    def project(self,xm,ym,x,y,g,s2):

        N = len(x)
        wm = zeros(len(xm))
        tol = 16.
        
        for j in range(0,N):
            ind = ( (((x[j]-xm)**2 + (y[j]-ym)**2))/4/s2 < tol )
            wm[ind] += g[j]/4/pi/s2*exp(-((x[j]-xm[ind])**2 + (y[j]-ym[ind])**2)/4./s2)
            
        return(wm)
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    plot = Plot_Widget()
    plot.show()

    sys.exit(app.exec_())



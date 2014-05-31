# -*- coding: utf-8 -*-
"""
Created on Sun Mar 30 17:58:59 2014

@author: rossi
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QWidget

import sys

from initializer import Ui_BlobFlow_creator
from matplotlibwidget import *

from scipy import *
import numpy
import os


class Plot_Widget(QWidget,Ui_BlobFlow_creator):
    def __init__(self, data2plot=None, parent = None):
        
        QWidget.__init__(self)
        
        super(Plot_Widget, self).__init__(parent)
        self.setupUi(self)

        self.str_start = "def f(x,y):\n    w=numpy.empty_like (x)\n"
        self.str_end = "    return(w)"
        msg = self.plainTextEdit.toPlainText()
        self.functionDef.setPlainText(self.str_start+msg+'\n'+self.str_end)

        self.xMin = self.xDomainMin.text().toDouble()[0]
        self.xMax = self.xDomainMax.text().toDouble()[0]
        self.yMin = self.yDomainMin.text().toDouble()[0]
        self.yMax = self.yDomainMax.text().toDouble()[0]
        self.nMesh = self.nMesh.text().toInt()[0]
        
        self.plot(self.mplwidget.axes)
        

    def plot(self,axes):
        
        x = r_[self.xMin:self.xMax:500j]
        y = r_[self.yMin:self.yMax:500j]

        [xm,ym] = meshgrid(x,y)

        xtmp = xm.reshape(size(xm),)
        ytmp = ym.reshape(size(ym),)

        w = zeros(size(xm))
                
        try:
            code_obj = compile(str(self.functionDef.toPlainText()), '<string>', 'single')
            exec code_obj
            w = f(xtmp,ytmp)       
            wm = w.reshape((len(x),len(y)))
                    
# We have to wipe and redraw the whole figure because the colorbar
# keeps sucking up space when replotting.
            self.mplwidget.figure.clf()
            axes=self.mplwidget.figure.add_subplot(111)
                    
            axes2 = axes.pcolormesh(xm,ym,wm,edgecolors='None',shading='None',rasterized=True)
#        self.mplwidget.figure.add_axes(axes)
    
            self.mplwidget.figure.colorbar(axes2)
            self.mplwidget.draw()
            
        except IndentationError,e:
            print "Check your indentation"
            print e

    def functionChanged(self):
        msg = self.plainTextEdit.toPlainText()
        self.functionDef.setPlainText(self.str_start+msg+'\n'+self.str_end)
        
    def xMinChanged(self):
        self.xMin = self.xDomainMin.text().toDouble()[0]
        self.plotFunction()
           
    def xMaxChanged(self):
        self.xMax = self.xDomainMax.text().toDouble()[0]
        self.plotFunction()
        
    def yMinChanged(self):
        self.yMin = self.yDomainMin.text().toDouble()[0]
        self.plotFunction()
        
    def yMaxChanged(self):
        self.yMax = self.yDomainMax.text().toDouble()[0]
        self.plotFunction()
                        
    def nMeshChanged(self):
        self.nMesh = self.nMesh.text().toInt()[0]
        self.plotFunction()
        
    def plotFunction(self):
            
        self.plot(self.mplwidget.axes)
        
    def saveFunction(self):
        fname = QtGui.QFileDialog.getOpenFileName(self,'Open file',os.getcwd())
        
        if (fname[-4:] != ".fun"):
            fname = fname+".fun"
        funFile = open(fname,"w")
        funFile.write(self.plainTextEdit.toPlainText())
        funFile.close()
        
#    def loadFunction(self):
#        fname = QtGui.QFileDialog.getOpenFileName(self,'Open file',os.getcwd())
#        
#        funFile = open(fname,"r")
#        funFile.readlines()
#        funFile.close()
        
    def saveDataFile(self):
        fname = QtGui.QFileDialog.getOpenFileName(self,'Open file',os.getcwd())

        if (fname[-4:] != ".dat"):
            fname = fname+".dat"
        
        meshFile = open(fname,"w")
        x = r_[self.xMin:self.xMax:self.nMesh*1j]
        y = r_[self.yMin:self.yMax:self.nMesh*1j]
        [xm,ym] = meshgrid(x,y)

        xtmp = xm.reshape(size(xm),)
        ytmp = ym.reshape(size(ym),)
        
        try:
            code_obj = compile(str(self.functionDef.toPlainText()), '<string>', 'single')
            exec code_obj
        except Error,e:
            print "error"
            print e

        w = zeros(size(xm))
        w = f(xtmp,ytmp)  

        for i in range(0,len(w)):
            meshFile.write("{0:12.8e}\n".format(w[i]))        
        meshFile.close()
        
        simName = fname[:-3] + "sim"
        simFile = open(simName,"w")
        simFile.write("FrameStep:" + "\n")
        simFile.write("EndTime:" + "\n")
        simFile.write("Viscosity:" + "\n")
        simFile.write("GrdInit: " + fname + "\n")
        simFile.write("GrdX0: " + "{0:12.8e}".format(self.xMin) + "\n")
        simFile.write("GrdX1: " + "{0:12.8e}".format(self.xMax) + "\n")
        simFile.write("GrdY0: " + "{0:12.8e}".format(self.yMin) + "\n")
        simFile.write("GrdY1: " + "{0:12.8e}".format(self.yMax) + "\n")
        simFile.write("GrdNumPts: " + "{0:d}".format(self.nMesh) + "\n")
        simFile.close()
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    plot = Plot_Widget()
    plot.show()

    sys.exit(app.exec_())

code_str = """
def f(x):
#    asdf
    return(x*x)
#print f(3)
#print "Hello, world"
#print "Goodbye, world"

"""
code_obj = compile(code_str, '<string>', 'single')

try:
    exec code_obj
except NameError,e:
    print "error"
    print e
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QWidget

import sys

from mpltest import Ui_BlobFlowExplorer
from matplotlibwidget import *

from scipy import *
from string import split,atof,atoi

from vtx import *
#from event import Event

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Plot_Widget(QWidget,Ui_BlobFlowExplorer):
    def __init__(self, data2plot=None, parent = None):
        self.grddata = {}
        self.MaxThreads = 4
        self.NMesh = 80
        self.FrameThreads = []
        self.FrameQueue =  []

        QWidget.__init__(self)
        
        super(Plot_Widget, self).__init__(parent)
        self.setupUi(self)
#        self.mplwidget = MatplotlibWidget(self, title='Example',
#                                          xlabel='Linear scale',
#                                          ylabel='Log scale',
#                                          hold=True, yscale='log')
#        self.mplwidget.setFocus()
#        self.setCentralWidget(self.mplwidget)

# Default domain values
        try:
            f = open('/home/rossi/Research/Oseen-explorations/expB-lowres/egrid.default','r')
            txt = f.read()
            f.close()
            nums = split(txt)
            self.num = map(atof,nums[0:4])
            self.gridn = atoi(nums[4])

            self.xMin.setValue(self.num[0])
            self.xMax.setValue(self.num[2])
            self.yMin.setValue(self.num[1])
            self.yMax.setValue(self.num[3])
            
            self.xScale = (self.num[2]-self.num[0])/(self.NMesh-1.)
            self.yScale = (self.num[3]-self.num[1])/(self.NMesh-1.)
            
            self.xMin.setSingleStep(self.xScale)
            self.xMinDial.setMinimum(0)
            self.xMinDial.setMaximum(self.NMesh-1)
            self.xMinDial.setValue(0)
            
            self.yMin.setSingleStep(self.yScale)
            self.yMinDial.setMinimum(0)
            self.yMinDial.setMaximum(self.NMesh-1)
            self.yMinDial.setValue(0)
            
            self.xMax.setSingleStep(self.xScale)
            self.xMaxDial.setMinimum(0)
            self.xMaxDial.setMaximum(self.NMesh-1)
            self.xMaxDial.setValue(self.NMesh-1)
            
            self.yMax.setSingleStep(self.yScale)
            self.yMaxDial.setMinimum(0)
            self.yMaxDial.setMaximum(self.NMesh-1)
            self.yMaxDial.setValue(self.NMesh-1)
            
        except IOError:
            print "No egrid.default file found."
        
            
        self.plot(self.mplwidget.axes)
#        QtCore.QObject.connect(self.timeDial, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.newplot)
        self.mplwidget.leaveEvent = self.mplleaveEvent
        self.mplwidget.enterEvent = self.mplenterEvent
        self.mplwidget.wheelEvent = self.mplwheelEvent
        
        self.timer = QtCore.QTimer()
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.playUpdate)
                
    def read_grd(self,n):
        name = '/home/rossi/Research/Oseen-explorations/expB-lowres/expB'
        name = '/home/rossi/Research/Oseen-explorations/lamb-dipole-perturb-A'
        grdname = name+'{0:04d}'.format(n)+'.grd'
        try:
            f = open(grdname,'r')
            txt = f.read()
            f.close()
            ws = split(txt)
            w = map(atof,ws)
            w = reshape(w,(self.gridn,self.gridn))
        except IOError:
            print "No grd file found."
        return(w)
        
    def xMinDialChanged(self,value):
        if (self.xMinDial.value()<self.xMaxDial.value()):
            self.xMin.setValue(self.num[0] + self.xMinDial.value()*self.xScale)
        else:
            self.xMinDial.setValue(self.xMaxDial.value()-1)

    def xMaxDialChanged(self,value):
        if (self.xMinDial.value()<self.xMaxDial.value()):
            self.xMax.setValue(self.num[0] + self.xMaxDial.value()*self.xScale)
        else:
            self.xMaxDial.setValue(self.xMinDial.value()+1)

    def yMinDialChanged(self,value):
        if (self.yMinDial.value()<self.yMaxDial.value()):
            self.yMin.setValue(self.num[1] + self.yMinDial.value()*self.yScale)
        else:
            self.yMinDial.setValue(self.yMaxDial.value()-1)
        
    def yMaxDialChanged(self,value):
        if (self.yMinDial.value()<self.yMaxDial.value()):
            self.yMax.setValue(self.num[1] + self.yMaxDial.value()*self.yScale)
        else:
            self.yMaxDial.setValue(self.yMinDial.value()+1)
        
    def xMinChanged(self,value):
        self.xMinDial.setValue((int) ((self.xMin.value()-self.num[0])/self.xScale + 0.5))
    def xMaxChanged(self,value):
        self.xMaxDial.setValue((int) ((self.xMax.value()-self.num[0])/self.xScale + 0.5))
        
    def yMinChanged(self,value):
        self.yMinDial.setValue((int) ((self.yMin.value()-self.num[1])/self.yScale + 0.5))
    def yMaxChanged(self,value):
        self.yMaxDial.setValue((int) ((self.yMax.value()-self.num[1])/self.yScale + 0.5))
        
    def ResetZoomx(self):
        self.xMin.setValue(self.num[0])
        self.xMax.setValue(self.num[2])
        
    def ResetZoomy(self):        
        self.yMin.setValue(self.num[1])
        self.yMax.setValue(self.num[3])
                
    def quit_gui(self):
        self.close()
        
    def play(self):
        self.timer.start(200)
            
    def pause(self):
        self.timer.stop()
        if (self.CurrentFrame.value() in self.FrameQueue):
            self.FrameQueue.remove(self.CurrentFrame.value())
            self.FrameQueue.insert(0,self.CurrentFrame.value())
            
    def playUpdate(self):
        x = self.CurrentFrame.value()
        if self.Play.isChecked():
            if (self.CurrentFrame.value()>100):
                self.CurrentFrame.setValue(99)
                self.timer.stop()
                self.Pause.setChecked(True)
            self.CurrentFrame.setValue(x+1)
            self.newplot()
        if self.Rewind.isChecked():
            if (self.CurrentFrame.value() == 0):
                self.CurrentFrame.setValue(1)
                self.timer.stop()
                self.Pause.setChecked(True)
            self.CurrentFrame.setValue(x-1)
            self.CurrentFrame.update()
            self.newplot()            

    def mplwheelEvent(self,event):
        print "Weeee"
        print event.delta()
        
    def mplenterEvent(self,event):
        print "Welcome"
        
    def mplleaveEvent(self,event):
        print "B-Bye"

    def FrameDone(self,n):
        if (n == self.CurrentFrame.value()):
            self.newplot()
        self.FrameThreads.remove(n)
        if (len(self.FrameQueue) > 0):
            self.grddata[self.FrameQueue[0]] = Vorticity_Frame(self.FrameQueue[0])
            self.FrameThreads.append(self.FrameQueue[0])
            self.grddata[self.FrameQueue[0]].SpawnMesh(self.NMesh,self.FrameDone)
            self.FrameQueue.remove(self.FrameQueue[0])

    def newplot(self):
        a=self.CurrentFrame.value()
        
        if  (not a in self.grddata):
            self.grddata[a] = Vorticity_Frame(a)
        print "Mesh ready..."
        print self.grddata[a].MeshReady()
        print len(self.grddata[a].vdata)
            
        if (self.grddata[a].MeshReady() == 0):
            if (len(self.FrameThreads) < self.MaxThreads):
                self.grddata[a] = Vorticity_Frame(a)
                self.FrameThreads.append(a)
                self.grddata[a].SpawnMesh(self.NMesh,self.FrameDone)
            else:
                if (not a in self.FrameQueue):
                    if (self.Pause.isChecked()):
                        self.FrameQueue.insert(0,a)
                    else:
                        self.FrameQueue.append(a)
                elif (self.Pause.isChecked()):
                    self.FrameQueue.remove(a)
                    self.FrameQueue.insert(0,a)
        
        if (self.grddata[a].MeshReady() == 2):
            self.grddata[a].GrabMesh()
#            if (a in self.FrameThreads):
#                self.FrameThreads.remove(a)
            self.mplwidget.axes.cla()
            self.mplwidget.axes.pcolormesh(self.grddata[a].xm,self.grddata[a].ym,self.grddata[a].wm,edgecolors='None',shading='None',rasterized=True)
            self.mplwidget.axes.set_xlim((self.xMin.value(),self.xMax.value()))
            self.mplwidget.axes.set_ylim((self.yMin.value(),self.yMax.value()))
            self.mplwidget.draw()
        else:
            self.mplwidget.axes.cla()
            self.mplwidget.axes.set_xlim((self.xMin.value(),self.xMax.value()))
            self.mplwidget.axes.set_ylim((self.yMin.value(),self.yMax.value()))
            xmid = (self.xMin.value()+self.xMax.value())/2.
            ymid = (self.yMin.value()+self.yMax.value())/2.
            if (self.grddata[a].MeshReady() == 0):
                self.mplwidget.axes.text(xmid,ymid,'Working...',fontsize=18, \
                    horizontalalignment='center',verticalalignment='center',color='red')
                self.mplwidget.draw()
            elif (self.grddata[a].MeshReady() == -1):
                self.mplwidget.axes.text(xmid,ymid,'Uploading...',fontsize=18, \
                    horizontalalignment='center',verticalalignment='center',color='red')
                self.mplwidget.draw()
 
    def plot(self, axes):
        self.newplot()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    plot = Plot_Widget()
    plot.show()

    sys.exit(app.exec_())


from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QWidget

import sys

from grd_GUI import Ui_BlobFlowExplorer
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
        self.MaxThreads = 3
        self.NMesh = 80
        self.FrameThreads = []
        self.FrameQueue =  []

        QWidget.__init__(self)
        
        super(Plot_Widget, self).__init__(parent)
        self.setupUi(self)

# Default domain values
        try:
            f = open('/home/rossi/Research/Oseen-explorations/expB-lowres/egrid.default','r')
            txt = f.read()
            f.close()
            nums = split(txt)
            self.num = map(atof,nums[0:4])
            self.gridn = atoi(nums[4])
            
            self.xViewLen = (self.num[2]-self.num[0])/2.
            self.yViewLen = (self.num[3]-self.num[1])/2.
            
            self.xCenter = (self.num[2]+self.num[0])/2.
            self.yCenter = (self.num[3]+self.num[1])/2.
                        
            self.xScale = (self.num[2]-self.num[0])/(self.NMesh-1.)
            self.yScale = (self.num[3]-self.num[1])/(self.NMesh-1.)
                     
        except IOError:
            print "No egrid.default file found."
        
            
        self.plot(self.mplwidget.axes)
#        QtCore.QObject.connect(self.timeDial, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.newplot)
        self.mplwidget.leaveEvent = self.mplleaveEvent
        self.mplwidget.enterEvent = self.mplenterEvent
        self.mplwidget.wheelEvent = self.mplwheelEvent
        self.mplwidget.mpl_connect('button_press_event',self.on_press)
        self.mplwidget.mpl_connect('button_release_event',self.on_release)
        
        self.timer = QtCore.QTimer()
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.playUpdate)
        
    def on_press(self,event):
        #print('you pressed', event.button, event.xdata, event.ydata)
        if (event.button == 1):

            self.xpress = event.xdata
            self.ypress = event.ydata
        
    def on_release(self,event):
        if (event.button == 1):
            delx = event.xdata-self.xpress
            dely = event.ydata-self.ypress
            del self.xpress 
            del self.ypress
            self.xCenter -= delx
            self.yCenter -= dely
            self.newplot()
                
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

    def VtxChangeStatus(self,n):
        if (self.grddata[n].GridStatus==0):
            if (len(self.FrameThreads) < self.MaxThreads):
                self.FrameThreads.append(n)
                self.grddata[n].SpawnMesh(self.NMesh)
            else:
                if (not n in self.FrameQueue):
                    if (self.Pause.isChecked()):
                        self.FrameQueue.insert(0,n)
                    else:
                        self.FrameQueue.append(n)
                elif (self.Pause.isChecked()):
                    self.FrameQueue.remove(n)
                    self.FrameQueue.insert(0,n)
            
        if (self.grddata[n].GridStatus==2):
            self.FrameThreads.remove(n)
            if (len(self.FrameQueue) > 0):
                self.FrameThreads.append(self.FrameQueue[0])
                self.grddata[self.FrameQueue[0]].SpawnMesh(self.NMesh)
                self.FrameQueue.remove(self.FrameQueue[0])
                
        if (n == self.CurrentFrame.value()):
            self.newplot()

    def FrameDone(self,n):
        if (n == self.CurrentFrame.value()):
            self.newplot()
        self.FrameThreads.remove(n)
        if (len(self.FrameQueue) > 0):
            self.grddata[self.FrameQueue[0]] = Vorticity_Frame(self.FrameQueue[0])
            self.FrameThreads.append(self.FrameQueue[0])
            self.grddata[self.FrameQueue[0]].SpawnMesh(self.NMesh)
            self.FrameQueue.remove(self.FrameQueue[0])

    def UploadDone(self,n):
        if (n == self.CurrentFrame.value()):
            
            self.newplot()
        self.FrameThreads.remove(n)
        if (len(self.FrameQueue) > 0):
            self.grddata[self.FrameQueue[0]] = Vorticity_Frame(self.FrameQueue[0])
            self.FrameThreads.append(self.FrameQueue[0])
            self.grddata[self.FrameQueue[0]].SpawnMesh(self.NMesh,self.FrameDone)
            self.FrameQueue.remove(self.FrameQueue[0])

    def zoomChanged(self):
        self.newplot()

    def newplot(self):
        a=self.CurrentFrame.value()
        if  (not a in self.grddata):
            self.grddata[a] = Vorticity_Frame(a,self.VtxChangeStatus)
        
        if (self.grddata[a].GridStatus == 2):
            self.mplwidget.axes.cla()
            self.mplwidget.axes.pcolormesh(self.grddata[a].xm,self.grddata[a].ym,self.grddata[a].wm,edgecolors='None',shading='None',rasterized=True)
            self.mplwidget.axes.set_xlim((self.xCenter-self.xViewLen*exp(-self.zoom.value()/10.),self.xCenter+self.xViewLen*exp(-self.zoom.value()/10.)))
            self.mplwidget.axes.set_ylim((self.yCenter-self.yViewLen*exp(-self.zoom.value()/10.),self.yCenter+self.yViewLen*exp(-self.zoom.value()/10.)))
            self.mplwidget.draw()
        else:
            self.mplwidget.axes.cla()
            self.mplwidget.axes.set_xlim((self.xCenter-self.xViewLen*exp(-self.zoom.value()/10.),self.xCenter+self.xViewLen*exp(-self.zoom.value()/10.)))
            self.mplwidget.axes.set_ylim((self.yCenter-self.yViewLen*exp(-self.zoom.value()/10.),self.yCenter+self.yViewLen*exp(-self.zoom.value()/10.)))
            if (self.grddata[a].GridStatus == 1):
                self.mplwidget.axes.text(self.xCenter,self.yCenter,'Meshing...',fontsize=18, \
                    horizontalalignment='center',verticalalignment='center',color='red')
                self.mplwidget.draw()
            elif (self.grddata[a].GridStatus == 0):
                self.mplwidget.axes.text(self.xCenter,self.yCenter,'Queued...',fontsize=18, \
                    horizontalalignment='center',verticalalignment='center',color='red')
                self.mplwidget.draw()
            elif (self.grddata[a].GridStatus == -1):
                self.mplwidget.axes.text(self.xCenter,self.yCenter,'Uploading...',fontsize=18, \
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


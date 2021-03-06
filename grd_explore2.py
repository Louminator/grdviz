#!/usr/bin/python

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QWidget

import sys, getopt

from grd_GUI import Ui_BlobFlowExplorer
from matplotlibwidget import *

from scipy import *
from string import split,atof,atoi

from vtx import *

from scipy.interpolate import RectBivariateSpline

#from event import Event

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Plot_Widget(QWidget,Ui_BlobFlowExplorer):
    def __init__(self, argv,data2plot=None, parent = None):
                
        try:
            opts, args = getopt.getopt(argv[1:],"h:p:",["help","host=","port="])
        except getopt.GetoptError:
            print 'grd_explore2.py -h <host> -p <port>'
            sys.exit(2)
            
        for opt,arg in opts:
            if opt == "--help":
                print 'grd_explore2.py -h <host> -p <port>'
                sys.exit()
            if opt in ("-h","--host"):
                self.host = arg
            if opt in ("-p","--port"):
                self.port = atoi(arg)
        
        self.grddata = {}
        self.MaxThreads = 3
        self.NMesh = 80
        self.FrameThreads = []
        self.FrameQueue =  []
 
        QWidget.__init__(self)
        super(Plot_Widget, self).__init__(parent)
        self.setupUi(self)
        

        self.domainLL = r_[-2.,-2.]
        self.domainUR = r_[2.,2.]
        
        self.xCenter = (self.domainLL[0]+self.domainUR[0])/2.
        self.yCenter = (self.domainLL[1]+self.domainUR[1])/2.
        self.xViewLen = (self.domainUR[0]-self.domainLL[0])*exp(-self.zoom.value()/10.)
        self.yViewLen = (self.domainUR[1]-self.domainLL[1])*exp(-self.zoom.value()/10.)
        
#Maybe time to dump these.
        self.xScale = self.xViewLen/(self.NMesh-1.)
        self.yScale = self.yViewLen/(self.NMesh-1.)
        
        self.pressed = False

#        QtCore.QObject.connect(self.timeDial, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.newplot)
#        self.mplwidget.leaveEvent = self.mplleaveEvent
#        self.mplwidget.enterEvent = self.mplenterEvent
        self.mplwidget.wheelEvent = self.mplwheelEvent
        self.mplwidget.mpl_connect('button_press_event',self.on_press)
        self.mplwidget.mpl_connect('button_release_event',self.on_release)
        self.mplwidget.mpl_connect('motion_notify_event', self.on_motion)
        self.timer = QtCore.QTimer()
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.playUpdate)

        self.CheckFileInventory()

        self.plot(self.mplwidget.axes)
       
    def on_motion(self,event):
        if self.pressed:
            if ( (event.xdata != None) & (event.ydata != None)):
                delx = event.xdata-self.xpress
                dely = event.ydata-self.ypress
                self.xCenter -= delx
                self.yCenter -= dely
                self.newplot()
       
    def on_press(self,event):
        if (event.button == 1):

            self.xpress = event.xdata
            self.ypress = event.ydata
            self.pressed = True
        
    def on_release(self,event):
        if (event.button == 1):
            self.pressed = False
            del self.xpress 
            del self.ypress
                
                                
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
        if self.Play.isChecked():
            if (self.CurrentFrame.value() == self.CurrentFrame.maximum()):
                self.timer.stop()
                self.Pause.setChecked(True)
            else:
                self.CurrentFrame.setValue(self.CurrentFrame.value()+1)
                self.newplot()
        if self.Rewind.isChecked():
            if (self.CurrentFrame.value() == self.CurrentFrame.minimum()):
                self.timer.stop()
                self.Pause.setChecked(True)
            else:
                self.CurrentFrame.setValue(self.CurrentFrame.value()-1)
                self.CurrentFrame.update()
            self.newplot()            

    def mplwheelEvent(self,event):
        if (event.delta()>0):
            self.zoom.setValue(self.zoom.value()+1)
        else:
            self.zoom.setValue(self.zoom.value()-1)

        
#    def mplenterEvent(self,event):
#        print "Welcome"
#        
#    def mplleaveEvent(self,event):
#        print "B-Bye"

    def CheckFileInventory(self):
        try:
            address = (self.host,self.port)
        except:
            print "No host specified. Trying localhost."
            self.host = 'localhost'
            self.port = 6000
            address = ('localhost', 6000)
#        address = ('jeremyfisher.math.udel.edu', 6000)
        #address = ('nutkin', 6000)
        conn = Client(address, authkey='secret password')
        conn.send('inv')
        self.UpperFrame = pickle.loads(conn.recv())
        conn.send('close')
        conn.close()
        print self.UpperFrame
        self.CurrentFrame.setMaximum(self.UpperFrame-1)
        self.timeDial.setMaximum(self.UpperFrame-1)
        self.horizontalScrollBar.setMaximum(self.UpperFrame-1)

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

    def zoomChanged(self):
        self.xViewLen = (self.domainUR[0]-self.domainLL[0])*exp(-self.zoom.value()/10.)
        self.yViewLen = (self.domainUR[1]-self.domainLL[1])*exp(-self.zoom.value()/10.)
        self.newplot()

    def newplot(self):
        a=self.CurrentFrame.value()
        
        if  (not a in self.grddata):
            self.grddata[a] = Vorticity_Frame(self.host,self.port,a,self.VtxChangeStatus,domainLL=self.domainLL,domainUR=self.domainUR)
        
        if (self.grddata[a].GridStatus == 2):
            
            oldx = self.grddata[a].xm[0,:]
            oldy = self.grddata[a].ym[:,0]
            oldz = self.grddata[a].wm
            
            f = RectBivariateSpline(oldx,oldy,oldz)
            
            xtemp = r_[self.xCenter-self.xViewLen/2.:self.xCenter+self.xViewLen/2.:200j]
            ytemp = r_[self.yCenter-self.yViewLen/2.:self.yCenter+self.yViewLen/2.:200j]
            [xm,ym] = meshgrid(xtemp,ytemp)

            z = f(xtemp,ytemp)
            zm = transpose(z.reshape(shape(xm)))
            
            self.mplwidget.axes.cla()
            self.mplwidget.axes.pcolormesh(xm,ym,zm,vmin=amin(oldz),vmax=amax(oldz))

#            self.mplwidget.axes.pcolormesh(self.grddata[a].xm,self.grddata[a].ym,self.grddata[a].wm,edgecolors='None',shading='None',rasterized=True)
            self.mplwidget.axes.set_xlim((self.xCenter-self.xViewLen/2.,self.xCenter+self.xViewLen/2.))
            self.mplwidget.axes.set_ylim((self.yCenter-self.yViewLen/2.,self.yCenter+self.yViewLen/2.))
            self.mplwidget.draw()
        else:
            self.mplwidget.axes.cla()
            self.mplwidget.axes.set_xlim((self.xCenter-self.xViewLen/2.,self.xCenter+self.xViewLen/2.))
            self.mplwidget.axes.set_ylim((self.yCenter-self.yViewLen/2.,self.yCenter+self.yViewLen/2.))
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

#  Queue up nearby frames.
        for k in range(max(a-4,self.CurrentFrame.minimum()),min(a+5,self.CurrentFrame.maximum())):
            if not k in self.grddata:
                self.grddata[k] = Vorticity_Frame(self.host,self.port,k,self.VtxChangeStatus,domainLL=self.domainLL,domainUR=self.domainUR)
 
    def plot(self, axes):
        self.newplot()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    plot = Plot_Widget(sys.argv)
    plot.show()

    sys.exit(app.exec_())


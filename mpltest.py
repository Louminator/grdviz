# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mpltest.ui'
#
# Created: Sun Oct  6 23:04:34 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_BlobFlowExplorer(object):
    def setupUi(self, BlobFlowExplorer):
        BlobFlowExplorer.setObjectName(_fromUtf8("BlobFlowExplorer"))
        BlobFlowExplorer.resize(700, 515)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(BlobFlowExplorer.sizePolicy().hasHeightForWidth())
        BlobFlowExplorer.setSizePolicy(sizePolicy)
        self.mplwidget = MatplotlibWidget(BlobFlowExplorer)
        self.mplwidget.setGeometry(QtCore.QRect(280, 10, 400, 300))
        self.mplwidget.setObjectName(_fromUtf8("mplwidget"))
        self.pushButton = QtGui.QPushButton(BlobFlowExplorer)
        self.pushButton.setGeometry(QtCore.QRect(590, 480, 90, 24))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.timeDial = QtGui.QDial(BlobFlowExplorer)
        self.timeDial.setGeometry(QtCore.QRect(210, 370, 50, 64))
        self.timeDial.setObjectName(_fromUtf8("timeDial"))
        self.verticalLayoutWidget = QtGui.QWidget(BlobFlowExplorer)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 320, 160, 113))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.line = QtGui.QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.line_2 = QtGui.QFrame(self.verticalLayoutWidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout.addWidget(self.line_2)
        self.Play = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.Play.setObjectName(_fromUtf8("Play"))
        self.verticalLayout.addWidget(self.Play)
        self.Rewind = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.Rewind.setObjectName(_fromUtf8("Rewind"))
        self.verticalLayout.addWidget(self.Rewind)
        self.Pause = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.Pause.setChecked(True)
        self.Pause.setObjectName(_fromUtf8("Pause"))
        self.verticalLayout.addWidget(self.Pause)
        self.line_3 = QtGui.QFrame(self.verticalLayoutWidget)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.verticalLayout.addWidget(self.line_3)
        self.horizontalLayoutWidget = QtGui.QWidget(BlobFlowExplorer)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(280, 390, 401, 80))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.horizontalScrollBar = QtGui.QScrollBar(self.horizontalLayoutWidget)
        self.horizontalScrollBar.setInputMethodHints(QtCore.Qt.ImhNone)
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName(_fromUtf8("horizontalScrollBar"))
        self.horizontalLayout.addWidget(self.horizontalScrollBar)
        self.CurrentFrame = QtGui.QSpinBox(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CurrentFrame.sizePolicy().hasHeightForWidth())
        self.CurrentFrame.setSizePolicy(sizePolicy)
        self.CurrentFrame.setObjectName(_fromUtf8("CurrentFrame"))
        self.horizontalLayout.addWidget(self.CurrentFrame)
        self.layoutWidget = QtGui.QWidget(BlobFlowExplorer)
        self.layoutWidget.setGeometry(QtCore.QRect(300, 320, 361, 52))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.xMin = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.xMin.setMinimum(-1000.0)
        self.xMin.setMaximum(1000.0)
        self.xMin.setObjectName(_fromUtf8("xMin"))
        self.horizontalLayout_2.addWidget(self.xMin)
        self.xMinDial = QtGui.QDial(self.layoutWidget)
        self.xMinDial.setObjectName(_fromUtf8("xMinDial"))
        self.horizontalLayout_2.addWidget(self.xMinDial)
        self.resetZoomx = QtGui.QPushButton(self.layoutWidget)
        self.resetZoomx.setObjectName(_fromUtf8("resetZoomx"))
        self.horizontalLayout_2.addWidget(self.resetZoomx)
        self.xMaxDial = QtGui.QDial(self.layoutWidget)
        self.xMaxDial.setObjectName(_fromUtf8("xMaxDial"))
        self.horizontalLayout_2.addWidget(self.xMaxDial)
        self.xMax = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.xMax.setMinimum(-1000.0)
        self.xMax.setMaximum(1000.0)
        self.xMax.setProperty("value", 1.0)
        self.xMax.setObjectName(_fromUtf8("xMax"))
        self.horizontalLayout_2.addWidget(self.xMax)
        self.layoutWidget1 = QtGui.QWidget(BlobFlowExplorer)
        self.layoutWidget1.setGeometry(QtCore.QRect(209, 40, 61, 251))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.yMax = QtGui.QDoubleSpinBox(self.layoutWidget1)
        self.yMax.setMinimum(-1000.0)
        self.yMax.setMaximum(1000.0)
        self.yMax.setSingleStep(0.1)
        self.yMax.setProperty("value", 1.0)
        self.yMax.setObjectName(_fromUtf8("yMax"))
        self.verticalLayout_2.addWidget(self.yMax)
        self.yMaxDial = QtGui.QDial(self.layoutWidget1)
        self.yMaxDial.setObjectName(_fromUtf8("yMaxDial"))
        self.verticalLayout_2.addWidget(self.yMaxDial)
        self.resetZoomy = QtGui.QPushButton(self.layoutWidget1)
        self.resetZoomy.setObjectName(_fromUtf8("resetZoomy"))
        self.verticalLayout_2.addWidget(self.resetZoomy)
        self.yMinDial = QtGui.QDial(self.layoutWidget1)
        self.yMinDial.setObjectName(_fromUtf8("yMinDial"))
        self.verticalLayout_2.addWidget(self.yMinDial)
        self.yMin = QtGui.QDoubleSpinBox(self.layoutWidget1)
        self.yMin.setMinimum(-1000.0)
        self.yMin.setMaximum(1000.0)
        self.yMin.setObjectName(_fromUtf8("yMin"))
        self.verticalLayout_2.addWidget(self.yMin)

        self.retranslateUi(BlobFlowExplorer)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), BlobFlowExplorer.quit_gui)
        QtCore.QObject.connect(self.timeDial, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.horizontalScrollBar.setValue)
        QtCore.QObject.connect(self.horizontalScrollBar, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.timeDial.setValue)
        QtCore.QObject.connect(self.horizontalScrollBar, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.CurrentFrame.setValue)
        QtCore.QObject.connect(self.CurrentFrame, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.horizontalScrollBar.setValue)
        QtCore.QObject.connect(self.Play, QtCore.SIGNAL(_fromUtf8("clicked()")), BlobFlowExplorer.play)
        QtCore.QObject.connect(self.Rewind, QtCore.SIGNAL(_fromUtf8("clicked()")), BlobFlowExplorer.play)
        QtCore.QObject.connect(self.Pause, QtCore.SIGNAL(_fromUtf8("clicked()")), BlobFlowExplorer.pause)
        QtCore.QObject.connect(self.xMin, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), BlobFlowExplorer.newplot)
        QtCore.QObject.connect(self.xMax, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), BlobFlowExplorer.newplot)
        QtCore.QObject.connect(self.yMin, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), BlobFlowExplorer.newplot)
        QtCore.QObject.connect(self.yMax, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), BlobFlowExplorer.newplot)
        QtCore.QObject.connect(self.CurrentFrame, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), BlobFlowExplorer.newplot)
        QtCore.QObject.connect(self.yMinDial, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), BlobFlowExplorer.yMinDialChanged)
        QtCore.QObject.connect(self.yMaxDial, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), BlobFlowExplorer.yMaxDialChanged)
        QtCore.QObject.connect(self.xMinDial, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), BlobFlowExplorer.xMinDialChanged)
        QtCore.QObject.connect(self.xMaxDial, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), BlobFlowExplorer.xMaxDialChanged)
        QtCore.QObject.connect(self.yMin, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), BlobFlowExplorer.yMinChanged)
        QtCore.QObject.connect(self.xMin, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), BlobFlowExplorer.xMinChanged)
        QtCore.QObject.connect(self.resetZoomx, QtCore.SIGNAL(_fromUtf8("clicked()")), BlobFlowExplorer.ResetZoomx)
        QtCore.QObject.connect(self.xMax, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), BlobFlowExplorer.xMaxChanged)
        QtCore.QObject.connect(self.yMax, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), BlobFlowExplorer.yMaxChanged)
        QtCore.QObject.connect(self.resetZoomy, QtCore.SIGNAL(_fromUtf8("clicked()")), BlobFlowExplorer.ResetZoomy)
        QtCore.QMetaObject.connectSlotsByName(BlobFlowExplorer)

    def retranslateUi(self, BlobFlowExplorer):
        BlobFlowExplorer.setWindowTitle(QtGui.QApplication.translate("BlobFlowExplorer", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("BlobFlowExplorer", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("BlobFlowExplorer", "Play", None, QtGui.QApplication.UnicodeUTF8))
        self.Play.setText(QtGui.QApplication.translate("BlobFlowExplorer", "Forward", None, QtGui.QApplication.UnicodeUTF8))
        self.Rewind.setText(QtGui.QApplication.translate("BlobFlowExplorer", "Rewind", None, QtGui.QApplication.UnicodeUTF8))
        self.Pause.setText(QtGui.QApplication.translate("BlobFlowExplorer", "Pause", None, QtGui.QApplication.UnicodeUTF8))
        self.Pause.setShortcut(QtGui.QApplication.translate("BlobFlowExplorer", "Ctrl+R, Ctrl+R", None, QtGui.QApplication.UnicodeUTF8))
        self.resetZoomx.setText(QtGui.QApplication.translate("BlobFlowExplorer", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.resetZoomy.setText(QtGui.QApplication.translate("BlobFlowExplorer", "Reset", None, QtGui.QApplication.UnicodeUTF8))

from matplotlibwidget import MatplotlibWidget

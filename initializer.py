# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'initializer.ui'
#
# Created: Fri May 30 21:29:41 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_BlobFlow_creator(object):
    def setupUi(self, BlobFlow_creator):
        BlobFlow_creator.setObjectName(_fromUtf8("BlobFlow_creator"))
        BlobFlow_creator.resize(980, 518)
        self.mplwidget = MatplotlibWidget(BlobFlow_creator)
        self.mplwidget.setGeometry(QtCore.QRect(510, 40, 261, 211))
        self.mplwidget.setObjectName(_fromUtf8("mplwidget"))
        self.plainTextEdit = QtGui.QPlainTextEdit(BlobFlow_creator)
        self.plainTextEdit.setGeometry(QtCore.QRect(180, 30, 311, 221))
        self.plainTextEdit.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.functionDef = QtGui.QPlainTextEdit(BlobFlow_creator)
        self.functionDef.setGeometry(QtCore.QRect(180, 280, 311, 211))
        self.functionDef.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.functionDef.setReadOnly(True)
        self.functionDef.setObjectName(_fromUtf8("functionDef"))
        self.plotButton = QtGui.QPushButton(BlobFlow_creator)
        self.plotButton.setGeometry(QtCore.QRect(10, 490, 90, 24))
        self.plotButton.setObjectName(_fromUtf8("plotButton"))
        self.label = QtGui.QLabel(BlobFlow_creator)
        self.label.setGeometry(QtCore.QRect(10, 10, 53, 15))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayoutWidget = QtGui.QWidget(BlobFlow_creator)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 50, 141, 90))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.yDomainMax = QtGui.QLineEdit(self.gridLayoutWidget)
        self.yDomainMax.setObjectName(_fromUtf8("yDomainMax"))
        self.gridLayout.addWidget(self.yDomainMax, 2, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 1, 1, 1)
        self.xDomainMax = QtGui.QLineEdit(self.gridLayoutWidget)
        self.xDomainMax.setObjectName(_fromUtf8("xDomainMax"))
        self.gridLayout.addWidget(self.xDomainMax, 0, 1, 1, 1)
        self.yDomainMin = QtGui.QLineEdit(self.gridLayoutWidget)
        self.yDomainMin.setObjectName(_fromUtf8("yDomainMin"))
        self.gridLayout.addWidget(self.yDomainMin, 2, 0, 1, 1)
        self.xDomainMin = QtGui.QLineEdit(self.gridLayoutWidget)
        self.xDomainMin.setObjectName(_fromUtf8("xDomainMin"))
        self.gridLayout.addWidget(self.xDomainMin, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 1, 1, 1)
        self.nMesh = QtGui.QLineEdit(BlobFlow_creator)
        self.nMesh.setGeometry(QtCore.QRect(10, 220, 71, 21))
        self.nMesh.setObjectName(_fromUtf8("nMesh"))
        self.label_6 = QtGui.QLabel(BlobFlow_creator)
        self.label_6.setGeometry(QtCore.QRect(10, 190, 101, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(BlobFlow_creator)
        self.label_7.setGeometry(QtCore.QRect(180, 10, 181, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(BlobFlow_creator)
        self.label_8.setGeometry(QtCore.QRect(180, 260, 201, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(BlobFlow_creator)
        self.label_9.setGeometry(QtCore.QRect(10, 250, 91, 16))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.saveButton = QtGui.QPushButton(BlobFlow_creator)
        self.saveButton.setGeometry(QtCore.QRect(240, 490, 141, 24))
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.saveFun = QtGui.QPushButton(BlobFlow_creator)
        self.saveFun.setGeometry(QtCore.QRect(110, 490, 101, 24))
        self.saveFun.setObjectName(_fromUtf8("saveFun"))

        self.retranslateUi(BlobFlow_creator)
        QtCore.QObject.connect(self.plainTextEdit, QtCore.SIGNAL(_fromUtf8("textChanged()")), BlobFlow_creator.functionChanged)
        QtCore.QObject.connect(self.plotButton, QtCore.SIGNAL(_fromUtf8("clicked()")), BlobFlow_creator.plotFunction)
        QtCore.QObject.connect(self.xDomainMin, QtCore.SIGNAL(_fromUtf8("returnPressed()")), BlobFlow_creator.xMinChanged)
        QtCore.QObject.connect(self.xDomainMax, QtCore.SIGNAL(_fromUtf8("returnPressed()")), BlobFlow_creator.xMaxChanged)
        QtCore.QObject.connect(self.yDomainMin, QtCore.SIGNAL(_fromUtf8("returnPressed()")), BlobFlow_creator.yMinChanged)
        QtCore.QObject.connect(self.yDomainMax, QtCore.SIGNAL(_fromUtf8("returnPressed()")), BlobFlow_creator.yMaxChanged)
        QtCore.QObject.connect(self.saveButton, QtCore.SIGNAL(_fromUtf8("clicked()")), BlobFlow_creator.saveDataFile)
        QtCore.QObject.connect(self.saveFun, QtCore.SIGNAL(_fromUtf8("clicked()")), BlobFlow_creator.saveFunction)
        QtCore.QMetaObject.connectSlotsByName(BlobFlow_creator)

    def retranslateUi(self, BlobFlow_creator):
        BlobFlow_creator.setWindowTitle(QtGui.QApplication.translate("BlobFlow_creator", "BlobFlow Creator", None, QtGui.QApplication.UnicodeUTF8))
        self.plainTextEdit.setPlainText(QtGui.QApplication.translate("BlobFlow_creator", "    w = cos(x)*sin(y)\n"
"    ind = (x>2) & (x<6) & (y>5) & (y<8)\n"
"    w[ind] = exp(-(x[ind]**2+y[ind]**2)/50)\n"
"", None, QtGui.QApplication.UnicodeUTF8))
        self.plotButton.setText(QtGui.QApplication.translate("BlobFlow_creator", "Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("BlobFlow_creator", "Domain", None, QtGui.QApplication.UnicodeUTF8))
        self.yDomainMax.setText(QtGui.QApplication.translate("BlobFlow_creator", "1.0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("BlobFlow_creator", "xMax", None, QtGui.QApplication.UnicodeUTF8))
        self.xDomainMax.setText(QtGui.QApplication.translate("BlobFlow_creator", "1.0", None, QtGui.QApplication.UnicodeUTF8))
        self.yDomainMin.setText(QtGui.QApplication.translate("BlobFlow_creator", "-1.0", None, QtGui.QApplication.UnicodeUTF8))
        self.xDomainMin.setText(QtGui.QApplication.translate("BlobFlow_creator", "-1.0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("BlobFlow_creator", "xMin", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("BlobFlow_creator", "yMin", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("BlobFlow_creator", "yMax", None, QtGui.QApplication.UnicodeUTF8))
        self.nMesh.setText(QtGui.QApplication.translate("BlobFlow_creator", "10", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("BlobFlow_creator", "Mesh parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("BlobFlow_creator", "Initial condition entry", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("BlobFlow_creator", "Python initial condition definition", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("BlobFlow_creator", "Mesh points", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("BlobFlow_creator", "Create  sim data file", None, QtGui.QApplication.UnicodeUTF8))
        self.saveFun.setText(QtGui.QApplication.translate("BlobFlow_creator", "Save function", None, QtGui.QApplication.UnicodeUTF8))

from matplotlibwidget import MatplotlibWidget

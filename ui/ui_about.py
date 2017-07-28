# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'K:\Library\Python\AssetsBrowser\ui\about.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName(_fromUtf8("AboutDialog"))
        AboutDialog.resize(240, 250)
        AboutDialog.setMinimumSize(QtCore.QSize(240, 250))
        AboutDialog.setMaximumSize(QtCore.QSize(240, 250))
        self.buttonBox = QtGui.QDialogButtonBox(AboutDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 210, 221, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.labelAbout = QtGui.QLabel(AboutDialog)
        self.labelAbout.setGeometry(QtCore.QRect(10, 120, 221, 80))
        self.labelAbout.setAlignment(QtCore.Qt.AlignCenter)
        self.labelAbout.setWordWrap(True)
        self.labelAbout.setObjectName(_fromUtf8("labelAbout"))
        self.labelGraphic = QtGui.QLabel(AboutDialog)
        self.labelGraphic.setGeometry(QtCore.QRect(25, 20, 192, 96))
        self.labelGraphic.setText(_fromUtf8(""))
        self.labelGraphic.setTextFormat(QtCore.Qt.AutoText)
        self.labelGraphic.setPixmap(QtGui.QPixmap(_fromUtf8("../icons/about.png")))
        self.labelGraphic.setScaledContents(False)
        self.labelGraphic.setObjectName(_fromUtf8("labelGraphic"))

        self.retranslateUi(AboutDialog)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(_translate("AboutDialog", "About", None))
        self.labelAbout.setText(_translate("AboutDialog", "<html><head/><body><p><span style=\" font-weight:600;\">Assets Browser<br/>Version 0.1.0</span></p><p>A Python based browser to manage various assets in a 3DCG/VFX production.</p></body></html>", None))


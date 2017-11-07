# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'K:\Library\Python\AssetsBrowser\ui\about.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(240, 250)
        AboutDialog.setMinimumSize(QtCore.QSize(240, 250))
        AboutDialog.setMaximumSize(QtCore.QSize(240, 250))
        self.buttonBox = QtWidgets.QDialogButtonBox(AboutDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 210, 221, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.labelAbout = QtWidgets.QLabel(AboutDialog)
        self.labelAbout.setGeometry(QtCore.QRect(10, 120, 221, 80))
        self.labelAbout.setAlignment(QtCore.Qt.AlignCenter)
        self.labelAbout.setWordWrap(True)
        self.labelAbout.setObjectName("labelAbout")
        self.labelGraphic = QtWidgets.QLabel(AboutDialog)
        self.labelGraphic.setGeometry(QtCore.QRect(25, 20, 192, 96))
        self.labelGraphic.setText("")
        self.labelGraphic.setTextFormat(QtCore.Qt.AutoText)
        self.labelGraphic.setPixmap(QtGui.QPixmap("../icons/about.png"))
        self.labelGraphic.setScaledContents(False)
        self.labelGraphic.setObjectName("labelGraphic")

        self.retranslateUi(AboutDialog)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate("AboutDialog", "About"))
        self.labelAbout.setText(_translate("AboutDialog", "<html><head/><body><p><span style=\" font-weight:600;\">Assets Browser<br/>Version 0.1.0</span></p><p>A Python based browser to manage various assets in a 3DCG/VFX production.</p></body></html>"))


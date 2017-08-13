# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'K:\Library\Python\AssetsBrowser\ui\asset.ui'
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

class Ui_AssetDialog(object):
    def setupUi(self, AssetDialog):
        AssetDialog.setObjectName(_fromUtf8("AssetDialog"))
        AssetDialog.resize(320, 440)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AssetDialog.sizePolicy().hasHeightForWidth())
        AssetDialog.setSizePolicy(sizePolicy)
        AssetDialog.setMinimumSize(QtCore.QSize(320, 440))
        AssetDialog.setMaximumSize(QtCore.QSize(320, 440))
        self.catGroup = QtGui.QGroupBox(AssetDialog)
        self.catGroup.setGeometry(QtCore.QRect(10, 70, 80, 161))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.catGroup.setFont(font)
        self.catGroup.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.catGroup.setFlat(False)
        self.catGroup.setCheckable(False)
        self.catGroup.setObjectName(_fromUtf8("catGroup"))
        self.catBG = QtGui.QRadioButton(self.catGroup)
        self.catBG.setGeometry(QtCore.QRect(10, 26, 36, 17))
        self.catBG.setObjectName(_fromUtf8("catBG"))
        self.catBtnGroup = QtGui.QButtonGroup(AssetDialog)
        self.catBtnGroup.setObjectName(_fromUtf8("catBtnGroup"))
        self.catBtnGroup.addButton(self.catBG)
        self.catCH = QtGui.QRadioButton(self.catGroup)
        self.catCH.setGeometry(QtCore.QRect(10, 52, 37, 17))
        self.catCH.setObjectName(_fromUtf8("catCH"))
        self.catBtnGroup.addButton(self.catCH)
        self.catFX = QtGui.QRadioButton(self.catGroup)
        self.catFX.setGeometry(QtCore.QRect(10, 78, 35, 17))
        self.catFX.setObjectName(_fromUtf8("catFX"))
        self.catBtnGroup.addButton(self.catFX)
        self.catProps = QtGui.QRadioButton(self.catGroup)
        self.catProps.setGeometry(QtCore.QRect(10, 104, 50, 17))
        self.catProps.setObjectName(_fromUtf8("catProps"))
        self.catBtnGroup.addButton(self.catProps)
        self.catVehicles = QtGui.QRadioButton(self.catGroup)
        self.catVehicles.setGeometry(QtCore.QRect(10, 130, 60, 17))
        self.catVehicles.setObjectName(_fromUtf8("catVehicles"))
        self.catBtnGroup.addButton(self.catVehicles)
        self.previewGroup = QtGui.QGroupBox(AssetDialog)
        self.previewGroup.setGeometry(QtCore.QRect(10, 270, 291, 120))
        self.previewGroup.setCheckable(True)
        self.previewGroup.setChecked(False)
        self.previewGroup.setObjectName(_fromUtf8("previewGroup"))
        self.previewText = QtGui.QPlainTextEdit(self.previewGroup)
        self.previewText.setGeometry(QtCore.QRect(10, 20, 271, 90))
        self.previewText.setReadOnly(True)
        self.previewText.setObjectName(_fromUtf8("previewText"))
        self.descGroup = QtGui.QGroupBox(AssetDialog)
        self.descGroup.setEnabled(False)
        self.descGroup.setGeometry(QtCore.QRect(100, 70, 201, 161))
        self.descGroup.setObjectName(_fromUtf8("descGroup"))
        self.descNameLineEdit = QtGui.QLineEdit(self.descGroup)
        self.descNameLineEdit.setGeometry(QtCore.QRect(20, 40, 171, 21))
        self.descNameLineEdit.setObjectName(_fromUtf8("descNameLineEdit"))
        self.descName = QtGui.QLabel(self.descGroup)
        self.descName.setGeometry(QtCore.QRect(20, 20, 61, 16))
        self.descName.setObjectName(_fromUtf8("descName"))
        self.descHint = QtGui.QLabel(self.descGroup)
        self.descHint.setGeometry(QtCore.QRect(20, 72, 171, 71))
        self.descHint.setTextFormat(QtCore.Qt.AutoText)
        self.descHint.setScaledContents(False)
        self.descHint.setWordWrap(True)
        self.descHint.setObjectName(_fromUtf8("descHint"))
        self.assetLabel = QtGui.QLabel(AssetDialog)
        self.assetLabel.setGeometry(QtCore.QRect(20, 30, 158, 16))
        self.assetLabel.setObjectName(_fromUtf8("assetLabel"))
        self.assetLineEdit = QtGui.QLineEdit(AssetDialog)
        self.assetLineEdit.setGeometry(QtCore.QRect(190, 30, 101, 20))
        self.assetLineEdit.setMaxLength(3)
        self.assetLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.assetLineEdit.setObjectName(_fromUtf8("assetLineEdit"))
        self.btnCreate = QtGui.QPushButton(AssetDialog)
        self.btnCreate.setGeometry(QtCore.QRect(141, 400, 75, 23))
        self.btnCreate.setObjectName(_fromUtf8("btnCreate"))
        self.btnCancel = QtGui.QPushButton(AssetDialog)
        self.btnCancel.setGeometry(QtCore.QRect(222, 400, 75, 23))
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.previewLabel = QtGui.QLabel(AssetDialog)
        self.previewLabel.setGeometry(QtCore.QRect(20, 240, 271, 21))
        self.previewLabel.setObjectName(_fromUtf8("previewLabel"))
        self.catGroup.raise_()
        self.previewGroup.raise_()
        self.descGroup.raise_()
        self.assetLineEdit.raise_()
        self.assetLabel.raise_()
        self.btnCreate.raise_()
        self.btnCancel.raise_()
        self.previewLabel.raise_()

        self.retranslateUi(AssetDialog)
        QtCore.QMetaObject.connectSlotsByName(AssetDialog)

    def retranslateUi(self, AssetDialog):
        AssetDialog.setWindowTitle(_translate("AssetDialog", "Create New Asset", None))
        self.catGroup.setTitle(_translate("AssetDialog", "Category", None))
        self.catBG.setText(_translate("AssetDialog", "BG", None))
        self.catCH.setText(_translate("AssetDialog", "CH", None))
        self.catFX.setText(_translate("AssetDialog", "FX", None))
        self.catProps.setText(_translate("AssetDialog", "Props", None))
        self.catVehicles.setText(_translate("AssetDialog", "Vehicles", None))
        self.previewGroup.setTitle(_translate("AssetDialog", "Preview", None))
        self.descGroup.setTitle(_translate("AssetDialog", "Description (disabled)", None))
        self.descName.setText(_translate("AssetDialog", "Full Name:", None))
        self.descHint.setText(_translate("AssetDialog", "<html><head/><body><p>Remember to write meaningful Full Name for easy identification. E.g.:</p><p>HSE - House<br/>PAU - Pope\'s Aura Flame</p></body></html>", None))
        self.assetLabel.setText(_translate("AssetDialog", "Asset Name (max 3 characters) :", None))
        self.assetLineEdit.setToolTip(_translate("AssetDialog", "Alphanumeric only", None))
        self.btnCreate.setText(_translate("AssetDialog", "Create", None))
        self.btnCancel.setText(_translate("AssetDialog", "Cancel", None))
        self.previewLabel.setText(_translate("AssetDialog", "*Preview must be checked to enable Create", None))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'K:\Library\Python\AssetsBrowser\ui\preferences.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PrefsDialog(object):
    def setupUi(self, PrefsDialog):
        PrefsDialog.setObjectName("PrefsDialog")
        PrefsDialog.setMinimumSize(QtCore.QSize(400, 160))
        PrefsDialog.setMaximumSize(QtCore.QSize(800, 160))
        PrefsDialog.setFocusPolicy(QtCore.Qt.StrongFocus)
        PrefsDialog.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        PrefsDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(PrefsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.formLayout.setObjectName("formLayout")
        self.theme_radio1 = QtWidgets.QRadioButton(PrefsDialog)
        self.theme_radio1.setShortcut("")
        self.theme_radio1.setChecked(True)
        self.theme_radio1.setObjectName("theme_radio1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.theme_radio1)
        self.theme_radio2 = QtWidgets.QRadioButton(PrefsDialog)
        self.theme_radio2.setShortcut("")
        self.theme_radio2.setObjectName("theme_radio2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.theme_radio2)
        self.gridLayout.addLayout(self.formLayout, 4, 0, 1, 1)
        self.btn_layout = QtWidgets.QHBoxLayout()
        self.btn_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.btn_layout.setObjectName("btn_layout")
        self.btn_ok = QtWidgets.QDialogButtonBox(PrefsDialog)
        self.btn_ok.setOrientation(QtCore.Qt.Horizontal)
        self.btn_ok.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.btn_ok.setCenterButtons(True)
        self.btn_ok.setObjectName("btn_ok")
        self.btn_layout.addWidget(self.btn_ok)
        self.btn_cancel = QtWidgets.QDialogButtonBox(PrefsDialog)
        self.btn_cancel.setOrientation(QtCore.Qt.Horizontal)
        self.btn_cancel.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.btn_cancel.setCenterButtons(True)
        self.btn_cancel.setObjectName("btn_cancel")
        self.btn_layout.addWidget(self.btn_cancel)
        self.gridLayout.addLayout(self.btn_layout, 5, 0, 1, 1)
        self.proj_layout = QtWidgets.QHBoxLayout()
        self.proj_layout.setObjectName("proj_layout")
        self.projectpath_label = QtWidgets.QLabel(PrefsDialog)
        self.projectpath_label.setSizeIncrement(QtCore.QSize(0, 0))
        self.projectpath_label.setObjectName("projectpath_label")
        self.proj_layout.addWidget(self.projectpath_label)
        self.projectpath_line = QtWidgets.QLineEdit(PrefsDialog)
        self.projectpath_line.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.projectpath_line.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.projectpath_line.setDragEnabled(False)
        self.projectpath_line.setPlaceholderText("")
        self.projectpath_line.setObjectName("projectpath_line")
        self.proj_layout.addWidget(self.projectpath_line)
        self.projectpath_tool = QtWidgets.QToolButton(PrefsDialog)
        self.projectpath_tool.setAutoRaise(False)
        self.projectpath_tool.setArrowType(QtCore.Qt.NoArrow)
        self.projectpath_tool.setObjectName("projectpath_tool")
        self.proj_layout.addWidget(self.projectpath_tool)
        self.gridLayout.addLayout(self.proj_layout, 0, 0, 1, 1)
        self.desc_check = QtWidgets.QCheckBox(PrefsDialog)
        self.desc_check.setObjectName("desc_check")
        self.gridLayout.addWidget(self.desc_check, 1, 0, 1, 1)
        self.theme_label = QtWidgets.QLabel(PrefsDialog)
        self.theme_label.setObjectName("theme_label")
        self.gridLayout.addWidget(self.theme_label, 3, 0, 1, 1)
        self.debug_check = QtWidgets.QCheckBox(PrefsDialog)
        self.debug_check.setObjectName("debug_check")
        self.gridLayout.addWidget(self.debug_check, 2, 0, 1, 1)
        self.theme_label.raise_()
        self.desc_check.raise_()
        self.debug_check.raise_()

        self.retranslateUi(PrefsDialog)
        self.btn_ok.accepted.connect(PrefsDialog.accept)
        self.btn_ok.rejected.connect(PrefsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PrefsDialog)

    def retranslateUi(self, PrefsDialog):
        _translate = QtCore.QCoreApplication.translate
        PrefsDialog.setWindowTitle(_translate("PrefsDialog", "Preferences"))
        self.theme_radio1.setText(_translate("PrefsDialog", "Default (Fusion)"))
        self.theme_radio2.setText(_translate("PrefsDialog", "Windows"))
        self.projectpath_label.setText(_translate("PrefsDialog", "Project Path:"))
        self.projectpath_line.setToolTip(_translate("PrefsDialog", "Insert your project path here. E.g. \"P:/\", \"media/projects\""))
        self.projectpath_tool.setToolTip(_translate("PrefsDialog", "Choose directory"))
        self.projectpath_tool.setText(_translate("PrefsDialog", "..."))
        self.desc_check.setText(_translate("PrefsDialog", "Show Description Panel"))
        self.theme_label.setText(_translate("PrefsDialog", "Theme:"))
        self.debug_check.setText(_translate("PrefsDialog", "Enable Debug Log"))

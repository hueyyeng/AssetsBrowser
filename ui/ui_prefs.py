# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'K:\Library\Python\AssetsBrowser\ui\prefs.ui'
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

class Ui_PrefsDialog(object):
    def setupUi(self, PrefsDialog):
        PrefsDialog.setObjectName(_fromUtf8("PrefsDialog"))
        PrefsDialog.resize(400, 160)
        PrefsDialog.setMinimumSize(QtCore.QSize(400, 160))
        PrefsDialog.setMaximumSize(QtCore.QSize(800, 160))
        PrefsDialog.setFocusPolicy(QtCore.Qt.StrongFocus)
        PrefsDialog.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        PrefsDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(PrefsDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.projectpath_label = QtGui.QLabel(PrefsDialog)
        self.projectpath_label.setSizeIncrement(QtCore.QSize(0, 0))
        self.projectpath_label.setObjectName(_fromUtf8("projectpath_label"))
        self.gridLayout.addWidget(self.projectpath_label, 0, 0, 1, 1)
        self.proj_layout = QtGui.QHBoxLayout()
        self.proj_layout.setObjectName(_fromUtf8("proj_layout"))
        self.projectpath_line = QtGui.QLineEdit(PrefsDialog)
        self.projectpath_line.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.projectpath_line.setEchoMode(QtGui.QLineEdit.Normal)
        self.projectpath_line.setDragEnabled(False)
        self.projectpath_line.setPlaceholderText(_fromUtf8(""))
        self.projectpath_line.setObjectName(_fromUtf8("projectpath_line"))
        self.proj_layout.addWidget(self.projectpath_line)
        self.projectpath_tool = QtGui.QToolButton(PrefsDialog)
        self.projectpath_tool.setAutoRaise(False)
        self.projectpath_tool.setArrowType(QtCore.Qt.NoArrow)
        self.projectpath_tool.setObjectName(_fromUtf8("projectpath_tool"))
        self.proj_layout.addWidget(self.projectpath_tool)
        self.gridLayout.addLayout(self.proj_layout, 0, 1, 1, 1)
        self.desc_check = QtGui.QCheckBox(PrefsDialog)
        self.desc_check.setObjectName(_fromUtf8("desc_check"))
        self.gridLayout.addWidget(self.desc_check, 1, 0, 1, 1)
        self.debug_check = QtGui.QCheckBox(PrefsDialog)
        self.debug_check.setObjectName(_fromUtf8("debug_check"))
        self.gridLayout.addWidget(self.debug_check, 2, 0, 1, 1)
        self.theme_label = QtGui.QLabel(PrefsDialog)
        self.theme_label.setObjectName(_fromUtf8("theme_label"))
        self.gridLayout.addWidget(self.theme_label, 3, 0, 1, 1)
        self.theme_layout = QtGui.QHBoxLayout()
        self.theme_layout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.theme_layout.setObjectName(_fromUtf8("theme_layout"))
        self.theme_radio1 = QtGui.QRadioButton(PrefsDialog)
        self.theme_radio1.setShortcut(_fromUtf8(""))
        self.theme_radio1.setChecked(True)
        self.theme_radio1.setObjectName(_fromUtf8("theme_radio1"))
        self.theme_layout.addWidget(self.theme_radio1)
        self.theme_radio2 = QtGui.QRadioButton(PrefsDialog)
        self.theme_radio2.setShortcut(_fromUtf8(""))
        self.theme_radio2.setObjectName(_fromUtf8("theme_radio2"))
        self.theme_layout.addWidget(self.theme_radio2)
        self.gridLayout.addLayout(self.theme_layout, 4, 0, 1, 1)
        self.btn_layout = QtGui.QHBoxLayout()
        self.btn_layout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.btn_layout.setObjectName(_fromUtf8("btn_layout"))
        self.btn_ok = QtGui.QDialogButtonBox(PrefsDialog)
        self.btn_ok.setOrientation(QtCore.Qt.Horizontal)
        self.btn_ok.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.btn_ok.setCenterButtons(True)
        self.btn_ok.setObjectName(_fromUtf8("btn_ok"))
        self.btn_layout.addWidget(self.btn_ok)
        self.btn_cancel = QtGui.QDialogButtonBox(PrefsDialog)
        self.btn_cancel.setOrientation(QtCore.Qt.Horizontal)
        self.btn_cancel.setStandardButtons(QtGui.QDialogButtonBox.Cancel)
        self.btn_cancel.setCenterButtons(True)
        self.btn_cancel.setObjectName(_fromUtf8("btn_cancel"))
        self.btn_layout.addWidget(self.btn_cancel)
        self.gridLayout.addLayout(self.btn_layout, 5, 0, 1, 2)
        self.projectpath_label.raise_()
        self.theme_label.raise_()
        self.desc_check.raise_()
        self.debug_check.raise_()

        self.retranslateUi(PrefsDialog)
        QtCore.QObject.connect(self.btn_ok, QtCore.SIGNAL(_fromUtf8("accepted()")), PrefsDialog.accept)
        QtCore.QObject.connect(self.btn_ok, QtCore.SIGNAL(_fromUtf8("rejected()")), PrefsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PrefsDialog)

    def retranslateUi(self, PrefsDialog):
        PrefsDialog.setWindowTitle(_translate("PrefsDialog", "Preferences", None))
        self.projectpath_label.setText(_translate("PrefsDialog", "Project Path:", None))
        self.projectpath_line.setToolTip(_translate("PrefsDialog", "Insert your project path here. E.g. \"P:/\", \"media/projects\"", None))
        self.projectpath_tool.setToolTip(_translate("PrefsDialog", "Choose directory", None))
        self.projectpath_tool.setText(_translate("PrefsDialog", "...", None))
        self.desc_check.setText(_translate("PrefsDialog", "Show Description Panel", None))
        self.debug_check.setText(_translate("PrefsDialog", "Enable Debug Log", None))
        self.theme_label.setText(_translate("PrefsDialog", "Theme:", None))
        self.theme_radio1.setText(_translate("PrefsDialog", "Default", None))
        self.theme_radio2.setText(_translate("PrefsDialog", "Plastique", None))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'K:\Library\Python\AssetsBrowser\ui\main.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        MainWindow.setFont(font)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setMinimumSize(QtCore.QSize(800, 550))
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.splitter = QtWidgets.QSplitter(self.centralWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.actionWidget = QtWidgets.QWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionWidget.sizePolicy().hasHeightForWidth())
        self.actionWidget.setSizePolicy(sizePolicy)
        self.actionWidget.setMinimumSize(QtCore.QSize(150, 0))
        self.actionWidget.setMaximumSize(QtCore.QSize(250, 16777215))
        self.actionWidget.setObjectName("actionWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.actionWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelProject = QtWidgets.QLabel(self.actionWidget)
        self.labelProject.setObjectName("labelProject")
        self.verticalLayout.addWidget(self.labelProject)
        self.comboBox = QtWidgets.QComboBox(self.actionWidget)
        self.comboBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
        self.comboBox.setFrame(True)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout.addWidget(self.comboBox)
        self.pushBtnNew = QtWidgets.QPushButton(self.actionWidget)
        self.pushBtnNew.setObjectName("pushBtnNew")
        self.verticalLayout.addWidget(self.pushBtnNew)
        self.checkBoxDebug = QtWidgets.QCheckBox(self.actionWidget)
        self.checkBoxDebug.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBoxDebug.sizePolicy().hasHeightForWidth())
        self.checkBoxDebug.setSizePolicy(sizePolicy)
        self.checkBoxDebug.setObjectName("checkBoxDebug")
        self.verticalLayout.addWidget(self.checkBoxDebug)
        self.textEdit = QtWidgets.QTextEdit(self.actionWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout.addItem(spacerItem)
        self.labelCredits = QtWidgets.QLabel(self.actionWidget)
        self.labelCredits.setTextFormat(QtCore.Qt.AutoText)
        self.labelCredits.setOpenExternalLinks(True)
        self.labelCredits.setObjectName("labelCredits")
        self.verticalLayout.addWidget(self.labelCredits)
        self.labelCredits.raise_()
        self.checkBoxDebug.raise_()
        self.pushBtnNew.raise_()
        self.labelProject.raise_()
        self.textEdit.raise_()
        self.comboBox.raise_()
        self.tabWidget = QtWidgets.QTabWidget(self.splitter)
        self.tabWidget.setObjectName("tabWidget")
        self.tabBG = QtWidgets.QWidget()
        self.tabBG.setObjectName("tabBG")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.tabBG)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.columnViewBG = QtWidgets.QColumnView(self.tabBG)
        self.columnViewBG.setAlternatingRowColors(False)
        self.columnViewBG.setResizeGripsVisible(True)
        self.columnViewBG.setObjectName("columnViewBG")
        self.horizontalLayout_6.addWidget(self.columnViewBG)
        self.tabWidget.addTab(self.tabBG, "")
        self.tabCH = QtWidgets.QWidget()
        self.tabCH.setObjectName("tabCH")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.tabCH)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.columnViewCH = QtWidgets.QColumnView(self.tabCH)
        self.columnViewCH.setAlternatingRowColors(False)
        self.columnViewCH.setResizeGripsVisible(True)
        self.columnViewCH.setObjectName("columnViewCH")
        self.horizontalLayout_5.addWidget(self.columnViewCH)
        self.tabWidget.addTab(self.tabCH, "")
        self.tabFX = QtWidgets.QWidget()
        self.tabFX.setObjectName("tabFX")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tabFX)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.columnViewFX = QtWidgets.QColumnView(self.tabFX)
        self.columnViewFX.setAlternatingRowColors(False)
        self.columnViewFX.setResizeGripsVisible(True)
        self.columnViewFX.setObjectName("columnViewFX")
        self.horizontalLayout_4.addWidget(self.columnViewFX)
        self.tabWidget.addTab(self.tabFX, "")
        self.tabProps = QtWidgets.QWidget()
        self.tabProps.setObjectName("tabProps")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.tabProps)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.columnViewProps = QtWidgets.QColumnView(self.tabProps)
        self.columnViewProps.setAlternatingRowColors(False)
        self.columnViewProps.setResizeGripsVisible(True)
        self.columnViewProps.setObjectName("columnViewProps")
        self.horizontalLayout_7.addWidget(self.columnViewProps)
        self.tabWidget.addTab(self.tabProps, "")
        self.tabVehicles = QtWidgets.QWidget()
        self.tabVehicles.setObjectName("tabVehicles")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.tabVehicles)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.columnViewVehicles = QtWidgets.QColumnView(self.tabVehicles)
        self.columnViewVehicles.setAlternatingRowColors(False)
        self.columnViewVehicles.setResizeGripsVisible(True)
        self.columnViewVehicles.setObjectName("columnViewVehicles")
        self.horizontalLayout_8.addWidget(self.columnViewVehicles)
        self.tabWidget.addTab(self.tabVehicles, "")
        self.tabHelp = QtWidgets.QWidget()
        self.tabHelp.setObjectName("tabHelp")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tabHelp)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frameHelp = QtWidgets.QFrame(self.tabHelp)
        self.frameHelp.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameHelp.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frameHelp.setObjectName("frameHelp")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frameHelp)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textBrowserHelp = QtWidgets.QTextBrowser(self.frameHelp)
        self.textBrowserHelp.setOpenExternalLinks(True)
        self.textBrowserHelp.setObjectName("textBrowserHelp")
        self.horizontalLayout.addWidget(self.textBrowserHelp)
        self.horizontalLayout_3.addWidget(self.frameHelp)
        self.tabWidget.addTab(self.tabHelp, "")
        self.horizontalLayout_2.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAlwaysOnTop = QtWidgets.QAction(MainWindow)
        self.actionAlwaysOnTop.setCheckable(True)
        self.actionAlwaysOnTop.setObjectName("actionAlwaysOnTop")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.menuFile.addAction(self.actionQuit)
        self.menuView.addAction(self.actionAlwaysOnTop)
        self.menuHelp.addAction(self.actionAbout)
        self.menuSettings.addAction(self.actionPreferences)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(5)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Assets Browser"))
        self.labelProject.setText(_translate("MainWindow", "Project:"))
        self.pushBtnNew.setText(_translate("MainWindow", "Create New Asset"))
        self.checkBoxDebug.setText(_translate("MainWindow", "Show Debug Panel"))
        self.labelCredits.setText(_translate("MainWindow", "<html><head/><body><p>Huey Yeng © 2017<br/><a href=\"https://taukeke.com\"><span style=\" text-decoration: underline; color:#0000ff;\">https://taukeke.com</span></a></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabBG), _translate("MainWindow", "BG"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCH), _translate("MainWindow", "CH"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFX), _translate("MainWindow", "FX"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabProps), _translate("MainWindow", "Props"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabVehicles), _translate("MainWindow", "Vehicles"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabHelp), _translate("MainWindow", "Help"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuView.setTitle(_translate("MainWindow", "&View"))
        self.menuHelp.setTitle(_translate("MainWindow", "&Help"))
        self.menuSettings.setTitle(_translate("MainWindow", "&Settings"))
        self.actionQuit.setText(_translate("MainWindow", "&Quit"))
        self.actionAbout.setText(_translate("MainWindow", "&About Assets Browser"))
        self.actionAlwaysOnTop.setText(_translate("MainWindow", "Always on &Top"))
        self.actionPreferences.setText(_translate("MainWindow", "&Preferences..."))


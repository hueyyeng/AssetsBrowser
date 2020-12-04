# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'K:\Library\Python\AssetsBrowser\ui\window\preferences.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PrefsDialog(object):
    def setupUi(self, PrefsDialog):
        PrefsDialog.setObjectName("PrefsDialog")
        PrefsDialog.setEnabled(True)
        PrefsDialog.resize(519, 614)
        PrefsDialog.setMinimumSize(QtCore.QSize(519, 614))
        PrefsDialog.setFocusPolicy(QtCore.Qt.StrongFocus)
        PrefsDialog.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        PrefsDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(PrefsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.sideLayout = QtWidgets.QVBoxLayout()
        self.sideLayout.setObjectName("sideLayout")
        self.sideList = QtWidgets.QListWidget(PrefsDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sideList.sizePolicy().hasHeightForWidth())
        self.sideList.setSizePolicy(sizePolicy)
        self.sideList.setMaximumSize(QtCore.QSize(100, 16777215))
        self.sideList.setObjectName("sideList")
        item = QtWidgets.QListWidgetItem()
        self.sideList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.sideList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.sideList.addItem(item)
        self.sideLayout.addWidget(self.sideList)
        self.gridLayout.addLayout(self.sideLayout, 3, 0, 2, 1)
        self.btnDialogBox = QtWidgets.QDialogButtonBox(PrefsDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnDialogBox.sizePolicy().hasHeightForWidth())
        self.btnDialogBox.setSizePolicy(sizePolicy)
        self.btnDialogBox.setOrientation(QtCore.Qt.Horizontal)
        self.btnDialogBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.RestoreDefaults)
        self.btnDialogBox.setCenterButtons(False)
        self.btnDialogBox.setObjectName("btnDialogBox")
        self.gridLayout.addWidget(self.btnDialogBox, 5, 1, 1, 1)
        self.stackedWidget = QtWidgets.QStackedWidget(PrefsDialog)
        self.stackedWidget.setObjectName("stackedWidget")
        self.pageGeneral = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pageGeneral.sizePolicy().hasHeightForWidth())
        self.pageGeneral.setSizePolicy(sizePolicy)
        self.pageGeneral.setObjectName("pageGeneral")
        self.formLayout_11 = QtWidgets.QFormLayout(self.pageGeneral)
        self.formLayout_11.setObjectName("formLayout_11")
        self.projectPathLayout = QtWidgets.QHBoxLayout()
        self.projectPathLayout.setObjectName("projectPathLayout")
        self.projectPathLabel = QtWidgets.QLabel(self.pageGeneral)
        self.projectPathLabel.setSizeIncrement(QtCore.QSize(0, 0))
        self.projectPathLabel.setObjectName("projectPathLabel")
        self.projectPathLayout.addWidget(self.projectPathLabel)
        self.projectPathLine = QtWidgets.QLineEdit(self.pageGeneral)
        self.projectPathLine.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.projectPathLine.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.projectPathLine.setDragEnabled(False)
        self.projectPathLine.setPlaceholderText("")
        self.projectPathLine.setObjectName("projectPathLine")
        self.projectPathLayout.addWidget(self.projectPathLine)
        self.projectPathTool = QtWidgets.QToolButton(self.pageGeneral)
        self.projectPathTool.setAutoRaise(False)
        self.projectPathTool.setArrowType(QtCore.Qt.NoArrow)
        self.projectPathTool.setObjectName("projectPathTool")
        self.projectPathLayout.addWidget(self.projectPathTool)
        self.formLayout_11.setLayout(0, QtWidgets.QFormLayout.SpanningRole, self.projectPathLayout)
        self.settingsDivider1 = QtWidgets.QFrame(self.pageGeneral)
        self.settingsDivider1.setFrameShape(QtWidgets.QFrame.HLine)
        self.settingsDivider1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.settingsDivider1.setObjectName("settingsDivider1")
        self.formLayout_11.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.settingsDivider1)
        self.descCheck = QtWidgets.QCheckBox(self.pageGeneral)
        self.descCheck.setObjectName("descCheck")
        self.formLayout_11.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.descCheck)
        self.settingsDivider2 = QtWidgets.QFrame(self.pageGeneral)
        self.settingsDivider2.setFrameShape(QtWidgets.QFrame.HLine)
        self.settingsDivider2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.settingsDivider2.setObjectName("settingsDivider2")
        self.formLayout_11.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.settingsDivider2)
        self.boxTheme = QtWidgets.QGroupBox(self.pageGeneral)
        self.boxTheme.setObjectName("boxTheme")
        self.formLayout = QtWidgets.QFormLayout(self.boxTheme)
        self.formLayout.setObjectName("formLayout")
        self.themeRadioLight = QtWidgets.QRadioButton(self.boxTheme)
        self.themeRadioLight.setShortcut("")
        self.themeRadioLight.setChecked(True)
        self.themeRadioLight.setObjectName("themeRadioLight")
        self.themeBtnGrp = QtWidgets.QButtonGroup(PrefsDialog)
        self.themeBtnGrp.setObjectName("themeBtnGrp")
        self.themeBtnGrp.addButton(self.themeRadioLight)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.themeRadioLight)
        self.themeRadioDark = QtWidgets.QRadioButton(self.boxTheme)
        self.themeRadioDark.setShortcut("")
        self.themeRadioDark.setObjectName("themeRadioDark")
        self.themeBtnGrp.addButton(self.themeRadioDark)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.themeRadioDark)
        self.formLayout_11.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.boxTheme)
        self.boxFont = QtWidgets.QGroupBox(self.pageGeneral)
        self.boxFont.setObjectName("boxFont")
        self.formLayout_10 = QtWidgets.QFormLayout(self.boxFont)
        self.formLayout_10.setObjectName("formLayout_10")
        self.fontRadioDefault = QtWidgets.QRadioButton(self.boxFont)
        self.fontRadioDefault.setChecked(True)
        self.fontRadioDefault.setObjectName("fontRadioDefault")
        self.fontBtnGrp = QtWidgets.QButtonGroup(PrefsDialog)
        self.fontBtnGrp.setObjectName("fontBtnGrp")
        self.fontBtnGrp.addButton(self.fontRadioDefault)
        self.formLayout_10.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.fontRadioDefault)
        self.fontRadioMonospace = QtWidgets.QRadioButton(self.boxFont)
        self.fontRadioMonospace.setObjectName("fontRadioMonospace")
        self.fontBtnGrp.addButton(self.fontRadioMonospace)
        self.formLayout_10.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.fontRadioMonospace)
        self.fontSizeLabel = QtWidgets.QLabel(self.boxFont)
        self.fontSizeLabel.setObjectName("fontSizeLabel")
        self.formLayout_10.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.fontSizeLabel)
        self.fontSizeComboBox = QtWidgets.QComboBox(self.boxFont)
        self.fontSizeComboBox.setObjectName("fontSizeComboBox")
        self.fontSizeComboBox.addItem("")
        self.fontSizeComboBox.addItem("")
        self.fontSizeComboBox.addItem("")
        self.formLayout_10.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.fontSizeComboBox)
        self.fontCustomLayout = QtWidgets.QHBoxLayout()
        self.fontCustomLayout.setSpacing(24)
        self.fontCustomLayout.setObjectName("fontCustomLayout")
        self.fontRadioCustom = QtWidgets.QRadioButton(self.boxFont)
        self.fontRadioCustom.setObjectName("fontRadioCustom")
        self.fontBtnGrp.addButton(self.fontRadioCustom)
        self.fontCustomLayout.addWidget(self.fontRadioCustom)
        self.fontListComboBox = QtWidgets.QFontComboBox(self.boxFont)
        self.fontListComboBox.setEnabled(False)
        self.fontListComboBox.setObjectName("fontListComboBox")
        self.fontCustomLayout.addWidget(self.fontListComboBox)
        self.fontCustomLayout.setStretch(1, 1)
        self.formLayout_10.setLayout(2, QtWidgets.QFormLayout.SpanningRole, self.fontCustomLayout)
        self.formLayout_11.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.boxFont)
        self.stackedWidget.addWidget(self.pageGeneral)
        self.pageAssets = QtWidgets.QWidget()
        self.pageAssets.setObjectName("pageAssets")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.pageAssets)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.boxNaming = QtWidgets.QGroupBox(self.pageAssets)
        self.boxNaming.setObjectName("boxNaming")
        self.formLayout_3 = QtWidgets.QFormLayout(self.boxNaming)
        self.formLayout_3.setObjectName("formLayout_3")
        self.maxCharLayout = QtWidgets.QFormLayout()
        self.maxCharLayout.setObjectName("maxCharLayout")
        self.maxCharLabel = QtWidgets.QLabel(self.boxNaming)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.maxCharLabel.sizePolicy().hasHeightForWidth())
        self.maxCharLabel.setSizePolicy(sizePolicy)
        self.maxCharLabel.setObjectName("maxCharLabel")
        self.maxCharLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.maxCharLabel)
        self.maxCharSpinner = QtWidgets.QSpinBox(self.boxNaming)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.maxCharSpinner.sizePolicy().hasHeightForWidth())
        self.maxCharSpinner.setSizePolicy(sizePolicy)
        self.maxCharSpinner.setMinimum(3)
        self.maxCharSpinner.setObjectName("maxCharSpinner")
        self.maxCharLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.maxCharSpinner)
        self.formLayout_3.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.maxCharLayout)
        self.separatorLayout = QtWidgets.QFormLayout()
        self.separatorLayout.setObjectName("separatorLayout")
        self.separatorLabel = QtWidgets.QLabel(self.boxNaming)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.separatorLabel.sizePolicy().hasHeightForWidth())
        self.separatorLabel.setSizePolicy(sizePolicy)
        self.separatorLabel.setObjectName("separatorLabel")
        self.separatorLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.separatorLabel)
        self.separatorCombo = QtWidgets.QComboBox(self.boxNaming)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.separatorCombo.sizePolicy().hasHeightForWidth())
        self.separatorCombo.setSizePolicy(sizePolicy)
        self.separatorCombo.setMaximumSize(QtCore.QSize(120, 16777215))
        self.separatorCombo.setObjectName("separatorCombo")
        self.separatorCombo.addItem("")
        self.separatorCombo.addItem("")
        self.separatorLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.separatorCombo)
        self.formLayout_3.setLayout(1, QtWidgets.QFormLayout.LabelRole, self.separatorLayout)
        self.boxPrefix = QtWidgets.QGroupBox(self.boxNaming)
        self.boxPrefix.setCheckable(True)
        self.boxPrefix.setObjectName("boxPrefix")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.boxPrefix)
        self.verticalLayout.setObjectName("verticalLayout")
        self.prefixRadioFirst = QtWidgets.QRadioButton(self.boxPrefix)
        self.prefixRadioFirst.setChecked(True)
        self.prefixRadioFirst.setObjectName("prefixRadioFirst")
        self.prefixBtnGrp = QtWidgets.QButtonGroup(PrefsDialog)
        self.prefixBtnGrp.setObjectName("prefixBtnGrp")
        self.prefixBtnGrp.addButton(self.prefixRadioFirst)
        self.verticalLayout.addWidget(self.prefixRadioFirst)
        self.prefixRadioWhole = QtWidgets.QRadioButton(self.boxPrefix)
        self.prefixRadioWhole.setChecked(False)
        self.prefixRadioWhole.setObjectName("prefixRadioWhole")
        self.prefixBtnGrp.addButton(self.prefixRadioWhole)
        self.verticalLayout.addWidget(self.prefixRadioWhole)
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.boxPrefix)
        self.boxSuffix = QtWidgets.QGroupBox(self.boxNaming)
        self.boxSuffix.setCheckable(True)
        self.boxSuffix.setChecked(True)
        self.boxSuffix.setObjectName("boxSuffix")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.boxSuffix)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.suffixVersionLayout = QtWidgets.QFormLayout()
        self.suffixVersionLayout.setObjectName("suffixVersionLayout")
        self.suffixRadioVersion = QtWidgets.QRadioButton(self.boxSuffix)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.suffixRadioVersion.sizePolicy().hasHeightForWidth())
        self.suffixRadioVersion.setSizePolicy(sizePolicy)
        self.suffixRadioVersion.setChecked(True)
        self.suffixRadioVersion.setObjectName("suffixRadioVersion")
        self.suffixBtnGrp = QtWidgets.QButtonGroup(PrefsDialog)
        self.suffixBtnGrp.setObjectName("suffixBtnGrp")
        self.suffixBtnGrp.addButton(self.suffixRadioVersion)
        self.suffixVersionLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.suffixRadioVersion)
        self.suffixVersionCombo = QtWidgets.QComboBox(self.boxSuffix)
        self.suffixVersionCombo.setMaximumSize(QtCore.QSize(120, 16777215))
        self.suffixVersionCombo.setObjectName("suffixVersionCombo")
        self.suffixVersionCombo.addItem("")
        self.suffixVersionCombo.addItem("")
        self.suffixVersionLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.suffixVersionCombo)
        self.verticalLayout_2.addLayout(self.suffixVersionLayout)
        self.suffixCustomLayout = QtWidgets.QHBoxLayout()
        self.suffixCustomLayout.setObjectName("suffixCustomLayout")
        self.suffixRadioCustomName = QtWidgets.QRadioButton(self.boxSuffix)
        self.suffixRadioCustomName.setObjectName("suffixRadioCustomName")
        self.suffixBtnGrp.addButton(self.suffixRadioCustomName)
        self.suffixCustomLayout.addWidget(self.suffixRadioCustomName)
        self.suffixCustomName = QtWidgets.QLineEdit(self.boxSuffix)
        self.suffixCustomName.setEnabled(False)
        self.suffixCustomName.setObjectName("suffixCustomName")
        self.suffixCustomLayout.addWidget(self.suffixCustomName)
        self.verticalLayout_2.addLayout(self.suffixCustomLayout)
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.boxSuffix)
        self.verticalLayout_3.addWidget(self.boxNaming)
        self.boxCategory = QtWidgets.QGroupBox(self.pageAssets)
        self.boxCategory.setObjectName("boxCategory")
        self.formLayout_4 = QtWidgets.QFormLayout(self.boxCategory)
        self.formLayout_4.setObjectName("formLayout_4")
        self.categoryBtnLayout = QtWidgets.QFormLayout()
        self.categoryBtnLayout.setObjectName("categoryBtnLayout")
        self.categoryBtnAdd = QtWidgets.QPushButton(self.boxCategory)
        self.categoryBtnAdd.setObjectName("categoryBtnAdd")
        self.categoryBtnLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.categoryBtnAdd)
        self.categoryBtnRemove = QtWidgets.QPushButton(self.boxCategory)
        self.categoryBtnRemove.setObjectName("categoryBtnRemove")
        self.categoryBtnLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.categoryBtnRemove)
        self.formLayout_4.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.categoryBtnLayout)
        self.categoryList = QtWidgets.QListWidget(self.boxCategory)
        self.categoryList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.categoryList.setObjectName("categoryList")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.categoryList)
        self.verticalLayout_3.addWidget(self.boxCategory)
        self.boxSubfolder = QtWidgets.QGroupBox(self.pageAssets)
        self.boxSubfolder.setObjectName("boxSubfolder")
        self.formLayout_5 = QtWidgets.QFormLayout(self.boxSubfolder)
        self.formLayout_5.setObjectName("formLayout_5")
        self.subfolderBtnLayout = QtWidgets.QFormLayout()
        self.subfolderBtnLayout.setObjectName("subfolderBtnLayout")
        self.subfolderBtnAdd = QtWidgets.QPushButton(self.boxSubfolder)
        self.subfolderBtnAdd.setObjectName("subfolderBtnAdd")
        self.subfolderBtnLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.subfolderBtnAdd)
        self.subfolderBtnRemove = QtWidgets.QPushButton(self.boxSubfolder)
        self.subfolderBtnRemove.setObjectName("subfolderBtnRemove")
        self.subfolderBtnLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.subfolderBtnRemove)
        self.formLayout_5.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.subfolderBtnLayout)
        self.subfolderList = QtWidgets.QListWidget(self.boxSubfolder)
        self.subfolderList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.subfolderList.setObjectName("subfolderList")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.subfolderList)
        self.verticalLayout_3.addWidget(self.boxSubfolder)
        self.stackedWidget.addWidget(self.pageAssets)
        self.pageAdvanced = QtWidgets.QWidget()
        self.pageAdvanced.setObjectName("pageAdvanced")
        self.formLayout_9 = QtWidgets.QFormLayout(self.pageAdvanced)
        self.formLayout_9.setObjectName("formLayout_9")
        self.boxLog = QtWidgets.QGroupBox(self.pageAdvanced)
        self.boxLog.setObjectName("boxLog")
        self.formLayout_6 = QtWidgets.QFormLayout(self.boxLog)
        self.formLayout_6.setObjectName("formLayout_6")
        self.logDebugCheck = QtWidgets.QCheckBox(self.boxLog)
        self.logDebugCheck.setObjectName("logDebugCheck")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.logDebugCheck)
        self.logDivider2 = QtWidgets.QFrame(self.boxLog)
        self.logDivider2.setFrameShape(QtWidgets.QFrame.HLine)
        self.logDivider2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.logDivider2.setObjectName("logDivider2")
        self.formLayout_6.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.logDivider2)
        self.logDebugWarning = QtWidgets.QLabel(self.boxLog)
        self.logDebugWarning.setObjectName("logDebugWarning")
        self.formLayout_6.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.logDebugWarning)
        self.logDivider1 = QtWidgets.QFrame(self.boxLog)
        self.logDivider1.setFrameShape(QtWidgets.QFrame.HLine)
        self.logDivider1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.logDivider1.setObjectName("logDivider1")
        self.formLayout_6.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.logDivider1)
        self.logButtonLayout = QtWidgets.QHBoxLayout()
        self.logButtonLayout.setObjectName("logButtonLayout")
        self.logButtonOpen = QtWidgets.QPushButton(self.boxLog)
        self.logButtonOpen.setObjectName("logButtonOpen")
        self.logButtonLayout.addWidget(self.logButtonOpen)
        self.logButtonClear = QtWidgets.QPushButton(self.boxLog)
        self.logButtonClear.setObjectName("logButtonClear")
        self.logButtonLayout.addWidget(self.logButtonClear)
        self.formLayout_6.setLayout(4, QtWidgets.QFormLayout.LabelRole, self.logButtonLayout)
        self.formLayout_9.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.boxLog)
        self.boxColumnView = QtWidgets.QGroupBox(self.pageAdvanced)
        self.boxColumnView.setObjectName("boxColumnView")
        self.formLayout_8 = QtWidgets.QFormLayout(self.boxColumnView)
        self.formLayout_8.setObjectName("formLayout_8")
        self.boxPreview = QtWidgets.QGroupBox(self.boxColumnView)
        self.boxPreview.setObjectName("boxPreview")
        self.formLayout_7 = QtWidgets.QFormLayout(self.boxPreview)
        self.formLayout_7.setObjectName("formLayout_7")
        self.previewHelpLabel = QtWidgets.QLabel(self.boxPreview)
        self.previewHelpLabel.setObjectName("previewHelpLabel")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.previewHelpLabel)
        self.previewLayout = QtWidgets.QVBoxLayout()
        self.previewLayout.setObjectName("previewLayout")
        self.previewRadioSmall = QtWidgets.QRadioButton(self.boxPreview)
        self.previewRadioSmall.setChecked(True)
        self.previewRadioSmall.setObjectName("previewRadioSmall")
        self.previewBtnGrp = QtWidgets.QButtonGroup(PrefsDialog)
        self.previewBtnGrp.setObjectName("previewBtnGrp")
        self.previewBtnGrp.addButton(self.previewRadioSmall)
        self.previewLayout.addWidget(self.previewRadioSmall)
        self.previewRadioBig = QtWidgets.QRadioButton(self.boxPreview)
        self.previewRadioBig.setObjectName("previewRadioBig")
        self.previewBtnGrp.addButton(self.previewRadioBig)
        self.previewLayout.addWidget(self.previewRadioBig)
        self.previewCustomLayout = QtWidgets.QHBoxLayout()
        self.previewCustomLayout.setObjectName("previewCustomLayout")
        self.previewRadioCustom = QtWidgets.QRadioButton(self.boxPreview)
        self.previewRadioCustom.setObjectName("previewRadioCustom")
        self.previewBtnGrp.addButton(self.previewRadioCustom)
        self.previewCustomLayout.addWidget(self.previewRadioCustom)
        self.previewSpinnerCustom = QtWidgets.QSpinBox(self.boxPreview)
        self.previewSpinnerCustom.setEnabled(False)
        self.previewSpinnerCustom.setMinimum(150)
        self.previewSpinnerCustom.setMaximum(1000)
        self.previewSpinnerCustom.setObjectName("previewSpinnerCustom")
        self.previewCustomLayout.addWidget(self.previewSpinnerCustom)
        self.previewLayout.addLayout(self.previewCustomLayout)
        self.formLayout_7.setLayout(1, QtWidgets.QFormLayout.LabelRole, self.previewLayout)
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.boxPreview)
        self.boxIcon = QtWidgets.QGroupBox(self.boxColumnView)
        self.boxIcon.setObjectName("boxIcon")
        self.formLayout_2 = QtWidgets.QFormLayout(self.boxIcon)
        self.formLayout_2.setObjectName("formLayout_2")
        self.iconRadioLayout = QtWidgets.QVBoxLayout()
        self.iconRadioLayout.setObjectName("iconRadioLayout")
        self.iconRadioEnable = QtWidgets.QRadioButton(self.boxIcon)
        self.iconRadioEnable.setChecked(True)
        self.iconRadioEnable.setObjectName("iconRadioEnable")
        self.iconBtnGrp = QtWidgets.QButtonGroup(PrefsDialog)
        self.iconBtnGrp.setObjectName("iconBtnGrp")
        self.iconBtnGrp.addButton(self.iconRadioEnable)
        self.iconRadioLayout.addWidget(self.iconRadioEnable)
        self.iconRadioDisable = QtWidgets.QRadioButton(self.boxIcon)
        self.iconRadioDisable.setChecked(False)
        self.iconRadioDisable.setObjectName("iconRadioDisable")
        self.iconBtnGrp.addButton(self.iconRadioDisable)
        self.iconRadioLayout.addWidget(self.iconRadioDisable)
        self.iconRadioGeneric = QtWidgets.QRadioButton(self.boxIcon)
        self.iconRadioGeneric.setMaximumSize(QtCore.QSize(331, 16777215))
        self.iconRadioGeneric.setChecked(False)
        self.iconRadioGeneric.setObjectName("iconRadioGeneric")
        self.iconBtnGrp.addButton(self.iconRadioGeneric)
        self.iconRadioLayout.addWidget(self.iconRadioGeneric)
        self.formLayout_2.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.iconRadioLayout)
        self.formLayout_8.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.boxIcon)
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.boxColumnView)
        self.stackedWidget.addWidget(self.pageAdvanced)
        self.gridLayout.addWidget(self.stackedWidget, 4, 1, 1, 1)

        self.retranslateUi(PrefsDialog)
        self.stackedWidget.setCurrentIndex(1)
        self.sideList.currentRowChanged['int'].connect(self.stackedWidget.setCurrentIndex)
        self.suffixRadioVersion.toggled['bool'].connect(self.suffixVersionCombo.setEnabled)
        self.previewRadioCustom.toggled['bool'].connect(self.previewSpinnerCustom.setEnabled)
        self.fontRadioCustom.toggled['bool'].connect(self.fontListComboBox.setEnabled)
        self.suffixRadioCustomName.toggled['bool'].connect(self.suffixCustomName.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(PrefsDialog)

    def retranslateUi(self, PrefsDialog):
        _translate = QtCore.QCoreApplication.translate
        PrefsDialog.setWindowTitle(_translate("PrefsDialog", "Preferences"))
        __sortingEnabled = self.sideList.isSortingEnabled()
        self.sideList.setSortingEnabled(False)
        item = self.sideList.item(0)
        item.setText(_translate("PrefsDialog", "General"))
        item = self.sideList.item(1)
        item.setText(_translate("PrefsDialog", "Assets"))
        item = self.sideList.item(2)
        item.setText(_translate("PrefsDialog", "Advanced"))
        self.sideList.setSortingEnabled(__sortingEnabled)
        self.projectPathLabel.setText(_translate("PrefsDialog", "Project Path:"))
        self.projectPathLine.setToolTip(_translate("PrefsDialog", "Insert your project path here. E.g. \"P:/\", \"media/projects\""))
        self.projectPathTool.setToolTip(_translate("PrefsDialog", "Choose directory"))
        self.projectPathTool.setText(_translate("PrefsDialog", "..."))
        self.descCheck.setToolTip(_translate("PrefsDialog", "Display description for assets."))
        self.descCheck.setText(_translate("PrefsDialog", "Show Description Panel"))
        self.boxTheme.setTitle(_translate("PrefsDialog", "Theme"))
        self.themeRadioLight.setToolTip(_translate("PrefsDialog", "Fusion Style"))
        self.themeRadioLight.setText(_translate("PrefsDialog", "Default (Light)"))
        self.themeRadioDark.setToolTip(_translate("PrefsDialog", "QDarkStyle"))
        self.themeRadioDark.setText(_translate("PrefsDialog", "Dark"))
        self.boxFont.setTitle(_translate("PrefsDialog", "Font"))
        self.fontRadioDefault.setText(_translate("PrefsDialog", "Default (Sans Serif)"))
        self.fontRadioMonospace.setText(_translate("PrefsDialog", "Monospace"))
        self.fontSizeLabel.setText(_translate("PrefsDialog", "Size:"))
        self.fontSizeComboBox.setItemText(0, _translate("PrefsDialog", "Default"))
        self.fontSizeComboBox.setItemText(1, _translate("PrefsDialog", "Tiny"))
        self.fontSizeComboBox.setItemText(2, _translate("PrefsDialog", "Large"))
        self.fontRadioCustom.setToolTip(_translate("PrefsDialog", "Select font that best suited to your project locale and language"))
        self.fontRadioCustom.setText(_translate("PrefsDialog", "Custom font"))
        self.boxNaming.setTitle(_translate("PrefsDialog", "Naming Convention"))
        self.maxCharLabel.setText(_translate("PrefsDialog", "Max characters:"))
        self.maxCharSpinner.setToolTip(_translate("PrefsDialog", "Min: 3, Max: 99"))
        self.separatorLabel.setText(_translate("PrefsDialog", "Separator:"))
        self.separatorCombo.setItemText(0, _translate("PrefsDialog", " _ (underscore)"))
        self.separatorCombo.setItemText(1, _translate("PrefsDialog", " - (dash)"))
        self.boxPrefix.setTitle(_translate("PrefsDialog", "Prefix"))
        self.prefixRadioFirst.setText(_translate("PrefsDialog", "Use first character of category (e.g.: p)"))
        self.prefixRadioWhole.setText(_translate("PrefsDialog", "Use whole category (e.g.: props)"))
        self.boxSuffix.setTitle(_translate("PrefsDialog", "Suffix"))
        self.suffixRadioVersion.setText(_translate("PrefsDialog", "Use versioning (v):"))
        self.suffixVersionCombo.setItemText(0, _translate("PrefsDialog", "lowercase (v001)"))
        self.suffixVersionCombo.setItemText(1, _translate("PrefsDialog", "UPPERCASE (V001)"))
        self.suffixRadioCustomName.setText(_translate("PrefsDialog", "Use custom naming:"))
        self.boxCategory.setTitle(_translate("PrefsDialog", "Categories"))
        self.categoryBtnAdd.setText(_translate("PrefsDialog", "Add"))
        self.categoryBtnRemove.setText(_translate("PrefsDialog", "Remove"))
        self.boxSubfolder.setTitle(_translate("PrefsDialog", "Subfolders"))
        self.subfolderBtnAdd.setText(_translate("PrefsDialog", "Add"))
        self.subfolderBtnRemove.setText(_translate("PrefsDialog", "Remove"))
        self.boxLog.setTitle(_translate("PrefsDialog", "Logs"))
        self.logDebugCheck.setToolTip(_translate("PrefsDialog", "Log file will include debug statement. Useful for troubleshooting."))
        self.logDebugCheck.setText(_translate("PrefsDialog", "Enable Debug Log"))
        self.logDebugWarning.setText(_translate("PrefsDialog", "WARNING: Debug log will result in bigger log file size!"))
        self.logButtonOpen.setToolTip(_translate("PrefsDialog", "Clear current log contents"))
        self.logButtonOpen.setText(_translate("PrefsDialog", "Open Log Location"))
        self.logButtonClear.setToolTip(_translate("PrefsDialog", "Clear current log contents"))
        self.logButtonClear.setText(_translate("PrefsDialog", "Clear Log"))
        self.boxColumnView.setTitle(_translate("PrefsDialog", "Column View"))
        self.boxPreview.setTitle(_translate("PrefsDialog", "Preview"))
        self.previewHelpLabel.setText(_translate("PrefsDialog", "Preview size for supported images"))
        self.previewRadioSmall.setToolTip(_translate("PrefsDialog", "150px"))
        self.previewRadioSmall.setText(_translate("PrefsDialog", "Small"))
        self.previewRadioBig.setToolTip(_translate("PrefsDialog", "300px"))
        self.previewRadioBig.setText(_translate("PrefsDialog", "Big"))
        self.previewRadioCustom.setToolTip(_translate("PrefsDialog", "Valid range: 150 to 1000"))
        self.previewRadioCustom.setText(_translate("PrefsDialog", "Custom max size:"))
        self.boxIcon.setTitle(_translate("PrefsDialog", "Icon Thumbnails"))
        self.iconRadioEnable.setToolTip(_translate("PrefsDialog", "Default. Performance hit when navigating directory with lots of supported images."))
        self.iconRadioEnable.setText(_translate("PrefsDialog", "Enable"))
        self.iconRadioDisable.setToolTip(_translate("PrefsDialog", "No icons display in Column View. Fastest performance."))
        self.iconRadioDisable.setText(_translate("PrefsDialog", "Disable (fastest)"))
        self.iconRadioGeneric.setToolTip(_translate("PrefsDialog", "Display generic icons by disabling icon thumbnail generation for supported images."))
        self.iconRadioGeneric.setText(_translate("PrefsDialog", "Use generic icons"))

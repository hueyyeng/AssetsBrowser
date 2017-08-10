# -*- coding: utf-8 -*-
import os
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from ui import ui_main
from modules import functions
from modules import assetDialog
from modules import aboutDialog
from modules import prefsDialog
from modules import prefsConfig

# Set Project Path from INI file
projectPath = prefsDialog.projpath

# Path to executable script
# FILEPATH = os.path.abspath(__file__)


class AssetsBrowser(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, parent = None):
        super(AssetsBrowser, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/logo.ico'))
        self.setWindowTitle('Assets Browser [PID: %d]' % QtGui.QApplication.applicationPid())

        # Install the custom output stream for debug log
        sys.stdout = functions.EmittingStream(textWritten = self.debug_stdout)

        # Initialise the chosen theme from INI file
        theme = prefsConfig.get_setting(prefsConfig.INI_PATH, 'UI', 'Theme')
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(theme))

        # Create New Asset Button
        self.pushBtnNew.clicked.connect(self.showAssetDialog)

        # Show Debug CheckBox and Disabled the Debug textEdit
        self.checkBoxDebug.clicked.connect(lambda: functions.show_debug(self))

        self.textEdit.setVisible(False)

        # Project List Dropdown ComboBox
        self.comboBox.fsm = QtGui.QFileSystemModel()
        self.comboBox.rootindex = self.comboBox.fsm.setRootPath(projectPath)

        self.comboBox.setModel(self.comboBox.fsm)
        self.comboBox.setRootModelIndex(self.comboBox.rootindex)
        self.comboBox.setCurrentIndex(0)
        self.comboBox.activated[str].connect(lambda: functions.project_list(self))

        # -----------------------------------------------------------------------------

        # Menu Action
        self.actionPreferences.triggered.connect(self.showPrefsDialog)
        self.actionAbout.triggered.connect(self.showAboutDialog)
        self.actionQuit.triggered.connect(functions.close_app)

        # When calling functions from imported modules that inherit the QMainWindow
        # but located outside its scope, use 'lambda:' followed by the function to
        # as though it was defined within the same class for easier code maintenance
        self.actionAlwaysOnTop.triggered.connect(lambda: functions.always_on_top(self))

        # -----------------------------------------------------------------------------

        # Ensure external attributes are explicitly defined in __init__
        self.window = None

        # -----------------------------------------------------------------------------

        # Create ColumnView Tabs using columnview_tabs function
        self.columnview_tabs(self.columnViewBG, 'BG')
        self.columnview_tabs(self.columnViewCH, 'CH')
        self.columnview_tabs(self.columnViewFX, 'FX')
        
    # Function for creating new ColumnView tab to reduce DRY for categories
    def columnview_tabs(self, columnview, category):

        # Select top most project from Project comboBox as default project
        projectName = (os.listdir(projectPath))[0]
        defaultpath = (projectPath + projectName + "/Assets/" + category)

        print defaultpath
        
        tab = columnview

        tab.fsm = QtGui.QFileSystemModel()
        tab.fsm.setReadOnly(False)

        tab.rootindex = tab.fsm.setRootPath(defaultpath)

        tab.setModel(tab.fsm)
        tab.setRootIndex(tab.rootindex)

        # Return selected item attributes in Model View for Preview Pane
        @QtCore.pyqtSlot(QtCore.QModelIndex)
        def get_fileinfo(index):
            indexItem = tab.fsm.index(index.row(), 0, index.parent())

            # Retrieve File Attributes
            fileName = str(tab.fsm.fileName(indexItem))
            fileSize = tab.fsm.size(indexItem)
            fileType = str(tab.fsm.type(indexItem))
            fileDate = tab.fsm.lastModified(indexItem)

            # Format the File Attributes into String
            fileNameLabel = fileName
            fileSizeLabel = functions.get_filesize(fileSize)
            fileTypeLabel = fileType.upper()  # Convert fileType to UPPERCASE
            fileDateLabel = fileDate.toString('yyyy/MM/dd' + ' ' + 'h:m AP')

            # Assign the File Attributes' String into respective labels
            tab.filename.setText(fileNameLabel)
            tab.filesize.setText(fileSizeLabel)
            tab.filetype.setText(fileTypeLabel)
            tab.filedate.setText(fileDateLabel)

            # For Debug Panel (feel free to comment/remove it)
            print fileNameLabel
            print fileSizeLabel
            print fileTypeLabel
            print fileDateLabel

            # Retrieve filePath for Thumbnail Preview in __init__
            picPath = tab.fsm.filePath(indexItem)
            picType = fileType[0:-5]

            picTypes = ['jpg', 'jpeg', 'bmp', 'png', 'gif', 'bmp', 'ico', 'tga', 'tif', 'tiff']

            # Generate thumbnails for Preview Pane
            for each in picTypes:
                if each.lower() == picType.lower():
                    max_size = 250  # Thumbnails max size in pixels

                    tb = QtGui.QPixmap(picPath)
                    tb_scaled = tb.scaled(max_size, max_size,
                                          QtCore.Qt.KeepAspectRatio,
                                          QtCore.Qt.SmoothTransformation)

                    tab.pvThumbs.setPixmap(tb_scaled)
                    break
                else:
                    fileInfo = QtCore.QFileInfo(picPath)  # Retrieve info like icons, path, etc
                    fileIcon = QtGui.QFileIconProvider().icon(fileInfo)
                    icon = fileIcon.pixmap(128, 128, QtGui.QIcon.Normal, QtGui.QIcon.On)

                    tab.pvThumbs.setPixmap(icon)

        # When an item clicked in the columnView tab, execute get_fileinfo method
        tab.clicked.connect(get_fileinfo)

        # Preview widget layout and features goes here as a function
        def preview(previewWidget, tab):

            # -------------------- TEXT LABELS STARTS HERE -------------------- #

            # File Category Labels
            catName = QtGui.QLabel('Name: ')
            catSize = QtGui.QLabel('Size: ')
            catType = QtGui.QLabel('Type: ')
            catDate = QtGui.QLabel('Modified: ')

            # File Attributes Labels
            tab.filename = QtGui.QLabel()
            tab.filesize = QtGui.QLabel()
            tab.filetype = QtGui.QLabel()
            tab.filedate = QtGui.QLabel()

            # Align Right for Prefix Labels
            align_right = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter

            catName.setAlignment(align_right)
            catSize.setAlignment(align_right)
            catType.setAlignment(align_right)
            catDate.setAlignment(align_right)

            # File Attributes Layout
            sublayout_text = QtGui.QGridLayout()

            sublayout_text.addWidget(catName, 0, 0)
            sublayout_text.addWidget(catSize, 1, 0)
            sublayout_text.addWidget(catType, 2, 0)
            sublayout_text.addWidget(catDate, 3, 0)

            # File Attributes Value for Preview Pane
            sublayout_text.addWidget(tab.filename, 0, 1)
            sublayout_text.addWidget(tab.filesize, 1, 1)
            sublayout_text.addWidget(tab.filetype, 2, 1)
            sublayout_text.addWidget(tab.filedate, 3, 1)

            # Arrange layout to upper part of widget
            sublayout_text.setRowStretch(4, 1)

            # -------------------- THUMBNAILS STARTS HERE -------------------- #

            # Preview Thumbnails (pvThumbs) WIP
            tab.pvThumbs = QtGui.QLabel()
            tab.pvThumbs.setPixmap(QtGui.QPixmap())

            sublayout_pic = QtGui.QVBoxLayout()
            sublayout_pic.addWidget(tab.pvThumbs)
            sublayout_pic.setAlignment(QtCore.Qt.AlignCenter)

            # -------------------- PREVIEW PANE STARTS HERE -------------------- #

            # Set Preview Pane to QColumnView setPreviewWidget
            preview_pane = QtGui.QVBoxLayout(previewWidget)
            preview_pane.addLayout(sublayout_pic)
            preview_pane.addLayout(sublayout_text)

            tab.setPreviewWidget(previewWidget)

        previewWidget = QtGui.QWidget()
        preview(previewWidget, tab)

    def showAboutDialog(self):
        self.window = aboutDialog.About()
        self.window.exec_()

    def showPrefsDialog(self):
        self.window = prefsDialog.Prefs()
        spam = self.window.exec_()

        # If OK, restart app to reinitialize new INI settings
        if spam:
            functions.restart_app()

    def showAssetDialog(self):
        self.window = assetDialog.AssetDialog()
        spam = self.window.exec_()

        # If Create, execute spam to create the new asset folders
        if spam:
            asset_name = self.window.create_asset()
            path_asset = functions.project_list(self)
            functions.createdir_asset(path_asset, asset_name)

            print 'Creating ' + asset_name + ' asset...'
        else:
            print 'Aborting Create New Asset...'

    def __del__(self):
        # Restore sys.stdout for debug log
        sys.stdout = sys.__stdout__

    def debug_stdout(self, text):
        # Append stdout to the QTextEdit for debug log
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()


if __name__ == "__main__":
    app = QtGui.QApplication.instance()
    if app is None:
        app = QtGui.QApplication(sys.argv)
    else:
        print('QApplication instance already exists: %s' % str(app))

    window = AssetsBrowser()
    window.show()
    sys.exit(app.exec_())


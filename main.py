# -*- coding: utf-8 -*-
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
        self.fsm = QtGui.QFileSystemModel()
        rootindex = self.fsm.setRootPath(projectPath)

        self.comboBox.setModel(self.fsm)
        self.comboBox.setRootModelIndex(rootindex)
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

        # List for Column Width for QColumnView
        colwidth = [150, 150, 150]

        # Ensure external attributes are defined in __init__
        self.columnView = None
        self.fsm = None
        self.window = None

        # Create ColumnView Tabs using columnview_tab function
        BG = self.columnViewBG
        CH = self.columnViewCH
        FX = self.columnViewFX

        BG.setColumnWidths(colwidth)
        CH.setColumnWidths(colwidth)
        FX.setColumnWidths(colwidth)

        self.columnview_tab(BG)
        self.columnview_tab(CH)
        # self.columnview_tab(FX)
        # ^ FX tab temporarily comment out for debugging

        # -----------------------------------------------------------------------------

        # previewWidget for QColumnView
        previewWidget = QtGui.QWidget()

        # TEXT LABELS STARTS HERE #
        
        # File Category Labels
        catName = QtGui.QLabel('Name: ')
        catSize = QtGui.QLabel('Size: ')
        catType = QtGui.QLabel('Type: ')
        catDate = QtGui.QLabel('Modified: ')

        # File Attributes Labels
        self.filename = QtGui.QLabel()  # To access variables between methods BUT in
        self.filesize = QtGui.QLabel()  # the same class, put the prefix self e.g.
        self.filetype = QtGui.QLabel()  # (self.varnamehere) instead of (varnamehere)
        self.filedate = QtGui.QLabel()  # so the value can be updated in another method
  #
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
        sublayout_text.addWidget(self.filename, 0, 1)
        sublayout_text.addWidget(self.filesize, 1, 1)
        sublayout_text.addWidget(self.filetype, 2, 1)
        sublayout_text.addWidget(self.filedate, 3, 1)

        # Arrange layout to upper part of widget
        sublayout_text.setRowStretch(4, 1)
        
        # TEXT LABELS ENDS HERE #

        # --------------------- #

        # THUMBNAILS START HERE #
        
        # Preview Thumbnails (pvThumbs) WIP
        self.pvThumbs = QtGui.QLabel()
        # self.pvThumbs.setPixmap(QtGui.QPixmap())

        sublayout_pic = QtGui.QVBoxLayout()
        sublayout_pic.addWidget(self.pvThumbs)
        sublayout_pic.setAlignment(QtCore.Qt.AlignCenter)
        
        # THUMBNAILS ENDS HERE #

        # -------------------- #

        # Set Preview Pane to QColumnView setPreviewWidget
        preview_pane = QtGui.QVBoxLayout(previewWidget)
        preview_pane.addLayout(sublayout_pic)
        preview_pane.addLayout(sublayout_text)
        
        CH.setPreviewWidget(previewWidget)

        # -----------------------------------------------------------------------------

    # Function for creating new ColumnView tab to reduce DRY for several categories
    def columnview_tab(self, viewmode):
        self.columnView = viewmode

        self.fsm = QtGui.QFileSystemModel()
        self.fsm.setReadOnly(False)

        rootindex = self.fsm.setRootPath(projectPath)

        self.columnView.setModel(self.fsm)
        self.columnView.setRootIndex(rootindex)

        self.columnView.clicked.connect(self.columnview_clicked)

    # Return selected item attributes in Model View for Preview Pane
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def columnview_clicked(self, index):
        # Selected file/directory
        indexItem = self.fsm.index(index.row(), 0, index.parent())

        # Retrieve File Attributes
        fileName = str(self.fsm.fileName(indexItem))
        fileSize = self.fsm.size(indexItem)
        fileType = str(self.fsm.type(indexItem))
        fileDate = self.fsm.lastModified(indexItem)

        # Format the File Attributes into String
        fileNameLabel = fileName
        fileSizeLabel = functions.get_filesize(fileSize)
        fileTypeLabel = fileType.upper()  # Convert fileType to UPPERCASE
        fileDateLabel = fileDate.toString('yyyy/MM/dd' + ' ' + 'h:m AP')

        # Assign the File Attributes' String into respective labels
        self.filename.setText(fileNameLabel)
        self.filesize.setText(fileSizeLabel)
        self.filetype.setText(fileTypeLabel)
        self.filedate.setText(fileDateLabel)

        # For Debug Panel (feel free to comment/remove it)
        print fileNameLabel
        print fileSizeLabel
        print fileTypeLabel
        print fileDateLabel

        # Retrieve filePath for Thumbnail Preview in __init__
        picPath = self.fsm.filePath(indexItem)
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

                self.pvThumbs.setPixmap(tb_scaled)
                break
            else:
                fileInfo = QtCore.QFileInfo(picPath)  # Retrieve info like icons, path, etc
                fileIcon = QtGui.QFileIconProvider().icon(fileInfo)
                icon = fileIcon.pixmap(128, 128, QtGui.QIcon.Normal, QtGui.QIcon.On)

                self.pvThumbs.setPixmap(icon)

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


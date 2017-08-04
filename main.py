# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from ui import ui_main
# from ui import ui_preview
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
    def __init__(self, parent = None, **kwargs):
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
        self.comboBox.activated[str].connect(self.comboProjectList)

        # -----------------------------------------------------------------------------

        # Menu Action
        self.actionPreferences.triggered.connect(self.showPrefsDialog)
        self.actionAbout.triggered.connect(self.showAboutDialog)
        self.actionQuit.triggered.connect(functions.close_app)

        # When we need to call a function from imported modules that inherit
        # the QMainWindow but located outside its scope, use 'lambda:'
        # followed by the function to allow for proper execution as though
        # it is defined within the same class for easier code maintenance
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

        # Preview Pane for QColumnView
        preview_pane = QtGui.QWidget()
        self.filename = QtGui.QLabel()
        self.filesize = QtGui.QLabel()
        self.filetype = QtGui.QLabel()
        self.filedate = QtGui.QLabel()

        preview_layout = QtGui.QGridLayout(preview_pane)
        preview_layout.addWidget(self.filename, 0, 0)
        preview_layout.addWidget(self.filesize, 1, 0)
        preview_layout.addWidget(self.filetype, 2, 0)
        preview_layout.addWidget(self.filedate, 3, 0)
        # preview_layout.setRowStretch(2, 1)

        CH.setPreviewWidget(preview_pane)

    # Function for creating new ColumnView tab to reduce copy paste codes for several categories
    def columnview_tab(self, viewmode):
        self.columnView = viewmode

        self.fsm = QtGui.QFileSystemModel()
        self.fsm.setReadOnly(False)

        rootindex = self.fsm.setRootPath(projectPath)

        self.columnView.setModel(self.fsm)
        self.columnView.setRootIndex(rootindex)

        self.columnView.clicked.connect(self.columnview_clicked)

    # Print selected item attributes in Model View
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def columnview_clicked(self, index):
        indexItem = self.fsm.index(index.row(), 0, index.parent())

        fileName = str(self.fsm.fileName(indexItem))
        fileSize = self.fsm.size(indexItem)
        fileType = str(self.fsm.type(indexItem))
        fileDate = self.fsm.lastModified(indexItem)

        fileNameLabel = ('\n' + fileName)
        fileSizeLabel = functions.get_filesize(fileSize)
        fileTypeLabel = fileType
        fileDateLabel = fileDate.toString('yyyy/MM/dd')

        self.filename.setText(fileNameLabel)
        self.filesize.setText(fileSizeLabel)
        self.filetype.setText(fileTypeLabel)
        self.filedate.setText(fileDateLabel)

    # Choose from comboBox list of Projects that are defined in INI ProjectPath
    def comboProjectList(self):
        functions.project_list(self)

    def showAboutDialog(self):
        self.window = aboutDialog.About()
        self.window.exec_()

    def showPrefsDialog(self):
        self.window = prefsDialog.Prefs()
        spam = self.window.exec_()

        # When OK, restart app to reinitialize new INI settings
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


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

        # Initialise the chosen theme from INI file
        theme = prefsConfig.get_setting(prefsConfig.INI_PATH, 'UI', 'Theme')
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(theme))

        # Declare var that are only used outside of __init__
        self.window = ''

        # Create New Asset Button
        self.pushBtnNew.clicked.connect(self.showAssetDialog)

        # Show Debug CheckBox
        self.checkBoxDebug.clicked.connect(functions.show_debug)

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

        # Create ColumnView Tabs using columnview_tab function
        BG = self.columnViewBG
        CH = self.columnViewCH
        FX = self.columnViewFX

        self.columnview_tab(BG)
        self.columnview_tab(CH)
        self.columnview_tab(FX)

    # Function for creating new ColumnView tab to reduce copy paste codes for several categories
    def columnview_tab(self, viewmode):
        self.columnView = viewmode

        self.fsm = QtGui.QFileSystemModel()             # self.itemview.model = QtGui.QFileSystemModel()
        self.fsm.setReadOnly(False)

        rootindex = self.fsm.setRootPath(projectPath)   # self.itemview.model.setRootPath( QtCore.QDir.currentPath() )

        self.columnView.setModel(self.fsm)              # self.itemview.setModel(self.itemview.model)
        self.columnView.setRootIndex(rootindex)

        self.columnView.clicked.connect(self.columnview_clicked)

    # Print selected item attributes in Model View
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def columnview_clicked(self, index):
        indexItem = self.fsm.index(index.row(), 0, index.parent())
        fileName = self.fsm.fileName(indexItem)
        # fileInfo = self.fsm.filePath(indexItem)

        print fileName
        # print fileInfo

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
            egg = self.window.create_asset()
            print 'Creating ' + egg + ' asset... NOT!'
        else:
            print 'Aborting Create New Asset...'


if __name__ == "__main__":
    app = QtGui.QApplication.instance()
    if app is None:
        app = QtGui.QApplication(sys.argv)
    else:
        print('QApplication instance already exists: %s' % str(app))

    window = AssetsBrowser()
    window.show()
    sys.exit(app.exec_())


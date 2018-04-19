# -*- coding: utf-8 -*-
import os
import sys
from ui import ui_main
from ui import ui_help
from modules import functions
from modules import assetDialog
from modules import aboutDialog
from modules import prefsDialog
from modules import prefsConfig
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets


# Set Project Path from INI file
CURRENTPROJECT = prefsConfig.CURRENTPROJECT
PROJECTPATH = prefsConfig.PROJECTPATH
INI_PATH = prefsConfig.INI_PATH
THEME = prefsConfig.THEME


class AssetsBrowser(QtWidgets.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, parent=None):
        super(AssetsBrowser, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Assets Browser [PID: %d]' % QtWidgets.QApplication.applicationPid())
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint)
        functions.window_icon(self)

        # -----------------------------------------------------------------------------

        # Redirect stdout to QTextEdit widget for debug log
        sys.stdout = functions.OutLog(self.textEdit, sys.stdout)
        sys.stderr = functions.OutLog(self.textEdit, sys.stderr, QtGui.QColor(255, 0, 0))

        # functions.font_overrides(self)
        QtWidgets.QApplication.setStyle(THEME)  # Initialise theme from INI file

        # In case it doesn't center on screen properly like in Lubuntu LXDE
        functions.center_screen(self)

        # -----------------------------------------------------------------------------

        # Project List Dropdown ComboBox
        self.comboBox.fsm = QtWidgets.QFileSystemModel()
        self.comboBox.rootindex = self.comboBox.fsm.setRootPath(PROJECTPATH)
        self.comboBox.setModel(self.comboBox.fsm)
        self.comboBox.setRootModelIndex(self.comboBox.rootindex)
        self.comboBox.setCurrentIndex(0)  # Set to top directory from PROJECTPATH
        self.comboBox.activated[str].connect(lambda: functions.project_list(self))

        projects = []

        for item in os.listdir(PROJECTPATH):
            if not item.startswith('.') and os.path.isdir(os.path.join(PROJECTPATH, item)):
                projects.append(item)

        # Use the first index of projects list as default project during app startup
        prefsConfig.update_setting(INI_PATH, 'Settings', 'CurrentProject', projects[0])

        # -----------------------------------------------------------------------------

        # Create list and dictionary for ColumnView tabs
        self.category = []  # List
        self.assets = {}  # Dictionary

        # Declare ASSETSPATH var to populate self.category list
        ASSETSPATH = (PROJECTPATH + CURRENTPROJECT + "/Assets/")

        for item in os.listdir(ASSETSPATH):
            if not item.startswith('_') and not item.startswith('.')\
                    and os.path.isdir(os.path.join(ASSETSPATH, item)):
                        self.category.append(item)

        # Generate Tabs using create_tabs
        functions.create_tabs(self)

        # -----------------------------------------------------------------------------

        # Splitter Size Config
        splitter_size = [150, 500]
        self.splitter.setSizes(splitter_size)

        # Help Tab
        html = 'ui/help/help.html'
        temp_path = 'file:///' + str(ui_help.help_repath(html))
        self.textBrowserHelp.setSource(QtCore.QUrl(temp_path))

        # Dialog Window
        about = aboutDialog.showAboutDialog
        asset = assetDialog.showAssetDialog
        prefs = prefsDialog.showPrefsDialog

        # Menu Action
        self.actionPreferences.triggered.connect(prefs)
        self.actionAbout.triggered.connect(about)
        self.actionQuit.triggered.connect(functions.close_app)

        # Create New Asset Button
        self.pushBtnNew.clicked.connect(asset)

        # When calling functions from imported modules that inherit the QMainWindow
        # but located outside its scope, use 'lambda:' followed by the function as
        # though it was defined within the same class for easier code maintenance
        self.actionAlwaysOnTop.triggered.connect(lambda: functions.always_on_top(self))

        # Show Debug CheckBox and Disabled the Debug textEdit
        self.checkBoxDebug.clicked.connect(lambda: functions.show_debug(self))
        self.textEdit.clear()
        self.textEdit.setHidden(True)
        self.textEdit.setEnabled(False)


if __name__ == "__main__":
    functions.highdpi_check()
    functions.setTaskbarIcon()

    validpath = functions.projectpath_is_valid(INI_PATH, PROJECTPATH)

    if validpath:
        app = QtWidgets.QApplication.instance()
        if app is None:
            app = QtWidgets.QApplication(sys.argv)
        else:
            print('QApplication instance already exists: %s' % str(app))

        window = AssetsBrowser()
        window.show()
        sys.exit(app.exec_())

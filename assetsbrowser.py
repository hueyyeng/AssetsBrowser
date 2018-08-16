# -*- coding: utf-8 -*-
import os
import sys
from config import configurations
from modules import functions
from ui import help
from ui.window import main
from ui.dialog import about, asset, preferences
from PyQt5 import QtGui, QtCore, QtWidgets

# Set Path from INI file
PROJECTPATH = configurations.PROJECTPATH
INI_PATH = configurations.INI_PATH
THEME = configurations.THEME


class AssetsBrowser(QtWidgets.QMainWindow, main.Ui_MainWindow):
    def __init__(self, parent=None):
        super(AssetsBrowser, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Assets Browser [PID: %d]' % QtWidgets.QApplication.applicationPid())
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint)
        functions.window_icon(self)

        # Redirect stdout to QTextEdit widget for debug log
        sys.stdout = functions.OutLog(self.textEdit, sys.stdout)
        sys.stderr = functions.OutLog(self.textEdit, sys.stderr, QtGui.QColor(255, 0, 0))

        # functions.font_overrides(self)
        QtWidgets.QApplication.setStyle(THEME)  # Initialise theme from INI file

        # In case it doesn't center on screen properly like in Lubuntu LXDE
        functions.center_screen(self)

        # Project List Dropdown ComboBox
        self.comboBox.fsm = QtWidgets.QFileSystemModel()
        self.comboBox.rootindex = self.comboBox.fsm.setRootPath(PROJECTPATH)
        self.comboBox.setModel(self.comboBox.fsm)
        self.comboBox.setRootModelIndex(self.comboBox.rootindex)
        self.comboBox.setCurrentIndex(1)
        self.comboBox.activated[str].connect(lambda: functions.project_list(self))

        projects = []
        for item in os.listdir(PROJECTPATH):
            if not item.startswith('.') and os.path.isdir(os.path.join(PROJECTPATH, item)):
                projects.append(item)
        configurations.update_setting(INI_PATH, 'Settings', 'CurrentProject', projects[0])
        current_project = configurations.current_project()

        # Create empty list and dictionary for ColumnView tabs
        # self.category = []
        self.assets = {}

        categories = self.category = []
        assets_path = (PROJECTPATH + current_project + "/Assets/")

        # Populate categories list of Assets folder
        for item in os.listdir(assets_path):
            name_prefix = item.startswith(('_', '.'))
            assets_directory = os.path.join(assets_path, item)
            if not name_prefix and os.path.isdir(assets_directory):
                categories.append(item)

        # Generate Tabs using create_tabs
        functions.create_tabs(self, categories, current_project)

        # Splitter Size Config
        splitter_size = [150, 500]
        self.splitter.setSizes(splitter_size)

        # Help Tab
        html = 'ui/help/help.html'
        temp_html_path = ('file:///' + str(help.repath(html)))
        self.textBrowserHelp.setSource(QtCore.QUrl(temp_html_path))

        # Dialog Window
        about_dialog = about.show_dialog
        asset_dialog = asset.show_dialog
        prefs_dialog = preferences.show_dialog

        # Menu Action
        self.actionAbout.triggered.connect(about_dialog)
        self.actionPreferences.triggered.connect(prefs_dialog)
        self.actionQuit.triggered.connect(functions.close_app)

        # Create New Asset Button
        self.pushBtnNew.clicked.connect(asset_dialog)

        # When calling functions from imported modules that inherit the QMainWindow
        # but located outside its scope, use 'lambda:' followed by the method as
        # though it was defined within the same class for easier code maintenance
        self.actionAlwaysOnTop.triggered.connect(lambda: functions.always_on_top(self))

        # Show Debug CheckBox and Disabled the Debug textEdit
        self.checkBoxDebug.clicked.connect(lambda: functions.show_debug(self))
        self.textEdit.clear()
        self.textEdit.setHidden(True)
        self.textEdit.setEnabled(False)


if __name__ == "__main__":
    functions.high_dpi_check()
    functions.taskbar_icon()

    valid_path = functions.project_path_valid(INI_PATH, PROJECTPATH)
    if valid_path:
        app = QtWidgets.QApplication.instance()
        if app is None:
            app = QtWidgets.QApplication(sys.argv)
        else:
            print('QApplication instance already exists: %s' % str(app))

        window = AssetsBrowser()
        window.show()
        sys.exit(app.exec_())

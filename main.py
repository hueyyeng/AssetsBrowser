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
PROJECTPATH = prefsConfig.PROJECTPATH
INI_PATH = prefsConfig.INI_PATH
THEME = prefsConfig.THEME


class AssetsBrowser(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, parent=None):
        super(AssetsBrowser, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/logo.ico'))
        self.setWindowTitle('Assets Browser [PID: %d]' % QtGui.QApplication.applicationPid())
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint)

        # -----------------------------------------------------------------------------

        # Install the custom output stream for debug log
        sys.stdout = functions.EmittingStream(textWritten = self.debug_stdout)

        # Initialise the chosen theme from INI file
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(THEME))

        # -----------------------------------------------------------------------------

        # Create ColumnView tabs using columnview_tabs function
        functions.columnview_tabs(self.columnViewBG, 'BG')
        functions.columnview_tabs(self.columnViewCH, 'CH')
        functions.columnview_tabs(self.columnViewFX, 'FX')
        functions.columnview_tabs(self.columnViewProps, 'Props')
        functions.columnview_tabs(self.columnViewVehicles, 'Vehicles')

        # -----------------------------------------------------------------------------

        # Project List Dropdown ComboBox
        self.comboBox.fsm = QtGui.QFileSystemModel()
        self.comboBox.rootindex = self.comboBox.fsm.setRootPath(PROJECTPATH)

        self.comboBox.setModel(self.comboBox.fsm)
        self.comboBox.setRootModelIndex(self.comboBox.rootindex)
        self.comboBox.setCurrentIndex(0)  # Set to top directory from PROJECTPATH
        self.comboBox.activated[str].connect(lambda: functions.project_list(self))

        project = (os.listdir(PROJECTPATH))[0]  # Retrieve top directory from PROJECTPATH
        prefsConfig.update_setting(INI_PATH, 'Settings', 'CurrentProject', project)

        # -----------------------------------------------------------------------------

        # Splitter Size Config
        splitter_size = [150, 500]
        self.splitter.setSizes(splitter_size)

        # Help Tab
        help_path = 'ui/help/help.html'
        help_html = open(help_path, "rb").read()
        self.labelHelp.setText(help_html)

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
        # but located outside its scope, use 'lambda:' followed by the function to
        # as though it was defined within the same class for easier code maintenance
        self.actionAlwaysOnTop.triggered.connect(lambda: functions.always_on_top(self))

        # Show Debug CheckBox and Disabled the Debug textEdit
        self.checkBoxDebug.clicked.connect(lambda: functions.show_debug(self))
        self.textEdit.clear()
        self.textEdit.setHidden(True)
        self.textEdit.setEnabled(False)

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


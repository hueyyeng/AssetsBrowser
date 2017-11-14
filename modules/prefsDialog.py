# -*- coding: utf-8 -*-
import os
import sys
import platform
from ui import ui_prefs
from modules import functions
from modules import prefsConfig
from PyQt5 import QtWidgets

# Declare var here first for use in methods below
DEFAULTPATH = prefsConfig.DEFAULTPATH
PROJECTPATH = prefsConfig.PROJECTPATH
INI_PATH = prefsConfig.INI_PATH
THEME = prefsConfig.THEME


class Prefs(QtWidgets.QDialog, ui_prefs.Ui_PrefsDialog):
    def __init__(self, parent=None):
        super(Prefs, self).__init__(parent)
        self.setupUi(self)
        functions.window_icon(self)

        # Retrieve ProjectPath value from PROJECTPATH
        self.projectpath_line.setText(PROJECTPATH)

        # Create config_check to reduce DRY (Don't Repeat Yourself)
        desc = self.desc_check
        # debug = self.debug_check  # TEMP DISABLE

        def config_check(ui, section, setting, value):
            if prefsConfig.get_setting(INI_PATH, section, setting) == value:
                ui.setChecked(True)
            else:
                ui.setChecked(False)

        config_check(desc, 'Settings', 'ShowDescriptionPanel', 'True')
        # config_check(debug, 'Settings', 'ShowDebugLog', 'True')  # TEMP DISABLE

        # Checked the relevant radio button for Theme at runtime
        system = platform.system()
        # theme = prefsConfig.get_setting(INI_PATH, 'UI', 'Theme')
        if system != 'Windows' and THEME == 'Fusion':
            self.theme_radio1.setChecked(True)
            self.theme_radio2.setDisabled(True)
        elif THEME == 'Fusion':
            self.theme_radio1.setChecked(True)
        else:
            self.theme_radio2.setChecked(True)

        # Connect the clicked Qt UI to function
        self.projectpath_tool.clicked.connect(self.browseprojectpath)

        self.desc_check.clicked.connect(self.showdescription)
        self.debug_check.clicked.connect(self.enabledebug)
        self.theme_radio1.clicked.connect(self.theme_fusion)
        self.theme_radio2.clicked.connect(self.theme_windows)

        self.btn_ok.clicked.connect(self.apply)
        self.btn_cancel.clicked.connect(self.reject)

        prefsConfig.get_config(INI_PATH)

    def apply(self):
        # Variables for apply function
        desc = self.desc_check
        # debug = self.debug_check
        desc_param = 'ShowDescriptionPanel'
        # debug_param = 'ShowDebugLog'

        # Function as reusable code for CheckBox elements
        def apply_checkbox(ui, param):
            if ui.isChecked():
                prefsConfig.update_setting(INI_PATH, 'Settings', param, 'True')
            else:
                prefsConfig.update_setting(INI_PATH, 'Settings', param, 'False')

        # Assign apply_checkbox function with description and debug parameters
        apply_checkbox(desc, desc_param)
        # apply_checkbox(debug, debug_param)

        # Theme function as radio toggle
        def apply_theme():
            if self.theme_radio1.isChecked():
                prefsConfig.update_setting(INI_PATH, 'UI', 'Theme', 'Fusion')
            else:
                prefsConfig.update_setting(INI_PATH, 'UI', 'Theme', 'WindowsVista')

            # Apply Theme to MainWindow
            theme = prefsConfig.get_setting(INI_PATH, 'UI', 'Theme')
            QtWidgets.QApplication.setStyle(theme)

        apply_theme()

        # Update the Project Path in the INI file
        def applyprojectpath():
            path = self.projectpath_line.text()
            prefsConfig.update_setting(INI_PATH, 'Settings', 'ProjectPath', path)

        applyprojectpath()

        self.accept()  # For MainWindow to execute restart_app when prefsDialog OK

    def browseprojectpath(self):
        path = str(QtWidgets.QFileDialog.getExistingDirectory(
            self,
            'Choose Directory',
            os.path.expanduser('~'),        # Defaults to home directory
            QtWidgets.QFileDialog.ShowDirsOnly  # Filter list to Directory only
            )
        )

        if path == '':  # If user cancel, popup Warning and reuse the original INI ProjectPath
            widget = QtWidgets.QWidget()
            txt = 'Please choose a directory!'
            QtWidgets.QMessageBox.warning(widget, 'Warning', txt)
            self.projectpath_line.setText(DEFAULTPATH)
        else:
            newpath = path.replace('\\', '/')           # Replace Windows style to UNIX style separator
            system = platform.system()

            if system == 'Linux':
                unixpath = (newpath + '/')
                self.projectpath_line.setText(unixpath)
            elif system == 'Darwin':
                macpath = (newpath + '/')
                self.projectpath_line.setText(macpath)
            else:
                self.projectpath_line.setText(newpath)  # Update the Line textbox with the newly chosen path

    def showdescription(self):
        if self.desc_check.isChecked():
            print 'Description Panel ON'
        else:
            print 'Description Panel OFF'

    def enabledebug(self):
        if self.debug_check.isChecked():
            print 'Debugger ON'
        else:
            print 'Debugger OFF'

    def theme_fusion(self):
        self.theme_radio1.setChecked(True)
        print 'Fusion Theme'

    def theme_windows(self):
        self.theme_radio2.setChecked(True)
        print 'Windows Theme'


def showPrefsDialog():
    window = Prefs()
    spam = window.exec_()

    # If OK, restart app to reinitialize new INI settings
    if spam:
        functions.restart_app()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Prefs()
    window.show()
    sys.exit(app.exec_())

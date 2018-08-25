# -*- coding: utf-8 -*-
import os
import sys
import platform
from PyQt5 import QtWidgets
from config import configurations
from modules import functions
from ui.window import preferences

# Declare var here first for use in methods below
DEFAULTPATH = configurations.DEFAULT_PATH
PROJECTPATH = configurations.PROJECT_PATH
INI_PATH = configurations.INI_PATH
THEME = configurations.THEME


class Prefs(QtWidgets.QDialog, preferences.Ui_PrefsDialog):
    def __init__(self, parent=None):
        super(Prefs, self).__init__(parent)
        self.setupUi(self)
        functions.window_icon(self)

        self.projectpath_line.setText(PROJECTPATH)

        # Create config_check to reduce DRY (Don't Repeat Yourself)
        desc = self.desc_check
        # debug = self.debug_check  # TEMP DISABLE
        def config_check(ui, section, setting, value):
            if configurations.get_setting(INI_PATH, section, setting) == value:
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
        self.projectpath_tool.clicked.connect(self.browser_project_path)
        self.desc_check.clicked.connect(self.show_description)
        self.debug_check.clicked.connect(self.enable_debug)
        self.theme_radio1.clicked.connect(self.theme_fusion)
        self.theme_radio2.clicked.connect(self.theme_windows)
        self.btn_ok.clicked.connect(self.apply)
        self.btn_cancel.clicked.connect(self.reject)

        configurations.get_config(INI_PATH)

    def apply(self):
        desc = self.desc_check
        desc_param = 'ShowDescriptionPanel'

        # Function as reusable code for CheckBox elements
        def apply_checkbox(ui, param):
            if ui.isChecked():
                configurations.update_setting(INI_PATH, 'Settings', param, 'True')
            else:
                configurations.update_setting(INI_PATH, 'Settings', param, 'False')
        apply_checkbox(desc, desc_param)

        # Theme function as radio toggle
        def apply_theme():
            if self.theme_radio1.isChecked():
                configurations.update_setting(INI_PATH, 'UI', 'Theme', 'Fusion')
            else:
                configurations.update_setting(INI_PATH, 'UI', 'Theme', 'WindowsVista')
            theme = configurations.get_setting(INI_PATH, 'UI', 'Theme')
            QtWidgets.QApplication.setStyle(theme)
        apply_theme()

        # Update the Project Path in the INI file
        def apply_project_path():
            path = self.projectpath_line.text()
            configurations.update_setting(INI_PATH, 'Settings', 'ProjectPath', path)
        apply_project_path()

        self.accept()  # For MainWindow to execute restart_app when prefsDialog OK

    def browser_project_path(self):
        path = str(QtWidgets.QFileDialog.getExistingDirectory(
            self,
            'Choose Directory',
            os.path.expanduser('~'),             # Defaults to home directory
            QtWidgets.QFileDialog.ShowDirsOnly,  # Filter list to Directory only
            )
        )

        if path == '':  # If user cancel, popup Warning and reuse the original INI ProjectPath
            widget = QtWidgets.QWidget()
            txt = 'Please choose a directory!'
            QtWidgets.QMessageBox.warning(widget, 'Warning', txt)
            self.projectpath_line.setText(DEFAULTPATH)
        else:
            new_path = path.replace('\\', '/')           # Replace Windows style to UNIX style separator
            system = platform.system()
            if system == 'Linux':
                unix_path = (new_path + '/')
                self.projectpath_line.setText(unix_path)
            elif system == 'Darwin':
                mac_path = (new_path + '/')
                self.projectpath_line.setText(mac_path)
            else:
                self.projectpath_line.setText(new_path)  # Update the Line textbox with the newly chosen path

    def show_description(self):
        if self.desc_check.isChecked():
            print('Description Panel ON')
        else:
            print('Description Panel OFF')

    def enable_debug(self):
        if self.debug_check.isChecked():
            print('Debugger ON')
        else:
            print('Debugger OFF')

    def theme_fusion(self):
        self.theme_radio1.setChecked(True)
        print('Fusion Theme')

    def theme_windows(self):
        self.theme_radio2.setChecked(True)
        print('Windows Theme')


def show_dialog():
    dialog = Prefs()
    if dialog.exec_():  # If OK, restart app to reinitialize new INI settings
        functions.restart_app()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Prefs()
    window.show()
    sys.exit(app.exec_())

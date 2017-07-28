# -*- coding: utf-8 -*-
import os
import sys
from PyQt4 import QtGui
from ui import ui_prefs
from modules import prefsConfig

# Declare path var here first for use in methods below
defaultpath = prefsConfig.get_setting(prefsConfig.INI_PATH, 'Settings', 'ProjectPath')
projpath = defaultpath


class Prefs(QtGui.QDialog, ui_prefs.Ui_PrefsDialog):
    def __init__(self, parent=None):
        super(Prefs, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/logo.ico'))

        # Retrieve ProjectPath value from projpath
        self.projectpath_line.setText(projpath)

        # Created this class to allow inheritance from parent class (Prefs)
        desc = self.desc_check
        debug = self.debug_check

        def config_check(ui, section, setting, value):
            if prefsConfig.get_setting(prefsConfig.INI_PATH, section, setting) == value:
                ui.setChecked(True)
            else:
                ui.setChecked(False)

        config_check(desc, 'Settings', 'ShowDescriptionPanel', 'True')
        config_check(debug, 'Settings', 'ShowDebugLog', 'True')

        # Checked the relevant radio button for Theme at runtime
        if prefsConfig.get_setting(prefsConfig.INI_PATH, 'UI', 'Theme') == 'windowsvista':
            self.theme_radio1.setChecked(True)
        else:
            self.theme_radio2.setChecked(True)

        # Connect the clicked Qt UI to function
        self.projectpath_tool.clicked.connect(self.browseprojectpath)

        self.desc_check.clicked.connect(self.showdescription)
        self.debug_check.clicked.connect(self.showdebug)
        self.theme_radio1.clicked.connect(self.theme_default)
        self.theme_radio2.clicked.connect(self.theme_plastique)

        self.btn_ok.clicked.connect(self.apply)
        self.btn_cancel.clicked.connect(self.reject)

        prefsConfig.get_config(prefsConfig.INI_PATH)

    def apply(self):
        # Variables for apply function
        desc = self.desc_check
        debug = self.debug_check
        desc_param = 'ShowDescriptionPanel'
        debug_param = 'ShowDebugLog'

        # Function as reusable code for CheckBox elements
        def apply_checkbox(ui, param):
            if ui.isChecked():
                prefsConfig.update_setting(prefsConfig.INI_PATH, 'Settings', param, 'True')
            else:
                prefsConfig.update_setting(prefsConfig.INI_PATH, 'Settings', param, 'False')

        # Assign apply_checkbox function with description and debug parameters
        apply_checkbox(desc, desc_param)
        apply_checkbox(debug, debug_param)

        # Theme function as radio toggle
        def apply_theme():
            if self.theme_radio1.isChecked():
                prefsConfig.update_setting(prefsConfig.INI_PATH, 'UI', 'Theme', 'windowsvista')
            else:
                prefsConfig.update_setting(prefsConfig.INI_PATH, 'UI', 'Theme', 'Plastique')

            # Apply Theme to MainWindow
            theme = prefsConfig.get_setting(prefsConfig.INI_PATH, 'UI', 'Theme')
            QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(theme))

        apply_theme()

        # Update the Project Path in the INI file
        def applyprojpath():
            path = self.projectpath_line.text()
            prefsConfig.update_setting(prefsConfig.INI_PATH, 'Settings', 'ProjectPath', path)

        applyprojpath()

        self.accept()

        return True  # For MainWindow to execute restart_app when prefsDialog OK

    def browseprojectpath(self):
        path = str(QtGui.QFileDialog.getExistingDirectory(
            self,
            'Choose Directory',
            os.path.expanduser('~'),  # Default to the home folder
            QtGui.QFileDialog.ShowDirsOnly  # Filter list to Directory only
            )
        )

        if path == '':  # If user cancel, popup Warning and reuse the original INI ProjectPath
            widget = QtGui.QWidget()
            txt = 'Please choose a directory!'
            QtGui.QMessageBox.warning(widget, 'Warning', txt)
            self.projectpath_line.setText(defaultpath)
        else:
            self.projectpath_line.setText(path)  # Update the Line textbox with the newly chosen path

    def showdescription(self):
        if self.desc_check.isChecked():
            print 'Description Panel ON'
        else:
            print 'Description Panel OFF'

    def showdebug(self):
        if self.debug_check.isChecked():
            print 'Debugger ON'
        else:
            print 'Debugger OFF'

    def theme_default(self):
        self.theme_radio1.setChecked(True)
        print 'Default Theme'

    def theme_plastique(self):
        self.theme_radio2.setChecked(True)
        print 'Plastique Theme'


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Prefs()
    window.show()
    sys.exit(app.exec_())

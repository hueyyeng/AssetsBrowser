import os
import sys
import platform
import logging
from PyQt5 import QtWidgets

from config import configurations, constants
import helpers.functions
import ui.functions
from ui.window.ui_preferences import Ui_PrefsDialog

logger = logging.getLogger(__name__)

DEFAULT_PATH = constants.DEFAULT_PATH
INI_PATH = constants.INI_PATH
PROJECT_PATH = constants.PROJECT_PATH
THEME = constants.THEME


class Preferences(QtWidgets.QDialog, Ui_PrefsDialog):
    def __init__(self, parent=None):
        super(Preferences, self).__init__(parent)
        self.setupUi(self)
        self.projectPathLine.setText(PROJECT_PATH)
        ui.functions.set_window_icon(self)

        # 1. Setup QDialogButtonBox
        self.btnDialogBox.button(QtWidgets.QDialogButtonBox.RestoreDefaults).setToolTip('Restore Defaults')
        self.btnDialogBox.button(QtWidgets.QDialogButtonBox.RestoreDefaults).clicked.connect(helpers.functions.ham)
        self.btnDialogBox.button(QtWidgets.QDialogButtonBox.Apply).setToolTip('Apply')
        self.btnDialogBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(helpers.functions.ham)
        self.btnDialogBox.accepted.connect(self._apply)
        self.btnDialogBox.rejected.connect(self.reject)

        # 1.1 Set configurable fields from INI
        self.checkDesc.setChecked(self._get_ini_value('Settings', 'ShowDescriptionPanel'))
        self.checkDebug.setChecked(self._get_ini_value('Settings', 'ShowDebugLog'))
        self.themeRadioLight.setChecked(True) if THEME == 'Default (Light)' else self.themeRadioDark.setChecked(True)

        # 3.1 Setup Settings input/button here
        self.projectPathTool.clicked.connect(self._project_path_dialog)

        # 3.2 Setup Assets input/button here
        # 3.3 Setup Advanced input/button here

    def _get_ini_value(self, section, setting):
        """Get INI value for Preferences UI elements.

        Parameters
        ----------
        section : str
            Section name.
        setting : str
            Setting name.

        Returns
        -------
        str or bool
            The value of the setting.

        """
        value = configurations.get_setting(INI_PATH, section, setting)
        return value

    def _project_path_dialog(self):
        """Opens Project Path Dialog.

        Uses QFileDialog for user to choose the directory for their project path.

        """
        # 1. Prepare `path` var with selected directory path through QFileDialog
        path = str(QtWidgets.QFileDialog.getExistingDirectory(
            self,
            'Choose Directory',
            os.path.expanduser('~'),  # Defaults to home directory
            QtWidgets.QFileDialog.ShowDirsOnly,  # Filter list to Directory only
        ))

        # 2. If user cancel, popup Warning and reuse the original INI ProjectPath
        if path == '':
            widget = QtWidgets.QWidget()
            text = 'Please choose a directory!'
            QtWidgets.QMessageBox.warning(widget, 'Warning', text)
            self.projectPathLine.setText(DEFAULT_PATH)

        # 3. Replace Windows style to UNIX style separator
        new_path = (path + '/') if platform.system() != 'Windows' else path
        new_path.replace('\\', '/')

        # 4. Set Project Path Line text field with new_path value
        logger.info(new_path)
        self.projectPathLine.setText(new_path)

    def _apply(self):
        def apply_checkbox(checkbox, param):
            """Save checkbox value in INI after apply.

            Parameters
            ----------
            checkbox : QtWidgets.QCheckBox
                QCheckbox element
            param : str
                Parameter name

            Returns
            -------
            None

            """
            value = 'True' if checkbox.isChecked() else 'False'
            configurations.update_setting(INI_PATH, 'Settings', param, value)

        apply_checkbox(self.checkDesc, 'ShowDescriptionPanel')
        apply_checkbox(self.checkDebug, 'ShowDebugLog')

        def apply_theme():
            value = str(self.themeBtnGroup.checkedButton().text())
            logger.info(value)
            configurations.update_setting(INI_PATH, 'UI', 'Theme', value)

        apply_theme()

        # Update the Project Path in the INI file
        def apply_project_path():
            path = self.projectPathLine.text()
            configurations.update_setting(INI_PATH, 'Settings', 'ProjectPath', path)

        apply_project_path()
        self.accept()  # Execute restart_app when OK


def show_dialog():
    dialog = Preferences()
    if dialog.exec_():
        # Restart app to reinitialize new INI settings
        helpers.functions.restart_app()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Preferences()
    window.show()
    sys.exit(app.exec_())

"""Preferences Dialog"""
import logging
import os
import platform
import sys
from typing import Any

from PyQt5 import QtWidgets

import helpers.functions
import ui.functions
from config import configurations, constants
from ui.window.ui_preferences import Ui_PrefsDialog

logger = logging.getLogger(__name__)

DEFAULT_PATH = constants.PROJECT_PATH
TOML_PATH = constants.TOML_PATH
PROJECT_PATH = constants.PROJECT_PATH
THEME = constants.THEME


class Preferences(QtWidgets.QDialog, Ui_PrefsDialog):
    def __init__(self, parent=None):
        super(Preferences, self).__init__(parent)
        self.setupUi(self)
        ui.functions.set_window_icon(self)

        # 1. Setup QDialogButtonBox
        self.btnDialogBox.button(QtWidgets.QDialogButtonBox.RestoreDefaults).setToolTip('Restore Defaults')
        self.btnDialogBox.button(QtWidgets.QDialogButtonBox.RestoreDefaults).clicked.connect(helpers.functions.ham)
        self.btnDialogBox.button(QtWidgets.QDialogButtonBox.Apply).setToolTip('Apply')
        self.btnDialogBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(helpers.functions.ham)
        self.btnDialogBox.accepted.connect(self._apply)
        self.btnDialogBox.rejected.connect(self.reject)

        # 2.1 Setup Settings input/button here
        self.projectPathLine.setText(PROJECT_PATH)
        self.projectPathTool.clicked.connect(self._project_path_dialog)
        self.descCheck.setChecked(self._get_toml_value('Settings', 'ShowDescriptionPanel'))
        self.debugCheck.setChecked(self._get_toml_value('Settings', 'ShowDebugLog'))
        self.themeRadioLight.setChecked(True)
        if THEME == 'Dark':
            self.themeRadioDark.setChecked(True)

        # 2.2 Setup Assets input/button here
        self.boxPrefix.setChecked(self._get_toml_value('Assets', 'UsePrefix'))
        self.boxSuffix.setChecked(self._get_toml_value('Assets', 'UseSuffix'))
        self.suffixCustomName.setText(self._get_toml_value('Assets', 'SuffixCustomName'))
        self.categoryBtnAdd.clicked.connect(lambda: self._add_item_list(self.categoryList, "Category"))
        self.categoryBtnRemove.clicked.connect(lambda: self._remove_item_list(self.categoryList))
        self.subfolderBtnAdd.clicked.connect(lambda: self._add_item_list(self.subfolderList, "Subfolder"))
        self.subfolderBtnRemove.clicked.connect(lambda: self._remove_item_list(self.subfolderList))

        # 2.3 Setup Advanced input/button here
        self.metadataCheck.setChecked(self._get_toml_value('Advanced', 'UseMetadata'))
        self.metadataBtnClear.clicked.connect(helpers.functions.ham)
        self.metadataBtnRebuild.clicked.connect(helpers.functions.ham)

        self._populate_list_value(self.categoryList, "Assets", "CategoryList")
        self._populate_list_value(self.subfolderList, "Assets", "SubfolderList")

    def _clear_metadata(self):
        # Find all Metadata files (JSON) and remove the file
        # TODO: Better ot use sqlite3 to handle metadata as DB...
        # TODO: Probably a good idea to allow to export assets metadata as a ZIP?
        pass

    def _rebuild_metadata(self):
        # Rebuild every assets' metadata (will destroy the existing metadata)
        # TODO: Maybe backup existing metadata to a tmp directory?
        pass

    def _add_item_list(self, list_widget: QtWidgets.QListWidget, title="..."):
        """Add item to QListWidget.

        Parameters
        ----------
        list_widget : QtWidgets.QListWidget
            QListWidget instance
        title : str
            Suffix for input dialog's title.

        """
        item = QtWidgets.QListWidgetItem()
        text, ok = QtWidgets.QInputDialog.getText(self, ("Add " + str(title)), "Name:", QtWidgets.QLineEdit.Normal, "")

        if ok and text != '':
            item.setText(str(text))
            list_widget.addItem(item)

    def _remove_item_list(self, list_widget: QtWidgets.QListWidget):
        """Remove items from QListWidget.

        Parameters
        ----------
        list_widget : QtWidgets.QListWidget
            QListWidget instance

        """
        items = list_widget.selectedItems()

        # Exit early if there is no selected items!
        if not items:
            return
        for item in items:
            list_widget.takeItem(list_widget.row(item))
            return

    def _get_toml_value(self, section: str, setting: str) -> Any:
        """Get TOML value for Preferences UI elements.

        Parameters
        ----------
        section : str
            Section name.
        setting : str
            Setting name.

        Returns
        -------
        Any
            The value of the setting.

        """
        value = configurations.get_setting(TOML_PATH, section, setting)
        return value

    def _populate_list_value(self, list_widget: QtWidgets.QListWidget, section: str, setting: str):
        value_list = self._get_toml_value(section, setting)

        # 1. Exit early and log error if not a valid list object
        if not isinstance(value_list, list):
            logger.error("Not a valid list: %s", value_list)
            return

        # 2. Loop through list object and populate target list
        for value in value_list:
            item = QtWidgets.QListWidgetItem()
            item.setText(str(value))
            list_widget.addItem(item)

    def _project_path_dialog(self):
        """Opens Project Path Dialog.

        Uses QFileDialog for user to choose the directory for their project path.

        """
        # 1. Initialize selected directory path through QFileDialog
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
        # TODO: Rework apply function to be more inclusive of every functions?
        def apply_checkbox(checkbox_widget: QtWidgets.QCheckBox, section: str, param: str):
            """Save checkbox value in TOML after apply.

            Parameters
            ----------
            checkbox_widget : QtWidgets.QCheckBox
                QCheckbox instance
            section : str
                Section name
            param : str
                Parameter name

            """
            value = 'True' if checkbox_widget.isChecked() else 'False'
            logger.info(value)
            configurations.update_setting(TOML_PATH, section, param, value)

        apply_checkbox(self.descCheck, 'Settings', 'ShowDescriptionPanel')
        apply_checkbox(self.debugCheck, 'Settings', 'ShowDebugLog')
        apply_checkbox(self.boxPrefix, 'Assets', 'UsePrefix')
        apply_checkbox(self.boxSuffix, 'Assets', 'UseSuffix')
        apply_checkbox(self.metadataCheck, 'Advanced', 'UseMetadata')

        def apply_line_value(line_widget: QtWidgets.QLineEdit, section: str, param: str):
            """Save line value in TOML after apply.

            Parameters
            ----------
            line_widget : QtWidgets.QLineEdit
                QLineEdit instance
            section : str
                Section name
            param : str
                Parameter name

            """
            value = line_widget.text()
            logger.info(value)
            configurations.update_setting(TOML_PATH, section, param, value)

        apply_line_value(self.projectPathLine, 'Settings', 'ProjectPath')
        apply_line_value(self.suffixCustomName, 'Assets', 'SuffixCustomName')

        def apply_list_value(list_widget: QtWidgets.QListWidget, section: str, param: str):
            """Save list value in TOML  after apply.

            Parameters
            ----------
            list_widget : QtWidgets.QListWidget
                QListWidget instance
            section : str
                Section name
            param : str
                Parameter name

            """
            items = []
            for x in range(list_widget.count()):
                value = list_widget.item(x).text()
                items.append(value)
            logger.info(items)
            configurations.update_setting(TOML_PATH, section, param, str(items))

        apply_list_value(self.categoryList, "Assets", "CategoryList")
        apply_list_value(self.subfolderList, "Assets", "SubfolderList")

        def apply_theme():
            value = str(self.themeBtnGrp.checkedButton().text())
            logger.info(value)
            configurations.update_setting(TOML_PATH, 'UI', 'Theme', value)

        apply_theme()

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

"""Preferences Dialog"""
import logging
import os
import platform
import sys
from typing import Any

from PyQt5 import QtWidgets

import helpers.functions
import ui.functions
from config import configurations
from ui.window.ui_preferences import Ui_PrefsDialog

logger = logging.getLogger(__name__)


class Preferences(QtWidgets.QDialog, Ui_PrefsDialog):
    def __init__(self, parent=None):
        super(Preferences, self).__init__(parent)
        self.setupUi(self)
        ui.functions.set_window_icon(self)

        project_path = configurations.get_setting('Settings', 'ProjectPath')
        self.default_path = project_path

        # 1. Setup QDialogButtonBox
        self.btnDialogBox.button(QtWidgets.QDialogButtonBox.RestoreDefaults).setToolTip('Restore Defaults')
        self.btnDialogBox.button(QtWidgets.QDialogButtonBox.RestoreDefaults).clicked.connect(helpers.functions.ham)
        self.btnDialogBox.button(QtWidgets.QDialogButtonBox.Apply).setToolTip('Apply')
        self.btnDialogBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(helpers.functions.ham)
        self.btnDialogBox.accepted.connect(self.apply)
        self.btnDialogBox.rejected.connect(self.reject)

        # 2.1 Setup Settings input/button here
        self.projectPathLine.setText(project_path)
        self.projectPathTool.clicked.connect(self.project_path_dialog)
        self.descCheck.setChecked(self.get_toml_value('Settings', 'ShowDescriptionPanel'))
        self.debugCheck.setChecked(self.get_toml_value('Settings', 'ShowDebugLog'))
        self.themeRadioLight.setChecked(True)
        theme = configurations.get_setting('UI', 'Theme')
        if theme == 'Dark':
            self.themeRadioDark.setChecked(True)

        # 2.2 Setup Assets input/button here
        self.maxCharSpinner.setValue(self.get_toml_value('Assets', 'MaxChars'))
        self.boxPrefix.setChecked(self.get_toml_value('Assets', 'UsePrefix'))
        self.boxSuffix.setChecked(self.get_toml_value('Assets', 'UseSuffix'))
        self.suffixCustomName.setText(self.get_toml_value('Assets', 'SuffixCustomName'))
        self.categoryBtnAdd.clicked.connect(lambda: self.add_item_list(self.categoryList, "Category"))
        self.categoryBtnRemove.clicked.connect(lambda: self.remove_item_list(self.categoryList))
        self.subfolderBtnAdd.clicked.connect(lambda: self.add_item_list(self.subfolderList, "Subfolder"))
        self.subfolderBtnRemove.clicked.connect(lambda: self.remove_item_list(self.subfolderList))

        # 2.3 Setup Advanced input/button here
        # self.metadataCheck.setChecked(self._get_toml_value('Advanced', 'UseMetadata'))
        self.metadataBtnClear.clicked.connect(helpers.functions.ham)
        self.metadataBtnRebuild.clicked.connect(helpers.functions.ham)

        self.populate_list_value(self.categoryList, "Assets", "CategoryList")
        self.populate_list_value(self.subfolderList, "Assets", "SubfolderList")

    def add_item_list(self, widget: QtWidgets.QListWidget, title="..."):
        """Add item to QListWidget.

        Parameters
        ----------
        widget : QtWidgets.QListWidget
            QListWidget instance
        title : str
            Suffix for input dialog's title.

        """
        item = QtWidgets.QListWidgetItem()
        text, ok = QtWidgets.QInputDialog.getText(self, ("Add " + str(title)), "Name:", QtWidgets.QLineEdit.Normal, "")

        if ok and text != '':
            item.setText(str(text))
            widget.addItem(item)

    def remove_item_list(self, widget: QtWidgets.QListWidget):
        """Remove items from QListWidget.

        Parameters
        ----------
        widget : QtWidgets.QListWidget
            QListWidget instance

        """
        items = widget.selectedItems()

        # Exit early if there is no selected items!
        if not items:
            return
        for item in items:
            widget.takeItem(widget.row(item))
            return

    def get_toml_value(self, section: str, setting: str) -> Any:
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
        value = configurations.get_setting(section, setting)
        return value

    def populate_list_value(self, list_widget: QtWidgets.QListWidget, section: str, setting: str):
        value_list = self.get_toml_value(section, setting)

        # 1. Exit early and log error if not a valid list object
        if not isinstance(value_list, list):
            logger.error("Not a valid list: %s", value_list)
            return

        # 2. Loop through list object and populate target list
        for value in value_list:
            item = QtWidgets.QListWidgetItem()
            item.setText(str(value))
            list_widget.addItem(item)

    def project_path_dialog(self):
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
            self.projectPathLine.setText(self.default_path)

        # 3. Replace Windows style to UNIX style separator
        new_path = (path + '/') if platform.system() != 'Windows' else path
        new_path.replace('\\', '/')

        # 4. Set Project Path Line text field with new_path value
        logger.info(new_path)
        self.projectPathLine.setText(new_path)

    def get_checkbox_value(self, widget: QtWidgets.QCheckBox, setting: str):
        value = widget.isChecked()
        config = {setting: value}
        return config

    def get_line_value(self, widget: QtWidgets.QLineEdit, setting: str):
        value = widget.text()
        config = {setting: value}
        return config

    def get_list_value(self, widget: QtWidgets.QListWidget, setting: str):
        items = []
        for x in range(widget.count()):
            value = widget.item(x).text()
            items.append(value)
        config = {setting: items}
        return config

    def apply(self):
        checkboxes = (
            (self.descCheck, "ShowDescriptionPanel"),
            (self.debugCheck, "ShowDebugLog"),
            (self.boxPrefix, "UsePrefix"),
            (self.boxSuffix, "UseSuffix"),
            (self.metadataCheck, "UseMetadata"),
        )
        lines = (
            (self.projectPathLine, "ProjectPath"),
            (self.suffixCustomName, "SuffixCustomName"),
        )
        lists = (
            (self.categoryList, "CategoryList"),
            (self.subfolderList, "SubfolderList"),
        )
        config = {}

        for widget, setting in checkboxes:
            config.update(
                self.get_checkbox_value(widget, setting)
            )

        for widget, setting in lines:
            config.update(
                self.get_line_value(widget, setting)
            )

        for widget, setting in lists:
            config.update(
                self.get_list_value(widget, setting)
            )

        config.update({
            "Theme": str(self.themeBtnGrp.checkedButton().text()),
            "MaxChars": self.maxCharSpinner.value(),
        })

        configurations.bulk_update_settings(config)
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

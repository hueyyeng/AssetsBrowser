"""Asset Dialog"""
import logging
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

import ui.functions
from config import configurations
from database.db import Database
from database.models import Asset as AssetModel
from database.models import Category, Project
from helpers.utils import alert_window
from ui.window.ui_asset import Ui_AssetDialog

logger = logging.getLogger(__name__)


class AssetDialog(QtWidgets.QDialog, Ui_AssetDialog):
    def __init__(self, parent=None):
        super(AssetDialog, self).__init__(parent)
        self.setupUi(self)
        self.db = Database(use_default_db=True)
        ui.functions.set_window_icon(self)
        self._setup_ui_buttons()
        self._setup_asset_name_validator()
        self._setup_category_combobox()
        self._append_max_chars_suffix()

    def _append_max_chars_suffix(self):
        """Append Max Chars to Asset's Name label"""
        max_chars = configurations.get_setting('Assets', 'MaxChars')
        label = self.shortNameLabel.text()
        self.shortNameLabel.setText(f"{label} (Max chars: {max_chars})")

    def _setup_category_combobox(self):
        """Setup Category combobox"""
        asset_categories = configurations.get_setting('Assets', 'CategoryList')
        for asset_category in asset_categories:
            self.categoryComboBox.addItem(asset_category)

    def _setup_asset_name_validator(self):
        """Setup Asset name validator"""
        # Limit the range of acceptable characters input by the user using regex
        regex = QtCore.QRegularExpression("^[a-zA-Z0-9]+$")
        validator = QtGui.QRegularExpressionValidator(regex, self)
        self.shortNameLineEdit.setValidator(validator)
        # Runs text_uppercase and preview whenever Qt detects textChanged
        self.shortNameLineEdit.textChanged.connect(self.text_uppercase)
        self.shortNameLineEdit.textChanged.connect(self.preview_asset_name)

    def _setup_ui_buttons(self):
        self.btnCreate.setDisabled(True)
        self.btnCreate.clicked.connect(self.create_asset)
        self.btnCancel.clicked.connect(self.close)
        self.previewGroup.clicked.connect(self.preview_asset_name)

    def text_uppercase(self):
        """Convert text to UPPERCASE."""
        asset_name = self.shortNameLineEdit.text()
        self.shortNameLineEdit.setText(asset_name.upper())

    def create_asset(self):
        """Create asset with preconfigure directories structure."""
        current_project = configurations.get_setting('Settings', 'CurrentProject')
        project_path = configurations.get_setting('Settings', 'ProjectPath')
        asset_category = self.catBtnGroup.checkedButton().text()
        asset_format = self.formatComboBox.currentText()
        asset_path = os.path.join(project_path, current_project, "Assets", asset_category)
        asset_full_name = self.nameLineEdit.text()
        asset_short_name = self.generate_asset_name()
        full_path = os.path.join(asset_path, asset_short_name)

        # Create Asset directory
        try:
            os.mkdir(full_path)
        except OSError:
            alert_window('Warning', 'ERROR! Asset already exists!')
        logger.debug('Assets will be created at %s', full_path)

        # Create Asset's subfolders
        folders = configurations.get_setting('Assets', 'SubfolderList')
        logger.debug(folders)
        for folder in folders:
            try:
                os.mkdir(os.path.join(full_path, folder))
            except OSError:
                logger.error("The Assets directory %s cannot be created.", full_path)

        # Retrieve category and project id. If not exists, create the category and project in DB
        category, _ = Category.get_or_create(name=asset_category)
        project, _ = Project.get_or_create(short_name=current_project)

        # Create Asset entry in DB
        asset_data = {
            "category": category.id,
            "project": project.id,
            "format": asset_format,
            "name": asset_full_name,
            "short_name": asset_short_name,
        }
        AssetModel.create(**asset_data)
        logger.info({
            "msg": "Asset creation successful",
            "short_name": asset_short_name,
            "project": project,
        })
        self.accept()

    def generate_asset_name(self):
        """Generate asset's name with category prefix.

        Use input from `shortNameLineEdit` to generate asset's name with

        Returns
        -------
        str
            Asset's name with category prefix

        """
        category = self.categoryComboBox.currentText()
        prefix = category[0].lower()
        suffix = self.shortNameLineEdit.text()
        asset_name = f"{prefix}{suffix}"
        return asset_name

    def preview_asset_name(self):
        """Preview asset's name in non-editable text field.

        Notes
        -----
        Since both `catBtnGroup` and `shortNameLineEdit` emits signal to this
        method, it allows the text field to "dynamically" update.

        """
        # 1. Disable Create button and clear the text field to create "illusion" of dynamic update
        self.previewText.clear()
        self.btnCreate.setDisabled(True)

        # 2.1 Generate preview message
        name_length = len(self.shortNameLineEdit.text())
        checked = self.previewGroup.isChecked()
        asset_name = self.generate_asset_name()

        # 2.2 Enable Create button and display the expected asset name
        message = "Ensure asset's name is three characters length!"
        if checked and name_length == 3:
            self.btnCreate.setDisabled(False)
            project = configurations.get_setting('Settings', 'CurrentProject')
            message = f"The asset name will be {asset_name}.\n" \
                      f"Ensure the asset name is correct before proceeding.\n" \
                      f"\n" \
                      f"Project:  {project}"
        self.previewText.appendPlainText(message)


def show_dialog():
    dialog = AssetDialog()
    if dialog.exec_():
        logger.debug('Creating new asset...')
    else:
        logger.debug('Aborting Create New Asset...')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AssetDialog()
    window.show()
    sys.exit(app.exec_())

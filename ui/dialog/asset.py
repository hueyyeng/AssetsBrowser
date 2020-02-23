"""Asset Dialog"""
import logging
import os
import sys

import sip
from PyQt5 import QtCore, QtGui, QtWidgets

import ui.functions
from config import configurations, constants
from config.constants import PROJECT_PATH, TOML_PATH
from helpers.utils import alert_window
from ui.window.ui_asset import Ui_AssetDialog

logger = logging.getLogger(__name__)


class Asset(QtWidgets.QDialog, Ui_AssetDialog):
    def __init__(self, parent=None):
        super(Asset, self).__init__(parent)
        self.setupUi(self)
        ui.functions.set_window_icon(self)

        # 1.1 Setup buttons here
        self.btnCreate.setDisabled(True)
        self.btnCreate.clicked.connect(self._create_asset)
        self.btnCancel.clicked.connect(self.close)
        self.previewGroup.clicked.connect(self._preview)

        # 1.2 Setup category radio buttons
        asset_categories = constants.ASSETS_CATEGORY_LIST
        # TODO: Rework dynamic radio buttons to retrieve categories per project basis instead of INI
        placeholder = bool(len(asset_categories))
        self._remove_radio_button(placeholder)
        for asset_category in asset_categories:
            self._generate_radio_button(asset_category)

        # 1.3 Set the first radio button as default choice
        radio_buttons = self.catGroup.findChildren(QtWidgets.QRadioButton)
        radio_buttons[0].setChecked(True)

        # 2.1 Limit the range of acceptable characters input by the user using regex
        regex = QtCore.QRegularExpression("^[a-zA-Z0-9]+$")
        self.validator = QtGui.QRegularExpressionValidator(regex, self)
        self.assetLineEdit.setValidator(self.validator)

        # 2.2 Runs text_uppercase and preview whenever Qt detects textChanged
        self.assetLineEdit.textChanged.connect(self._text_uppercase)
        self.assetLineEdit.textChanged.connect(self._preview)

    def _remove_radio_button(self, placeholder=False):
        """Remove radio button."""
        # TODO: Allow removal of any radio buttons
        if not placeholder:
            self.layoutVtlCat.removeWidget(self.catPlaceholder)
            sip.delete(self.catPlaceholder)
            self.catPlaceholder = None

    def _generate_radio_button(self, name):
        """Generate category radio button."""
        _translate = QtCore.QCoreApplication.translate
        self.catRadioButton = QtWidgets.QRadioButton(self.catGroup)
        self.catRadioButton.setObjectName("cat" + name)
        self.catBtnGroup.addButton(self.catRadioButton)
        self.layoutVtlCat.addWidget(self.catRadioButton)
        self.catRadioButton.setText(_translate("AssetDialog", name))
        self.catRadioButton.clicked.connect(self._preview)

    def _text_uppercase(self):
        """Convert text to UPPERCASE."""
        asset_name = self.assetLineEdit.text()
        self.assetLineEdit.setText(asset_name.upper())

    def _create_asset(self):
        """Create asset with preconfigure directories structure."""
        # 1. Prepare variables
        category = str(self.catBtnGroup.checkedButton().text())
        project = configurations.get_setting(TOML_PATH, 'Settings', 'CurrentProject')
        asset_path = os.path.join(PROJECT_PATH, project, "Assets", category)
        asset_name = str(self._preview())
        full_path = os.path.join(asset_path, asset_name)

        # 2.1 Raise error if `full_path` exists
        try:
            os.mkdir(full_path)
        except OSError:
            alert_window('Warning', 'ERROR! Asset already exists!')
        logger.debug('Assets will be created at %s', full_path)

        # 2.2 Create Assets directory
        folders = constants.ASSETS_SUBFOLDER_LIST
        logger.debug(folders)
        for folder in folders:
            try:
                os.mkdir(os.path.join(full_path, folder))
            except OSError:
                logger.error("The Assets directory %s cannot be created.", full_path)

        self.accept()

    def _generate_asset_name(self):
        """Generate asset's name with category prefix.

        Use input from `assetLineEdit` to generate asset's name with

        Returns
        -------
        str
            Asset's name with category prefix

        """
        category = str(self.catBtnGroup.checkedButton().text())
        prefix = category[0].lower()
        suffix = str(self.assetLineEdit.text())
        asset_name = (prefix + suffix)
        return asset_name

    def _preview(self):
        """Previews asset's creation name in non-editable text field.

        Notes
        -----
        Since both `catBtnGroup` and `assetLineEdit` emits signal to this
        method, it allows the text field to "dynamically" update.

        Returns
        -------
        str
            Asset's name.

        """
        # 1. Disable Create button and clear the text field to create "illusion" of dynamic update
        self.previewText.clear()
        self.btnCreate.setDisabled(True)

        # 2.1 Generate preview message
        name_length = len(self.assetLineEdit.text())
        checked = self.previewGroup.isChecked()
        asset_name = self._generate_asset_name()
        message = ''

        # 2.2 Enable Create button and display the expected asset name
        if checked and name_length != 3:
            message = "Ensure asset's name is three characters length!"
        if checked and name_length == 3:
            self.btnCreate.setDisabled(False)
            project = configurations.get_setting(TOML_PATH, 'Settings', 'CurrentProject')
            message = (
                    'The asset name will be ' + asset_name + '.\n'
                    + 'Ensure the asset name is correct before proceeding.\n'
                    + '\n'
                    + 'Project: ' + project
            )
        self.previewText.appendPlainText(message)
        return asset_name


def show_dialog():
    dialog = Asset()
    if dialog.exec_():
        logger.debug('Creating new asset...')
    else:
        logger.debug('Aborting Create New Asset...')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Asset()
    window.show()
    sys.exit(app.exec_())

import os
import sys
import json
import logging
from PyQt5 import QtGui, QtCore, QtWidgets
from config import configurations, constants
from modules import functions
from ui.window.ui_asset import Ui_AssetDialog

logger = logging.getLogger(__name__)

PROJECT_PATH = constants.PROJECT_PATH
INI_PATH = constants.INI_PATH
CURRENT_PROJECT = configurations.get_setting(INI_PATH, 'Settings', 'CurrentProject')
# TODO: Rework CURRENTPROJECT to properly receive INI CurrentProject value


class AssetDialog(QtWidgets.QDialog, Ui_AssetDialog):
    def __init__(self, parent=None):
        super(AssetDialog, self).__init__(parent)
        self.setupUi(self)
        functions.set_window_icon(self)

        # Disable to prevent user from creating without inputting asset name
        self.btnCreate.setDisabled(True)

        # Buttons Action
        self.btnCreate.clicked.connect(self.create_asset)
        self.btnCancel.clicked.connect(self.close)
        self.previewGroup.clicked.connect(self.preview)

        # Setup category radio buttons
        placeholder = False
        asset_categories = json.loads(constants.ASSETS_CATEGORY_LIST)
        if len(asset_categories) == 0:
            placeholder = True
        self.remove_radio_button(placeholder)
        for asset_category in asset_categories:
            self.generate_radio_button(asset_category)

        # Set the first radio button as default choice
        radio_buttons = self.catGroup.findChildren(QtWidgets.QRadioButton)
        radio_buttons[0].setChecked(True)

        # Limit the range of acceptable characters input by the user using regex
        regex = QtCore.QRegularExpression("^[a-zA-Z0-9]+$")
        self.validator = QtGui.QRegularExpressionValidator(regex, self)
        self.assetLineEdit.setValidator(self.validator)

        # Runs text_uppercase and preview whenever Qt detects textChanged
        self.assetLineEdit.textChanged.connect(self.text_uppercase)
        self.assetLineEdit.textChanged.connect(self.preview)

    def remove_radio_button(self, placeholder=False):
        """Remove radio button."""
        # TODO: Allow removal of any radio buttons
        if not placeholder:
            import sip
            self.layoutVtlCat.removeWidget(self.catPlaceholder)
            sip.delete(self.catPlaceholder)
            self.catPlaceholder = None

    def generate_radio_button(self, name):
        """Generate category radio button."""
        _translate = QtCore.QCoreApplication.translate
        self.catRadioButton = QtWidgets.QRadioButton(self.catGroup)
        self.catRadioButton.setObjectName("cat" + name)
        self.catBtnGroup.addButton(self.catRadioButton)
        self.layoutVtlCat.addWidget(self.catRadioButton)
        self.catRadioButton.setText(_translate("AssetDialog", name))
        self.catRadioButton.clicked.connect(self.preview)

    def text_uppercase(self):
        """Convert text to UPPERCASE."""
        asset_name = self.assetLineEdit.text()
        self.assetLineEdit.setText(asset_name.upper())

    def create_asset(self):
        """Create asset with preconfigure directories structure."""
        # 1. Prepare variables
        category = str(self.catBtnGroup.checkedButton().text())
        asset_name = str(self.preview())
        asset_path = (PROJECT_PATH + CURRENT_PROJECT + "/Assets/" + category)
        full_path = (asset_path + '/' + asset_name)

        # 2.1 Raise error if `full_path` exists
        if os.path.exists(full_path):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle('Warning')
            msg.setText('ERROR! Asset already exists!')
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            functions.set_window_icon(msg)
            msg.exec_()

        # 2.2 Create Assets directory
        else:
            os.mkdir(full_path)
            logger.debug('Assets will be created at %s', full_path)
            # TODO: Rework hard-coded folders for Create New Assets. Use JSON to parse list from INI?
            folders = json.loads(constants.ASSETS_SUBFOLDER_LIST)
            logger.debug(folders)
            for folder in folders:
                try:
                    os.mkdir(os.path.join(full_path, folder))
                except OSError:
                    logger.error("The Assets directory %s cannot be created.", full_path)

            self.accept()

    def preview(self):
        """Previews asset's creation name in non-editable text field.

        Notes
        -----
        Since both ``category radio buttons`` and ``assetLineEdit`` emits signal to this
        method, it allows the text field to "dynamically" update.

        Returns
        -------
        None

        """
        # 1. Clear the text field for every signal to create "illusion" of dynamic update
        self.previewText.clear()
        self.btnCreate.setDisabled(True)
        name_length = len(self.assetLineEdit.text())
        checked = self.previewGroup.isChecked()
        # 2.1 Generate preview message
        if checked and name_length == 3:
            self.btnCreate.setDisabled(False)
            category = str(self.catBtnGroup.checkedButton().text())
            prefix = category[0].lower()
            suffix = str(self.assetLineEdit.text())
            asset_name = (prefix + suffix)
            project = configurations.get_setting(INI_PATH, 'Settings', 'CurrentProject')
            asset_text = (
                    'The asset name will be ' + asset_name + '.\n'
                    + 'Ensure the asset name is correct before proceeding.\n'
                    + '\n'
                    + 'Project: ' + project
            )
            self.previewText.appendPlainText(asset_text)
        # 2.2 Display warning text when asset name is not fulfilled
        elif checked and name_length != 3:
            warning_text = 'ENSURE ASSET NAME IS THREE CHARACTERS LENGTH!'
            self.previewText.appendPlainText(warning_text)


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

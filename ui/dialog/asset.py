import os
import sys
import json
import logging
from PyQt5 import QtGui, QtCore, QtWidgets
from config import configurations, constants
from modules import functions
from ui.window.asset import Ui_AssetDialog

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

        # Buttons Action
        self.btnCreate.clicked.connect(self.create_asset)
        self.btnCreate.setDisabled(True)  # Disable to prevent user from creating without inputting asset name
        self.btnCancel.clicked.connect(self.close)
        self.previewGroup.clicked.connect(self.preview)

        # Set BG radio button as default choice
        self.catBG.setChecked(True)

        # Iterate each radio_button using Qt findChildren
        radio_buttons = self.catGroup.findChildren(QtWidgets.QRadioButton)
        for radio_button in radio_buttons:
            radio_button.clicked.connect(self.preview)

        # Limit the range of acceptable characters input by the user using regex
        regex = QtCore.QRegularExpression("^[a-zA-Z0-9]+$")
        self.validator = QtGui.QRegularExpressionValidator(regex, self)
        self.assetLineEdit.setValidator(self.validator)

        # Runs text_uppercase and preview whenever Qt detects textChanged
        self.assetLineEdit.textChanged.connect(self.text_uppercase)
        self.assetLineEdit.textChanged.connect(self.preview)

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
        project = configurations.get_setting(INI_PATH, 'Settings', 'CurrentProject')
        length = len(self.assetLineEdit.text())
        checked = self.previewGroup.isChecked()
        if checked and length == 3:
            self.previewText.clear()  # Clear the text field for every signal to create "illusion" of dynamic update
            self.btnCreate.setDisabled(False)
            category = str(self.catBtnGroup.checkedButton().text())
            prefix = category[0].lower()  # Slice the first letter of the selected category radio and make it lowercase
            suffix = str(self.assetLineEdit.text())  # Retrieve the assetLineEdit text as string
            asset_name = (prefix + suffix)
            asset_text = (
                    'The asset name will be ' + asset_name + '.'
                    + '\n'
                    + 'Ensure the asset name is correct before proceeding.'
                    + '\n'
                    + '\n'
                    + 'Project: ' + project
            )
            self.previewText.appendPlainText(asset_text)
        elif checked and length != 3:
            warning_text = 'ENSURE ASSET NAME IS THREE CHARACTERS LENGTH!'
            self.previewText.appendPlainText(warning_text)
            self.previewText.clear()
            self.btnCreate.setDisabled(True)
        else:
            self.previewText.clear()
            self.btnCreate.setDisabled(True)


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

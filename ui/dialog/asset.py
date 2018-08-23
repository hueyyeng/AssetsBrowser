# -*- coding: utf-8 -*-
import os
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from config import configurations
from modules import functions
from ui.window import asset

PROJECTPATH = configurations.PROJECTPATH
INI_PATH = configurations.INI_PATH
# CURRENTPROJECT = prefsConfig.CURRENTPROJECT
# CURRENTPROJECT = prefsConfig.get_setting(INI_PATH, 'Settings', 'CurrentProject')
# TODO: Rework CURRENTPROJECT to properly receive INI CurrentProject value


class AssetDialog(QtWidgets.QDialog, asset.Ui_AssetDialog):
    def __init__(self, parent=None):
        super(AssetDialog, self).__init__(parent)
        self.setupUi(self)
        functions.window_icon(self)

        # Buttons Action
        self.btnCreate.clicked.connect(self.create_asset)
        self.btnCancel.clicked.connect(self.close)
        self.previewGroup.clicked.connect(self.preview)

        # Set BG radio button as default choice
        self.catBG.setChecked(True)

        # Disable Create button to prevent user from creating without inputting asset name
        self.btnCreate.setDisabled(True)

        # Iterate each radio_button using Qt findChildren
        radio_buttons = self.catGroup.findChildren(QtWidgets.QRadioButton)
        for button in radio_buttons:
            button.clicked.connect(self.preview)

        # Limit the range of acceptable characters input by the user
        regex = QtCore.QRegularExpression("^[a-zA-Z0-9]+$")

        # Declare self.validator with QRegExpValidator using regex var as argument
        self.validator = QtGui.QRegularExpressionValidator(regex, self)

        # Qt LineEdit has a setValidator attribute which requires
        # either QValidator or QRegExpValidator as argument
        self.assetLineEdit.setValidator(self.validator)

        # Runs text_uppercase and preview whenever Qt detects textChanged
        self.assetLineEdit.textChanged.connect(self.text_uppercase)
        self.assetLineEdit.textChanged.connect(self.preview)

    # Change text to UPPERCASE
    def text_uppercase(self):
        asset_name = self.assetLineEdit.text()
        self.assetLineEdit.setText(asset_name.upper())

    # Create asset with preconfigure directories structure
    def create_asset(self):
        # project = CURRENTPROJECT
        project = configurations.get_setting(INI_PATH, 'Settings', 'CurrentProject')
        category = str(self.catBtnGroup.checkedButton().text())
        asset_name = str(self.preview())
        asset_path = (PROJECTPATH + project + "/Assets/" + category)
        full_path = (asset_path + '/' + asset_name)

        # Check whether Asset directory already exist
        if os.path.exists(full_path):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle('Warning')
            msg.setText('ERROR! Asset already exists!')
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            functions.window_icon(msg)
            msg.exec_()
        else:
            os.mkdir(full_path)
            print('Assets will be created at ' + full_path)

            # Declare names for child folders
            folder1 = "Scenes"
            folder2 = "Textures"
            folder3 = "References"
            folder4 = None
            folder5 = "WIP"

            folders = [folder1, folder2, folder3, folder4, folder5]
            for folder in folders:
                if folder is None:
                    pass
                else:
                    os.mkdir(os.path.join(full_path, folder))

            self.accept()

    # A check group that has non-editable text field to preview the asset's
    # name. Since both the category radio buttons and the assetLineEdit emit a
    # signal to this method, it allows the text field to "dynamically" update.
    def preview(self):
        project = configurations.get_setting(INI_PATH, 'Settings', 'CurrentProject')
        checked = self.previewGroup.isChecked()
        length = len(self.assetLineEdit.text())

        if checked and length == 3:
            self.previewText.clear()  # Clear the text field for every signal to create "illusion" of dynamic update
            self.btnCreate.setDisabled(False)  # Enable Create button
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
            self.previewText.clear()
            self.btnCreate.setDisabled(True)
            warning_text = 'ENSURE ASSET NAME IS THREE CHARACTERS LENGTH!'
            self.previewText.appendPlainText(warning_text)
        else:
            self.previewText.clear()
            self.btnCreate.setDisabled(True)


def show_dialog():
    dialog = AssetDialog()
    if dialog.exec_():
        print('Creating new asset...')
    else:
        print('Aborting Create New Asset...')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AssetDialog()
    window.show()
    sys.exit(app.exec_())

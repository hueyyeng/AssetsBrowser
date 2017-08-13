# -*- coding: utf-8 -*-
import os
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from ui import ui_asset
from modules import prefsConfig


# Declare var here first for use in methods below
CURRENTPROJECT = prefsConfig.CURRENTPROJECT
PROJECTPATH = prefsConfig.PROJECTPATH
INI_PATH = prefsConfig.INI_PATH


class AssetDialog(QtGui.QDialog, ui_asset.Ui_AssetDialog):
    def __init__(self, parent=None):
        super(AssetDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/logo.ico'))

        # Buttons Action
        self.btnCreate.clicked.connect(self.create_asset)
        self.btnCancel.clicked.connect(self.close)
        self.previewGroup.clicked.connect(self.preview)

        # Set BG radio button as default choice
        self.catBG.setChecked(True)

        # Disable Create button to prevent user from creating without inputting asset name
        self.btnCreate.setDisabled(True)

        # Create a radioButton list using Qt findChildren which returns
        # the type that we wanted (in this case, QRadioButton)
        radioButton = self.catGroup.findChildren(QtGui.QRadioButton)

        # Iterate each radioButton in a for loop to reduce code duplication
        for each in radioButton:

            # Define a method to return the text value of the radio buttons
            # when checked. In this case, the radio buttons are grouped using
            # QButtonGroup in QtDesigner so we can use the checkedButton()
            # attribute as QGroupBox lack such feature
            def category_checked():
                category = self.catBtnGroup.checkedButton().text()
                print (category + ' is selected.')

            # Connect each radioButton to category_checked when clicked
            each.clicked.connect(category_checked)
            each.clicked.connect(self.preview)

        # Regex are used to limit the range of acceptable characters to
        # prevent accidental non-acceptable input by the user.
        # Search for "regular expression" to know the usage parameter
        # which are often compatible with various languages.
        regex = QtCore.QRegExp("^[a-zA-Z0-9]+$")

        # Declare self.validator with QRegExpValidator using regex var as argument
        self.validator = QtGui.QRegExpValidator(regex, self)

        # Qt LineEdit has a setValidator attribute which requires
        # either QValidator or QRegExpValidator as argument
        self.assetLineEdit.setValidator(self.validator)

        # Using the New-style Signal to connect assetLineEdit to fix_case method
        # whenever Qt detects textChanged
        self.assetLineEdit.textChanged[str].connect(self.fix_case)
        self.assetLineEdit.textChanged[str].connect(self.preview)

    # Create a method that will be called when assetLineEdit.textChanged occurs.
    # The "text" argument can be anything like "spam", "ham", or etc as long
    # the relevant parameter are appropriately rename like (spam.toUpper()).
    def fix_case(self, text):
        self.assetLineEdit.setText(text.toUpper())  # Convert to Uppercase

    # Create asset with preconfigure directories structure
    def create_asset(self):
        project = CURRENTPROJECT()
        category = str(self.catBtnGroup.checkedButton().text())

        asset_name = str(self.preview())
        asset_path = (PROJECTPATH + project + "/Assets/" + category)
        full_path = (asset_path + '/' + asset_name)

        # Check whether Asset directory already exist
        if os.path.exists(full_path):
            widget = QtGui.QWidget()
            text = 'ERROR! Asset already exists!'
            QtGui.QMessageBox.warning(widget, 'Warning', text)
        else:
            os.mkdir(full_path, 0755)
            print ('Assets will be created at ' + full_path)

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

    # A checkable group that has non-editable text field to preview the asset's
    # name. Since both the category radio buttons and the assetLineEdit emit a
    # signal to this method, it allows the text field to "dynamically" update.
    def preview(self):
        project = CURRENTPROJECT()

        checked = self.previewGroup.isChecked()
        length = len(self.assetLineEdit.text())

        if checked and length == 3:
            self.previewText.clear()  # Clear the text field for every signal to create "illusion" of dynamic update
            self.btnCreate.setDisabled(False)  # Enabled Create button

            cat = str(self.catBtnGroup.checkedButton().text())

            prefix = cat[0].lower()  # Slice the first letter of the selected category radio and make it lowercase
            suffix = str(self.assetLineEdit.text())  # Retrieve the assetLineEdit text as string

            asset_name = (prefix + suffix)

            asset_text = 'The asset name will be ' + asset_name + '.' + \
                         '\nEnsure the asset name is correct before proceeding.' + \
                         '\n\nProject: ' + project

            self.previewText.appendPlainText(asset_text)

            return asset_name

        elif checked and length != 3:
            self.previewText.clear()
            self.btnCreate.setDisabled(True)

            warning_text = 'ENSURE ASSET NAME IS THREE CHARACTERS LENGTH!'
            self.previewText.appendPlainText(warning_text)

        else:
            self.previewText.clear()
            self.btnCreate.setDisabled(True)


def showAssetDialog():
    window = AssetDialog()
    spam = window.exec_()

    # If Create, execute spam to create the new asset folders
    if spam:
        print 'Creating new asset...'
    else:
        print 'Aborting Create New Asset...'


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = AssetDialog()
    window.show()
    sys.exit(app.exec_())

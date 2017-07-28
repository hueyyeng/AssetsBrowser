# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from ui import ui_asset


class AssetDialog(QtGui.QDialog, ui_asset.Ui_AssetDialog):
    def __init__(self, parent=None):
        super(AssetDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/logo.ico'))

        # Declare var that are only used outside of __init__
        self.thread = ''

        # Buttons Action
        self.btnCreate.clicked.connect(self.new_asset)
        self.btnCancel.clicked.connect(self.close)

        self.previewGroup.clicked.connect(self.preview)

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

        # Using the New-style Signal to connect assetLineEdit to fixCase method
        # whenever Qt detects textChanged
        self.assetLineEdit.textChanged[str].connect(self.fixCase)

    # Create a method that will be called when assetLineEdit.textChanged occurs.
    # The "text" argument can be anything like "spam", "ham", or etc as long
    # the relevant parameter are appropriately rename like (spam.toUpper()).
    def fixCase(self, text):
        self.assetLineEdit.setText(text.toUpper()) # Convert to Uppercase

    def new_asset(self):
        print self.catBtnGroup.checkedButton().text()

    def preview(self):
        if self.previewGroup.isChecked():
            ham = str(self.catBtnGroup.checkedButton().text())

            prefix = ham[0].lower()
            suffix = str(self.assetLineEdit.text())

            asset_name = 'The asset name will be ' + (prefix + suffix) + '.' + \
                         '\nEnsure the asset name is correct before proceeding.'

            self.previewText.appendPlainText(asset_name)
        else:
            self.previewText.clear()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = AssetDialog()
    window.show()
    sys.exit(app.exec_())

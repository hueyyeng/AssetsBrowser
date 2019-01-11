import os
import sys
import platform
import json
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
        self.descCheck.setChecked(self._get_ini_value('Settings', 'ShowDescriptionPanel'))
        self.debugCheck.setChecked(self._get_ini_value('Settings', 'ShowDebugLog'))
        self.themeRadioLight.setChecked(True)
        if THEME == 'Dark':
            self.themeRadioDark.setChecked(True)

        # 2.2 Setup Assets input/button here
        self.boxPrefix.setChecked(self._get_ini_value('Assets', 'UsePrefix'))
        self.boxSuffix.setChecked(self._get_ini_value('Assets', 'UseSuffix'))
        self.suffixCustomName.setText(self._get_ini_value('Assets', 'SuffixCustomName'))
        self.categoryBtnAdd.clicked.connect(lambda: self._add_item_list(self.categoryList, "Category"))
        self.categoryBtnRemove.clicked.connect(lambda: self._remove_item_list(self.categoryList))
        self.subfolderBtnAdd.clicked.connect(lambda: self._add_item_list(self.subfolderList, "Subfolder"))
        self.subfolderBtnRemove.clicked.connect(lambda: self._remove_item_list(self.subfolderList))

        # 2.3 Setup Advanced input/button here
        self.metadataCheck.setChecked(self._get_ini_value('Advanced', 'UseMetadata'))
        self.metadataBtnClear.clicked.connect(helpers.functions.ham)
        self.metadataBtnRebuild.clicked.connect(helpers.functions.ham)

        self._populate_list_value("Assets", "CategoryList", self.categoryList)
        self._populate_list_value("Assets", "SubfolderList", self.subfolderList)

    def _add_item_list(self, list_widget, title="..."):
        """Add item to QListWidget.

        Parameters
        ----------
        list_widget : QtWidgets.QListWidget
            QListWidget instance
        title : str
            Suffix for input dialog's title.

        Returns
        -------
        None

        """
        item = QtWidgets.QListWidgetItem()
        text, ok = QtWidgets.QInputDialog.getText(self, ("Add " + str(title)), "Name:", QtWidgets.QLineEdit.Normal, "")

        if ok and text != '':
            item.setText(str(text))
            list_widget.addItem(item)

    def _remove_item_list(self, list_widget):
        """Remove items from QListWidget.

        Parameters
        ----------
        list_widget : QtWidgets.QListWidget
            QListWidget instance

        Returns
        -------
        None

        """
        items = list_widget.selectedItems()

        # Exit early if there is no selected items!
        if not items:
            return
        for item in items:
            list_widget.takeItem(list_widget.row(item))
            return

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

    def _populate_list_value(self, section, setting, list_widget):
        value = self._get_ini_value(section, setting)
        value_list = json.loads(value)

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
        # TODO: Rework apply function to be more inclusive of every functions?
        def apply_checkbox(checkbox_widget, section, param):
            """Save checkbox value in INI after apply.

            Parameters
            ----------
            checkbox_widget : QtWidgets.QCheckBox
                QCheckbox instance
            section : str
                Section name
            param : str
                Parameter name

            Returns
            -------
            None

            """
            value = 'True' if checkbox_widget.isChecked() else 'False'
            logger.info(value)
            configurations.update_setting(INI_PATH, section, param, value)

        apply_checkbox(self.descCheck, 'Settings', 'ShowDescriptionPanel')
        apply_checkbox(self.debugCheck, 'Settings', 'ShowDebugLog')
        apply_checkbox(self.boxPrefix, 'Assets', 'UsePrefix')
        apply_checkbox(self.boxSuffix, 'Assets', 'UseSuffix')
        apply_checkbox(self.metadataCheck, 'Advanced', 'UseMetadata')

        def apply_line_value(line_widget, section, param):
            """Save line value in INI after apply.

            Parameters
            ----------
            line_widget : QtWidgets.QLineEdit
                QLineEdit instance
            section : str
                Section name
            param : str
                Parameter name

            Returns
            -------
            None

            """
            value = line_widget.text()
            logger.info(value)
            configurations.update_setting(INI_PATH, section, param, value)

        apply_line_value(self.projectPathLine, 'Settings', 'ProjectPath')
        apply_line_value(self.suffixCustomName, 'Assets', 'SuffixCustomName')

        def apply_list_value(list_widget, section, param):
            """Save list value in INI after apply.

            Parameters
            ----------
            list_widget : QtWidgets.QListWidget
                QListWidget instance
            section : str
                Section name
            param : str
                Parameter name

            Notes
            -----
            Python stores string value with single quote marks and the JSON library
            requires values to be store with double quote marks for it to load properly
            hence the replace function.

            Returns
            -------
            None

            """
            items = []
            for x in range(list_widget.count()):
                value = list_widget.item(x).text()
                items.append(value)
            logger.info(items)
            configurations.update_setting(INI_PATH, section, param, str(items).replace("'", '"'))

        apply_list_value(self.categoryList, "Assets", "CategoryList")
        apply_list_value(self.subfolderList, "Assets", "SubfolderList")

        def apply_theme():
            value = str(self.themeBtnGrp.checkedButton().text())
            logger.info(value)
            configurations.update_setting(INI_PATH, 'UI', 'Theme', value)

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

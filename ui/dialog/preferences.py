"""Preferences Dialog"""
import logging
import sys
from pathlib import Path

from PyQt5 import QtCore, QtWidgets

import helpers.functions
import ui.functions
from config import configurations
from ui.enums import (
    FontRadio,
    FontSize,
    IconRadio,
    PrefixRadio,
    PreviewRadio,
    SeparatorCombo,
    SuffixRadio,
    ThemeRadio,
)
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
        self.descCheck.setChecked(configurations.get_setting('Settings', 'ShowDescriptionPanel'))
        theme = getattr(ThemeRadio, configurations.get_setting('UI', 'Theme').upper())
        theme_radios = {
            "LIGHT": self.themeRadioLight,
            "DARK": self.themeRadioDark,
        }
        ui.functions.checked_radio(theme, theme_radios)
        font_mode = FontRadio(configurations.get_setting('UI', 'FontMode'))
        font_radios = {
            "DEFAULT": self.fontRadioDefault,
            "MONOSPACE": self.fontRadioMonospace,
            "CUSTOM": self.fontRadioCustom,
        }
        ui.functions.checked_radio(font_mode, font_radios)
        self.fontSizeComboBox.setCurrentIndex(
            self.fontSizeComboBox.findText(
                FontSize(configurations.get_setting('UI', 'FontSize')).name,
                QtCore.Qt.MatchContains,
            )
        )
        # Show blank in dropdown list if font not found
        self.fontListComboBox.setCurrentIndex(
            self.fontListComboBox.findText(
                configurations.get_setting('UI', 'Font'),
                QtCore.Qt.MatchContains,
            )
        )

        # 2.2 Setup Assets input/button here
        self.maxCharSpinner.setValue(configurations.get_setting('Assets', 'MaxChars'))
        self.separatorCombo.setCurrentIndex(
            self.separatorCombo.findText(
                configurations.get_setting('Assets', 'Separator'),
                QtCore.Qt.MatchContains,
            )
        )
        self.boxPrefix.setChecked(configurations.get_setting('Assets', 'UsePrefix'))
        prefix_type = PrefixRadio(configurations.get_setting('Assets', 'PrefixType'))
        prefix_radios = {
            "FIRST": self.prefixRadioFirst,
            "WHOLE": self.prefixRadioWhole,
        }
        ui.functions.checked_radio(prefix_type, prefix_radios)
        self.boxSuffix.setChecked(configurations.get_setting('Assets', 'UseSuffix'))
        suffix_type = SuffixRadio(configurations.get_setting('Assets', 'SuffixType'))
        suffix_radios = {
            "VERSION": self.suffixRadioVersion,
            "CUSTOM": self.suffixRadioCustomName,
        }
        ui.functions.checked_radio(suffix_type, suffix_radios)
        self.suffixVersionCombo.setCurrentIndex(configurations.get_setting('Assets', 'SuffixVersionMode'))
        self.suffixCustomName.setText(configurations.get_setting('Assets', 'SuffixCustomName'))
        self.populate_list_value(self.categoryList, "Assets", "CategoryList")
        self.categoryBtnAdd.clicked.connect(lambda: self.add_item_list(self.categoryList, "Category"))
        self.categoryBtnRemove.clicked.connect(lambda: self.remove_item_list(self.categoryList))
        self.populate_list_value(self.subfolderList, "Assets", "SubfolderList")
        self.subfolderBtnAdd.clicked.connect(lambda: self.add_item_list(self.subfolderList, "Subfolder"))
        self.subfolderBtnRemove.clicked.connect(lambda: self.remove_item_list(self.subfolderList))

        # 2.3 Setup Advanced input/button here
        preview = PreviewRadio(configurations.get_setting('Advanced', 'Preview'))
        preview_radios = {
            "SMALL": self.previewRadioSmall,
            "BIG": self.previewRadioBig,
            "CUSTOM": self.previewRadioCustom,
        }
        ui.functions.checked_radio(preview, preview_radios)
        icon = IconRadio(configurations.get_setting('Advanced', 'IconThumbnails'))
        icon_radios = {
            "ENABLE": self.iconRadioEnable,
            "DISABLE": self.iconRadioDisable,
            "GENERIC": self.iconRadioGeneric,
        }
        ui.functions.checked_radio(icon, icon_radios)
        self.previewSpinnerCustom.setValue(configurations.get_setting('Advanced', 'PreviewCustomMaxSize'))
        self.logButtonOpen.clicked.connect(helpers.functions.ham)
        self.logButtonClear.clicked.connect(helpers.functions.ham)
        self.logDebugCheck.setChecked(configurations.get_setting('Advanced', 'UseDebugLog'))

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
        text, ok = QtWidgets.QInputDialog.getText(
            self,
            f"Add {title}",
            "Name:",
            QtWidgets.QLineEdit.Normal,
            "",
        )

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

    def populate_list_value(self, list_widget: QtWidgets.QListWidget, section: str, setting: str):
        value_list = configurations.get_setting(section, setting)

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
        existing_path = Path(self.projectPathLine.text()).as_posix()

        # 1. Initialize selected directory path through QFileDialog
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            'Choose Directory',
            Path.home().as_posix(),  # Defaults to home directory
            QtWidgets.QFileDialog.ShowDirsOnly,  # Filter list to Directory only
        )

        # 2. If user cancel, revert to original value
        if not path:
            path = existing_path

        # 3. Set Project Path Line text field with new_path value
        logger.info("Selected Project Path: %s", path)
        self.projectPathLine.setText(path)

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

    def get_font(self):
        selection = self.fontBtnGrp.checkedId()
        if selection == -4:
            return self.fontListComboBox.currentText()
        return FontRadio(selection).font()

    def get_font_size(self):
        font_size = getattr(FontSize, self.fontSizeComboBox.currentText().upper())
        return font_size.value

    def apply(self):
        checkboxes = (
            (self.descCheck, "ShowDescriptionPanel"),
            (self.logDebugCheck, "UseDebugLog"),
            (self.boxPrefix, "UsePrefix"),
            (self.boxSuffix, "UseSuffix"),
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
            "Theme": ThemeRadio(self.themeBtnGrp.checkedId()).name,
            "Font": self.get_font(),
            "FontMode": self.fontBtnGrp.checkedId(),
            "FontSize": self.get_font_size(),
            "Preview": self.previewBtnGrp.checkedId(),
            "Separator": SeparatorCombo(self.separatorCombo.currentIndex()).name,
            "IconThumbnails": self.iconBtnGrp.checkedId(),
            "PrefixType": self.prefixBtnGrp.checkedId(),
            "SuffixType": self.suffixBtnGrp.checkedId(),
            "SuffixVersionMode": self.suffixVersionCombo.currentIndex(),
            "MaxChars": self.maxCharSpinner.value(),
            "PreviewCustomMaxSize": self.previewSpinnerCustom.value(),
        })
        configurations.bulk_update_settings(config)

        ui.functions.generate_stylesheet(
            font=configurations.get_setting('UI', 'Font'),
            size=self.get_font_size(),
        )
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

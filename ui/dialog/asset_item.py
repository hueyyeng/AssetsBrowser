"""Asset Item Dialog"""
import logging
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

import ui.functions
from config import configurations
from database.db import Database
from database.models import (
    Asset,
    AssetItemFormat,
    AssetItem,
    Category,
    Project,
)
from helpers.functions import ham
from helpers.utils import alert_window
from ui.window.ui_asset_item import (
    Ui_AssetItemDialog,
)

logger = logging.getLogger(__name__)


class AssetItemDialog(QtWidgets.QDialog, Ui_AssetItemDialog):
    def __init__(self, parent=None):
        super(AssetItemDialog, self).__init__(parent)
        self.setupUi(self)
        self.db = Database(use_default_db=True)
        ui.functions.set_window_icon(self)
        self._setup_ui_buttons()
        self._setup_asset_combobox()
        self._setup_format_combobox()

    def _setup_asset_combobox(self):
        """Setup Asset combobox"""
        asset_categories = configurations.get_setting('Assets', 'CategoryList')
        for asset_category in asset_categories:
            self.assetComboBox.addItem(asset_category)

    def _setup_format_combobox(self):
        """Setup Asset Format combobox"""
        asset_categories = configurations.get_setting('Assets', 'CategoryList')
        for asset_category in asset_categories:
            self.formatComboBox.addItem(asset_category)

    def _setup_ui_buttons(self):
        self.btnCreate.setDisabled(True)
        self.btnCreate.clicked.connect(ham)
        self.btnCancel.clicked.connect(self.close)


def show_dialog():
    dialog = AssetItemDialog()
    if dialog.exec_():
        logger.debug('Creating new asset item...')
    else:
        logger.debug('Aborting Create New Asset Item...')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AssetItemDialog()
    window.show()
    sys.exit(app.exec_())

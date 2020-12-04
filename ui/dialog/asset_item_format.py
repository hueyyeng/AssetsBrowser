"""Asset Item Format Dialog"""
import logging
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

import ui.functions
from database.db import Database
from database.models import (
    Asset,
    AssetItem,
    AssetItemFormat,
    Category,
    Project,
)
from helpers.functions import ham
from ui.window.ui_asset_item_format import (
    Ui_AssetItemFormatDialog,
)

logger = logging.getLogger(__name__)


class AssetItemFormatDialog(QtWidgets.QDialog, Ui_AssetItemFormatDialog):
    def __init__(self, parent=None):
        super(AssetItemFormatDialog, self).__init__(parent)
        self.setupUi(self)
        self.db = Database(use_default_db=True)
        ui.functions.set_window_icon(self)
        self._setup_ui_buttons()

    def _setup_ui_buttons(self):
        self.btnPushAdd.clicked.connect(ham)
        self.btnPushRemove.clicked.connect(ham)
        self.btnPushClear.clicked.connect(ham)


def show_dialog():
    dialog = AssetItemFormatDialog()
    if not dialog.exec_():
        logger.debug('Aborting Manage Asset Item Format...')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AssetItemFormatDialog()
    window.show()
    sys.exit(app.exec_())

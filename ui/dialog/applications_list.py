"""Applications List Dialog"""
import logging
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

import ui.functions
from database.db import Database
from database.models import (
    Application,
)
from helpers.functions import ham
from ui.window.ui_applications_list import (
    Ui_AppListDialog,
)

logger = logging.getLogger(__name__)


class AppListDialog(QtWidgets.QDialog, Ui_AppListDialog):
    def __init__(self, parent=None):
        super(AppListDialog, self).__init__(parent)
        self.setupUi(self)
        self.db = Database(use_default_db=True)
        ui.functions.set_window_icon(self)
        self._setup_ui_buttons()

    def _setup_ui_buttons(self):
        self.btnPushAdd.clicked.connect(ham)
        self.btnPushRemove.clicked.connect(ham)
        self.btnPushClear.clicked.connect(ham)


def show_dialog():
    dialog = AppListDialog()
    if not dialog.exec_():
        logger.debug('Aborting Applications List...')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AppListDialog()
    window.show()
    sys.exit(app.exec_())

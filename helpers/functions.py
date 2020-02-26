"""Assets Browser Functions"""
import logging
import os
import sys

from PyQt5 import QtCore, QtWidgets

from config.configurations import get_setting
from helpers.widgets import ColumnViewWidget

logger = logging.getLogger(__name__)


def create_column_view(
    column_view: ColumnViewWidget,
    category: str,
    project: str
):
    """Create column_view tabs.

    Create new column_view tabs to for each categories.

    Parameters
    ----------
    column_view : ColumnViewWidget
        ColumnViewWidget object.
    category : str
        Category name.
    project : str
        Project name.

    """
    default_path = (get_setting('Settings', 'ProjectPath') + project + "/Assets/" + category)
    default_path_log = "Load... " + default_path
    logger.debug(default_path_log)

    column_view.setColumnWidths([200] * 9)  # Column width multiply by the amount of columns
    column_view.setEnabled(True)
    column_view.fsm = QtWidgets.QFileSystemModel()
    column_view.fsm.setReadOnly(False)
    column_view.rootindex = column_view.fsm.setRootPath(default_path)
    column_view.setModel(column_view.fsm)
    column_view.setRootIndex(column_view.rootindex)
    column_view.clicked.connect(column_view.get_file_info)
    column_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    column_view.customContextMenuRequested.connect(column_view.context_menu)


def clear_layout(layout):
    """Clear layout?"""
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


def show_cwd():
    """Show CWD (Current Work Directory) as a QMessageBox."""
    widget = QtWidgets.QWidget()
    cwd = os.getcwd()
    QtWidgets.QMessageBox.information(widget, "Information", cwd)


def close_app():
    """Terminate/Close App."""
    sys.exit()


def restart_app():
    """Restart App.

    99% it doesn't restart in an IDE like PyCharm for complex script but
    it has been tested to work when execute through Python interpreter.

    """
    # QtWidgets.qApp.exit(-123)
    os.execv(sys.executable, [sys.executable] + sys.argv)


def ham():
    """When testing or in doubt, it's HAM time!"""
    print('HAM! HAM! HAM!')

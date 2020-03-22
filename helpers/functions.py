"""Assets Browser Functions"""
import logging
import os
import sys

from PyQt5 import QtWidgets

logger = logging.getLogger(__name__)


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

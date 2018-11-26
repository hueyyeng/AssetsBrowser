"""Utilities."""
import sys
from PyQt5 import QtGui, QtWidgets


class PyQTCheck:
    try:
        __import__('PyQt5')
        pyqt5 = True
    except ImportError:
        pyqt5 = False


def alert_window(title, text):
    """PyQt MessageBox Alert Window

    Reusable generic alert window.

    Parameters
    ----------
    title : str
        Title of the alert window.
    text : str
        Text message of the alert window.

    Returns
    -------
    None

    """
    # 1. Set up QApplication, QWidget and QMessageBox instance
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icons/logo.ico'))
    widget = QtWidgets.QWidget()
    message = QtWidgets.QMessageBox

    # 2. Move PyQt Window position to center of the screen
    qt_rectangle = widget.frameGeometry()
    center_point = QtWidgets.QDesktopWidget().availableGeometry().center()
    qt_rectangle.moveCenter(center_point)
    widget.move(qt_rectangle.topLeft())

    # 3. Display widget (alert window)
    message.warning(widget, title, text, message.Ok)
    widget.show()

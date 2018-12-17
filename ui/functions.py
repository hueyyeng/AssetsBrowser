"""UI Functions"""
import ctypes
import logging
import platform
import qdarkstyle
from PyQt5 import QtGui, QtCore, QtWidgets

from config import configurations, constants

logger = logging.getLogger(__name__)

INI_PATH = constants.INI_PATH


def set_window_icon(self, icon='icons/file.png'):
    """Set PyQt Window Icon.

    Parameters
    ----------
    icon : str
        Path to icon file.

    Returns
    -------
    None

    """
    self.setWindowIcon(QtGui.QIcon(icon))


def font_size_overrides(self, size=8, scale=1.0):
    """Overrides font sizes.

    Overrides font sizes based on platform due to PyQt quirks especially on macOS/OSX.

    Notes
    -----
    This can also override the default font size to arbitrary values although the default
    values are good enough on non HiDPI display (e.g. Windows 7).

    Parameters
    ----------
    size : int
        Set the default font size.
    scale : float
        The scale multiplier to resize the font size.

    Returns
    -------
    None

    """
    system = platform.system()
    font = QtGui.QFont()

    if system == 'Darwin':
        size = 12
        scale = 1.0
    if system == 'Linux':
        scale = 1.0

    font.setPointSize(size * scale)
    self.setFont(font)


def center_screen(self):
    """Center PyQt Window on screen."""
    resolution = QtWidgets.QDesktopWidget().screenGeometry()
    self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
              (resolution.height() / 2) - (self.frameSize().height() / 2))


def always_on_top(self):
    """Toggle AlwaysOnTop (works in Windows and Linux)."""
    if self.actionAlwaysOnTop.isChecked():
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        print("Always on Top Enabled")
    else:
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
        print("Always on Top Disabled")
    self.show()


def taskbar_icon():
    """Workaround to show setWindowIcon on Win7 taskbar instead of default Python icon."""
    if platform.system() == 'Windows':
        app_id = u'taukeke.python.assetsbrowser'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)


def hidpi_check(app):
    """HiDPI check for QApplication.

    Parameters
    ----------
    app : PyQt5.QtWidgets.QApplication

    Returns
    -------
    None

    """
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        logger.info('High DPI Scaling Enabled')
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
        logger.info('High DPI Pixmaps Enabled')


def theme_loader(app):
    """Theme loader for QApplication.

    Parameters
    ----------
    app : PyQt5.QtWidgets.QApplication

    Returns
    -------
    None

    """
    theme = configurations.get_setting(INI_PATH, "UI", "Theme")
    if theme == "Default (Light)":
        app.setStyle('Fusion')
    if theme == "Dark":
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

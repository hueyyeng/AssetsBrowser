"""UI Functions"""
import ctypes
import logging
import platform
from PyQt5 import QtGui, QtCore, QtWidgets

logger = logging.getLogger(__name__)


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

    font_size = size
    font.setPointSize(font_size * scale)
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
        PyQt QtWidgets QApplication object.

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

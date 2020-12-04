"""UI Functions"""
import ctypes
import logging
import platform
from enum import Enum
from pathlib import Path

import qdarkstyle
from PyQt5 import QtCore, QtGui, QtWidgets

from config import configurations
from config.constants import ICON_FILE

logger = logging.getLogger(__name__)


def set_window_icon(widget: QtWidgets.QWidget, icon=None):
    """Set PyQt Window Icon

    Parameters
    ----------
    widget : QtWidgets.QWidget
    icon : str or None
        Path to icon file. If None, use default icon (file.png)

    """
    if not icon:
        icon = Path.cwd() / 'ui' / 'icons' / ICON_FILE
    widget.setWindowIcon(QtGui.QIcon(str(icon)))


def set_font_scale(widget: QtWidgets.QWidget, size=None, scale=1.0):
    """Set font scale

    Adjust font scaling (and optionally size) for HiDPI display (e.g. macOS devices).

    Notes
    -----
    This can also override the default font size to arbitrary values although the default
    values are good enough on non HiDPI display (e.g. Windows 7).

    Parameters
    ----------
    widget : QtWidgets.QWidget
    size : int
        Set the default font size. If None, use FontSize value from TOML settings.
    scale : float
        The scale multiplier to resize the font size.

    """
    font = QtGui.QFont()
    if not size:
        size = configurations.get_setting('UI', 'FontSize')

    system = platform.system()
    # TODO: Get access to macOS device with Retina display
    if system == 'Darwin':
        scale = 1.0
    elif system == 'Linux':
        scale = 1.0

    font.setPointSize(size * scale)
    widget.setFont(font)


def center_screen(widget: QtWidgets.QWidget):
    """Center PyQt Window on screen"""
    resolution = QtWidgets.QDesktopWidget().screenGeometry()
    widget.move((resolution.width() / 2) - (widget.frameSize().width() / 2),
                (resolution.height() / 2) - (widget.frameSize().height() / 2))


def always_on_top(widget: QtWidgets.QWidget):
    """Toggle AlwaysOnTop (works in Windows and Linux)"""
    widget.setWindowFlags(widget.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
    checked = widget.actionAlwaysOnTop.isChecked()
    if checked:
        widget.setWindowFlags(widget.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
    logger.debug('Always on Top Enabled' if checked else 'Always on Top Disabled')
    widget.show()


def taskbar_icon():
    """Workaround to show setWindowIcon on Win7 taskbar instead of default Python icon"""
    if platform.system() == 'Windows':
        app_id = u'taukeke.python.assetsbrowser'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)


def enable_hidpi(app):
    """Enable HiDPI support for QApplication.

    Parameters
    ----------
    app : QtWidgets.QApplication

    """
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    logger.info('High DPI Scaling and Pixmaps Enabled')


def theme_loader(app):
    """Theme loader for QApplication.

    Parameters
    ----------
    app : QtWidgets.QApplication

    """
    theme = configurations.get_setting("UI", "Theme")
    if theme == "LIGHT":
        app.setStyle('Fusion')
    if theme == "DARK":
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


def generate_stylesheet(font=None, size=12):
    """Generate/update stylesheet for QApplication

    Handle font-family and font-size for users working with different
    language like Japanese, Traditional/Simplified Chinese, etc

    Parameters
    ----------
    font : str or None
        Font name. If None, use system default font
    size : int
        Font size

    """
    font_db = QtGui.QFontDatabase()
    if not font or font == 'sans-serif':
        font = font_db.systemFont(font_db.GeneralFont).family()
    elif font == 'monospace':
        font = font_db.systemFont(font_db.FixedFont).family()

    css = (
        "QWidget { "
        f"font-family: '{font}'; "
        f"font-size: {size}px; "
        "}"
    )
    css_path = Path(__file__).parent / 'stylesheet.css'
    with open(css_path, 'w') as f:
        f.write(css)


def checked_radio(enum: Enum, radios: dict):
    """Checked radio button

    Retrieve the QRadioButton to be check

    Parameters
    ----------
    enum : Enum
    radios : dict
        Dict mapping must have the following key value pairs
        - Key: Enum name
        - Value: QRadioButton

    """
    radio = radios.get(enum.name)
    radio.setChecked(True)

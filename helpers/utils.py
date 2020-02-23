"""Utilities"""
import os
import platform
import subprocess
import sys

from PyQt5 import QtGui, QtWidgets

from config import configurations
from helpers.exceptions import InvalidProjectPath


def alert_window(title: str, text: str):
    """PyQt MessageBox Alert Window

    Reusable generic alert window.

    Parameters
    ----------
    title : str
        Title of the alert window.
    text : str
        Text message of the alert window.

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


def valid_project_path(toml: str, project: str):
    """Check path validity and update TOML if invalid.

    Check if PROJECT_PATH is valid and reset to home directory if error.

    A warning message will pop up to inform user that the Project Path has
    been reset to the user's home directory.

    Parameters
    ----------
    toml : str
        Path to TOML file.
    project : str
        Path to project directory.

    Raises
    ------
    InvalidProjectPath
        If project path value in TOML is invalid.

    """
    exists = os.path.exists(project)
    if not exists:
        # 1. Set Project Path to User's Home directory
        home = os.path.expanduser('~')
        system = platform.system()
        if system == 'Darwin' or 'Linux':
            home = (home + '/')
        if system == 'Windows':
            home = (home + '\\')

        # 2. Update ProjectPath in TOML with User's Home directory path
        configurations.update_setting(
                    toml,
                    'Settings',
                    'ProjectPath',
                    home,
        )

        #  3. Raise Alert Window
        warning_text = (
                "Project Path doesn't exists!\n"
                + "\n"
                + "Project Path has been set to " + home + " temporarily.\n"
                + "\n"
                + "Please restart Assets Browser."
        )
        alert_window('Warning', warning_text)
        raise InvalidProjectPath(project)


def get_file_size(size: int or float, precision=2) -> str:
    """Get file size.

    Refactor from https://stackoverflow.com/a/32009595/8337847

    Parameters
    ----------
    size : int or float
        The file size value.
    precision : int
        The decimal place.

    Returns
    -------
    str
        The formatted message of the file size.

    See Also
    --------
    hurry.file_size : https://pypi.python.org/pypi/hurry.file_size/

    """
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    suffix_index = 0
    while size > 1024 and suffix_index < 4:
        suffix_index += 1   # Increment the index of the suffix
        size = size / 1024  # Apply the division
    # Return using String formatting. f for float and s for string.
    return "%.*f %s" % (precision, size, suffixes[suffix_index])


def reveal_in_os(path: str):
    """Reveal in OS.

    Reveal the file/directory path using the OS File Manager.

    Parameters
    ----------
    path : str
        The path of the file/directory.

    """
    system = platform.system()
    win_path = path.replace("/", "\\")

    # Default to macOS since no extra handling
    cmd = (['open', '-R', path])

    if system == 'Windows' and os.path.isdir(path):
        cmd = str('explorer /e,' + win_path)
    elif system == 'Windows' and os.path.exists(path):
        cmd = str('explorer /select,' + win_path)
    elif system == 'Linux':
        dir_path = '/'.join(path.split('/')[0:-1])  # Omit file_name from path
        # subprocess.Popen(['xdg-open', dir_path])
        cmd = (['xdg-open', dir_path])

    subprocess.call(cmd)


def open_file(target: str):
    """ Open selected file using the OS associated program.

    Parameters
    ----------
    target : str
        Path to file/directory.

    """
    system = platform.system()
    try:
        os.startfile(target)
    except OSError:
        if system == 'Linux':
            subprocess.call(['xdg-open', target])
        if system == 'Darwin':
            subprocess.call(['open', target])

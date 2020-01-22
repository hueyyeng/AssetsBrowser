"""Assets Browser Functions"""
import os
import sys
import logging
import platform
import subprocess

from PyQt5 import QtGui, QtCore, QtWidgets
from config import configurations, constants
from helpers.exceptions import InvalidProjectPath
from helpers.utils import alert_window

logger = logging.getLogger(__name__)

# Set Path from INI file
PROJECT_PATH = constants.PROJECT_PATH
INI_PATH = constants.INI_PATH

# File/Directory Path Dictionary for easy access by any methods
# TODO: Might want to move to constants.py
selected_path = {'Path': ''}
selected_file = {'File': ''}
file_manager = {
    'Windows': 'Explorer',
    'Darwin': 'Finder',
    'Linux': 'File Manager',
}


def create_tabs(self, categories, project):
    """Create QColumnView tabs.

    Create QColumnView tabs dynamically from Assets' List.

    Parameters
    ----------
    categories : :obj:`list` of :obj:`str`
        Array of categories in str format.
    project : str
        The project name.

    """
    for category in categories:
        self.tab = QtWidgets.QWidget()
        self.column_view = QtWidgets.QColumnView(self.tab)
        self.column_view.setAlternatingRowColors(False)
        self.column_view.setResizeGripsVisible(True)

        self.assets["column_view{0}".format(category)] = self.column_view

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.addWidget(self.column_view)

        self.tabWidget.addTab(self.tab, category)
        column_views(self.column_view, category, project)


def preview_widget(widget, tab):
    """Preview widget.

    Preview widget using QtWidgets for column_view tab.

    Parameters
    ----------
    widget : QtWidgets.QWidget
        QtWidget object.
    tab : QtWidgets.QColumnView
        QColumnView object.


    """
    # File Category Labels
    category_name = QtWidgets.QLabel('Name:')
    category_size = QtWidgets.QLabel('Size:')
    category_type = QtWidgets.QLabel('Type:')
    category_date = QtWidgets.QLabel('Modified:')

    # File Attributes Labels
    tab.file_name = QtWidgets.QLabel()
    tab.file_size = QtWidgets.QLabel()
    tab.file_type = QtWidgets.QLabel()
    tab.file_date = QtWidgets.QLabel()

    # Align Right for Prefix Labels
    align_right = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
    category_name.setAlignment(align_right)
    category_size.setAlignment(align_right)
    category_type.setAlignment(align_right)
    category_date.setAlignment(align_right)

    # File Attributes Layout and Value for Preview Pane
    sublayout_text = QtWidgets.QGridLayout()
    sublayout_text.addWidget(category_name, 0, 0)
    sublayout_text.addWidget(category_size, 1, 0)
    sublayout_text.addWidget(category_type, 2, 0)
    sublayout_text.addWidget(category_date, 3, 0)
    sublayout_text.addWidget(tab.file_name, 0, 1)
    sublayout_text.addWidget(tab.file_size, 1, 1)
    sublayout_text.addWidget(tab.file_type, 2, 1)
    sublayout_text.addWidget(tab.file_date, 3, 1)
    sublayout_text.setRowStretch(4, 1)  # Arrange layout to upper part of widget

    # Preview Thumbnails
    tab.preview = QtWidgets.QLabel()
    sublayout_thumbnail = QtWidgets.QVBoxLayout()
    sublayout_thumbnail.addWidget(tab.preview)
    sublayout_thumbnail.setAlignment(QtCore.Qt.AlignCenter)

    # Set Preview Pane to Qcolumn_view setPreviewWidget
    preview_pane = QtWidgets.QVBoxLayout(widget)
    preview_pane.addLayout(sublayout_thumbnail)
    preview_pane.addLayout(sublayout_text)

    tab.setPreviewWidget(widget)


def column_views(column_view, category, project):
    """Create column_view tabs.

    Create new column_view tabs to for each categories.

    Parameters
    ----------
    column_view : QtWidgets.QColumnView
        QColumnView object.
    category : str
        Category name.
    project : str
        Project name.


    """
    default_path = (PROJECT_PATH + project + "/Assets/" + category)
    default_path_log = "Load... " + default_path
    logger.debug(default_path_log)

    tab = column_view
    tab.setColumnWidths([200] * 9)  # Column width multiply by the amount of columns
    tab.setEnabled(True)
    tab.fsm = QtWidgets.QFileSystemModel()
    tab.fsm.setReadOnly(False)
    tab.rootindex = tab.fsm.setRootPath(default_path)
    tab.setModel(tab.fsm)
    tab.setRootIndex(tab.rootindex)

    preview_widget(QtWidgets.QWidget(), tab)

    # Return selected item attributes in Model View for Preview Pane
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def get_file_info(index):
        """Get file info.

        Retrieve file information for display in Preview tab.

        Parameters
        ----------
        index : QtCore.QModelIndex
            QModelIndex using decorator method.

        Returns
        -------
        str
            File path.

        """
        index_item = tab.fsm.index(index.row(), 0, index.parent())

        # Retrieve File Attributes
        file_name = str(tab.fsm.fileName(index_item))
        file_size = tab.fsm.size(index_item)
        file_type = str(tab.fsm.type(index_item))
        file_date = tab.fsm.lastModified(index_item)
        file_path = str(tab.fsm.filePath(index_item))

        selected_file['File'] = file_name
        selected_path['Path'] = file_path

        # Split file_type into array for easy formatting
        file_type_list = file_type.split(' ')

        # Assign the File Attributes' string into respective labels
        tab.file_name.setText(file_name)
        tab.file_size.setText(get_file_size(file_size))
        tab.file_type.setText(file_type_list[0].upper() + ' file')
        tab.file_date.setText(file_date.toString('yyyy/MM/dd h:m AP'))

        # Retrieve file_path for Thumbnail Preview in __init__
        image_path = tab.fsm.filePath(index_item)
        image_type = file_type[0:-5]
        image_types = constants.IMAGE_FORMAT

        # Generate thumbnails for Preview Pane
        max_size = 150  # Thumbnails max size in pixels
        thumbnail_object = QtGui.QPixmap()
        thumbnail_object.load(image_path)
        if image_type in image_types:
            thumbnail = thumbnail_object.scaled(
                max_size,
                max_size,
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation,
            )
        else:
            file_info = QtCore.QFileInfo(image_path)  # Retrieve info like icons, path, etc
            file_icon = QtWidgets.QFileIconProvider().icon(file_info)
            thumbnail = file_icon.pixmap(48, 48, QtGui.QIcon.Normal, QtGui.QIcon.Off)

        tab.preview.setPixmap(thumbnail)
        return file_path

    tab.clicked.connect(get_file_info)

    def open_menu(position):
        menu = QtWidgets.QMenu()
        open_action = menu.addAction('Open ' + selected_file['File'])
        open_action.triggered.connect(lambda: open_file(selected_path['Path']))
        reveal_action = menu.addAction(('Reveal in ' + file_manager[platform.system()]))
        reveal_action.triggered.connect(lambda: reveal_in_os(selected_path['Path']))
        menu.addSeparator()
        quit_action = menu.addAction("Quit")
        quit_action.triggered.connect(QtWidgets.QApplication.quit)
        menu.exec_(tab.mapToGlobal(position))

    tab.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    tab.customContextMenuRequested.connect(open_menu)


def project_list(self):
    """List Project directories in PROJECT_PATH comboBox.

    Retrieve directories in PROJECT_PATH comboBox, clear existing tabs and create new tabs.

    """
    # 1. Update INI CurrentProject with chosen project from comboBox
    project = self.comboBox.currentText()
    configurations.update_setting(INI_PATH, 'Settings', 'CurrentProject', project)

    # 2. Clear all tabs except Help
    count = 0
    while count < 10:
        count = count + 1
        self.tabWidget.removeTab(1)

    # 3. Force clear existing self.category and self.assets value
    self.category = []
    self.assets = {}

    # 4. Populate self.category list with valid Assets directory name
    assets_path = (PROJECT_PATH + project + "/Assets/")
    for item in os.listdir(assets_path):
        prefix = item.startswith(('_', '.'))
        is_directory = os.path.isdir(os.path.join(assets_path, item))
        if not prefix and is_directory:
            self.category.append(item)

    # 5. Create tabs using self.category list and selected project
    create_tabs(self, self.category, project)


def valid_path(ini, project):
    """Check path validity and update INI if invalid.

    Check if PROJECT_PATH is valid and reset to home directory if error.

    A warning message will pop up to inform user that the Project Path has
    been reset to the user's home directory.

    Parameters
    ----------
    ini : str
        Path to INI file.
    project : str
        Path to project directory.

    Raises
    ------
    InvalidProjectPath
        If project path value in INI is invalid.

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

        # 2. Update ProjectPath in INI with User's Home directory path
        configurations.update_setting(
                    ini,
                    'Settings',
                    'ProjectPath',
                    home.replace('\\', '/'),
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


def clear_layout(layout):
    """Clear layout?"""
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


def show_debug(self):
    """Toggle Debug Display."""
    text = self.textEdit
    if self.checkBoxDebug.isChecked():
        text.clear()
        text.setHidden(False)
        text.setEnabled(True)
    else:
        text.setHidden(True)
        text.setEnabled(False)


def get_file_size(size, precision=2):
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


def reveal_in_os(path):
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


def open_file(target):
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
    os.execv(sys.executable, [sys.executable] + sys.argv)


def ham():
    """When testing or in doubt, it's HAM time!"""
    print('HAM! HAM! HAM!')

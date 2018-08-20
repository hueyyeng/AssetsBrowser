# -*- coding: utf-8 -*-
import os
import sys
import ctypes
import platform
import subprocess
from config import configurations
from PyQt5 import QtGui, QtCore, QtWidgets

# Set Path from INI file
PROJECTPATH = configurations.PROJECTPATH
INI_PATH = configurations.INI_PATH

# File/Directory Path Dictionary for easy access by any methods
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

    Returns
    -------
    None

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


# Create new column_view tabs to for each categories
def column_views(column_view, category, project_name):   
    project = project_name
    default_path = (PROJECTPATH + project + "/Assets/" + category)
    column_width = [
                    200,
                    200,
                    200,
                    200, 
                    200, 
                    200, 
                    200, 
                    200, 
                    200,
                   ]

    if os.path.isdir(default_path):
        print("Load..." + default_path)
        column_view.setEnabled(True)

        tab = column_view

        tab.fsm = QtWidgets.QFileSystemModel()
        tab.fsm.setReadOnly(False)
        tab.rootindex = tab.fsm.setRootPath(default_path)
        tab.setModel(tab.fsm)
        tab.setRootIndex(tab.rootindex)

        # List for Column Width for QColumnView
        tab.setColumnWidths(column_width)

        # Return selected item attributes in Model View for Preview Pane
        @QtCore.pyqtSlot(QtCore.QModelIndex)
        def get_file_info(index):
            index_item = tab.fsm.index(index.row(), 0, index.parent())

            # Retrieve File Attributes
            file_name = str(tab.fsm.fileName(index_item))
            file_size = tab.fsm.size(index_item)
            file_type = str(tab.fsm.type(index_item))
            file_date = tab.fsm.lastModified(index_item)
            file_path = str(tab.fsm.filePath(index_item))

            # Split file_type into array for easy formatting
            file_type_list = file_type.split(' ')

            # Format the File Attributes into String
            file_name_label = file_name
            file_size_label = get_file_size(file_size)
            file_type_label = file_type_list[0].upper() + ' file'
            file_date_label = file_date.toString(
                                                'yyyy/MM/dd'
                                                + ' '
                                                + 'h:m AP'
                                                )

            # Assign the File Attributes' String into respective labels
            tab.file_name.setText(file_name_label)
            tab.file_size.setText(file_size_label)
            tab.file_type.setText(file_type_label)
            tab.file_date.setText(file_date_label)

            selected_path['Path'] = file_path
            selected_file['File'] = file_name

            # Retrieve file_path for Thumbnail Preview in __init__
            pic_path = tab.fsm.filePath(index_item)
            pic_type = file_type[0:-5]

            pic_types = [
                        'jpg',
                        'jpeg',
                        'bmp',
                        'png',
                        'gif',
                        'bmp',
                        'ico',
                        'tga',
                        'tif',
                        'tiff',
                        ]

            # Omit format that doesn't work on specific OS
            system = platform.system()
            if system == 'Darwin':
                # pic_types.remove('gif')
                pic_types.remove('ico')

            # Generate thumbnails for Preview Pane
            for each in pic_types:
                thumb_max_size = 150  # Thumbnails max size in pixels

                if each.lower() == pic_type.lower():
                    tb = QtGui.QPixmap()
                    tb.load(pic_path)
                    tb_scaled = tb.scaled(
                                thumb_max_size,
                                thumb_max_size,
                                QtCore.Qt.KeepAspectRatio,
                                QtCore.Qt.SmoothTransformation,
                                )
                    tab.pvThumbs.setPixmap(tb_scaled)
                    break
                else:
                    file_info = QtCore.QFileInfo(pic_path)  # Retrieve info like icons, path, etc
                    file_icon = QtWidgets.QFileIconProvider().icon(file_info)
                    icon = file_icon.pixmap(48, 48, QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    tab.pvThumbs.setPixmap(icon)

            return file_path

        # When an item clicked in the column_view tab, execute get_file_info method
        tab.clicked.connect(get_file_info)

        # ContextMenu (Right Click Menu)
        tab.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

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

        # When Right Click, execute open_menu
        tab.customContextMenuRequested.connect(open_menu)

        # Preview widget layout and features goes here as a function
        def preview(widget, preview_tab):
            # File Category Labels
            category_name = QtWidgets.QLabel('Name:')
            category_size = QtWidgets.QLabel('Size:')
            category_type = QtWidgets.QLabel('Type:')
            category_date = QtWidgets.QLabel('Modified:')

            # File Attributes Labels
            preview_tab.file_name = QtWidgets.QLabel()
            preview_tab.file_size = QtWidgets.QLabel()
            preview_tab.file_type = QtWidgets.QLabel()
            preview_tab.file_date = QtWidgets.QLabel()

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
            sublayout_text.addWidget(preview_tab.file_name, 0, 1)
            sublayout_text.addWidget(preview_tab.file_size, 1, 1)
            sublayout_text.addWidget(preview_tab.file_type, 2, 1)
            sublayout_text.addWidget(preview_tab.file_date, 3, 1)
            sublayout_text.setRowStretch(4, 1)  # Arrange layout to upper part of widget

            # Preview Thumbnails (pvThumbs)
            preview_tab.pvThumbs = QtWidgets.QLabel()
            sublayout_pic = QtWidgets.QVBoxLayout()
            sublayout_pic.addWidget(preview_tab.pvThumbs)
            sublayout_pic.setAlignment(QtCore.Qt.AlignCenter)

            # Set Preview Pane to Qcolumn_view setPreviewWidget
            preview_pane = QtWidgets.QVBoxLayout(widget)
            preview_pane.addLayout(sublayout_pic)
            preview_pane.addLayout(sublayout_text)

            preview_tab.setPreviewWidget(widget)

        preview_widget = QtWidgets.QWidget()
        preview(preview_widget, tab)

    else:
        print(default_path + " doesn't exists!")
        column_view.setDisabled(True)


# Retrieve directories in PROJECTPATH comboBox, clear existing tabs and create new tabs
def project_list(self):
    project = self.comboBox.currentText()
    configurations.update_setting(INI_PATH, 'Settings', 'CurrentProject', project)

    # Clear all tabs except Help
    count = 0
    while count < 10:
        count = count + 1
        self.tabWidget.removeTab(1)

    # Force clear existing self.category and self.assets value
    self.category = []
    self.assets = {}

    category = self.category
    assets_path = (PROJECTPATH + project + "/Assets/")

    for item in os.listdir(assets_path):
        if not item.startswith(('_', '.')) and os.path.isdir(os.path.join(assets_path, item)):
            category.append(item)

    create_tabs(self, category, project)


# Check if PROJECTPATH is valid and reset to home directory if error
def valid_path(INI_PATH, PROJECTPATH):
    exists = os.path.exists(PROJECTPATH)
    if exists:
        print("Project Path is valid.")
    else:
        home = os.path.expanduser('~')
        system = platform.system()
        if system == 'Darwin':
            home = (home + '/')
        if system == 'Windows':
            home = (home + '\\')
        configurations.update_setting(
                    INI_PATH,
                    'Settings',
                    'ProjectPath',
                    home.replace('\\', '/'),
        )

        # Move PyQt Window position to center of the screen
        app = QtWidgets.QApplication(sys.argv)
        app.setWindowIcon(QtGui.QIcon('icons/logo.ico'))

        widget = QtWidgets.QWidget()
        message = QtWidgets.QMessageBox

        qt_rectangle = widget.frameGeometry()
        center_point = QtWidgets.QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        widget.move(qt_rectangle.topLeft())

        warning_text = (
                "Project Path doesn't exists!"
                + "\n\nProject Path has been set to " + home + " temporarily."
                + "\n\nPlease restart Assets Browser."
        )
        message.warning(widget, 'Warning', warning_text, message.Ok)
        widget.show()
    return exists


# Clear Layout?
def clear_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


# Toggle Debug Display
def show_debug(self):
    text = self.textEdit
    if self.checkBoxDebug.isChecked():
        text.clear()
        text.setHidden(False)
        text.setEnabled(True)
    else:
        text.setHidden(True)
        text.setEnabled(False)


# Toggle AlwaysOnTop (works in Windows and Linux)
def always_on_top(self):
    if self.actionAlwaysOnTop.isChecked():
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        print("Always on Top Enabled")
    else:
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
        print("Always on Top Disabled")
    self.show()


# Center PyQt Window on screen
def center_screen(self):
    resolution = QtWidgets.QDesktopWidget().screenGeometry()
    self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
              (resolution.height() / 2) - (self.frameSize().height() / 2))


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


# Reveal in OS (works across all major platform)
def reveal_in_os(path):
    system = platform.system()
    if system == 'Windows':
        win_path = path.replace("/", "\\")
        if os.path.isdir(path):
            cmd = str('explorer /e,' + win_path)
            subprocess.call(cmd)
        elif os.path.exists(path):
            cmd = str('explorer /select,' + win_path)
            subprocess.call(cmd)
        else:
            print('Is this a valid OS?')
    if system == 'Darwin':  # OSX/macOS
        subprocess.call(['open', '-R', path])
    if system == 'Linux':
        dir_path = '/'.join(path.split('/')[0:-1])  # Omit file_name from path
        subprocess.Popen(['xdg-open', dir_path])
    else:
        print('FILE/DIRECTORY IS NOT VALID!')


# Overrides font sizes based on platform due to PyQt quirks especially on macOS/OSX
def font_overrides(self):
    system = platform.system()
    font = QtGui.QFont()
    if system == 'Darwin':
        font.setPointSize(8 * 1.2)
        self.setFont(font)
    elif system == 'Linux':
        font.setPointSize(8 * 1.0)
        self.setFont(font)


# Set Icon for PyQt Window for consistent look
def window_icon(self):
    self.setWindowIcon(QtGui.QIcon('icons/file.png'))


# Open selected file using the OS associated program
def open_file(target):
    system = platform.system()
    if system == 'Linux':
        subprocess.call(['xdg-open', target])
    if system == 'Darwin':
        subprocess.call(['open', target])
    else:
        os.startfile(target)


# Check High DPI Support
def high_dpi_check():
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        print('High DPI Scaling Enabled')
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
        print('High DPI Pixmaps Enabled')


# Workaround to show setWindowIcon on Win7 taskbar instead of default Python icon
def taskbar_icon():
    if platform.system() == 'Windows':
        app_id = u'taukeke.python.assetsbrowser'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)


# Show CWD (Current Work Directory) as a QMessageBox
def show_cwd():
    widget = QtWidgets.QWidget()
    cwd = os.getcwd()
    QtWidgets.QMessageBox.information(widget, "Information", cwd)


# Terminate/Close App
def close_app():
    sys.exit()


# Restart App (often 99% it doesn't restart in an IDE like PyCharm for complex
# script but it has been tested to work when execute through Python interpreter
def restart_app():
    os.execv(sys.executable, [sys.executable] + sys.argv)


# When testing or in doubt, it's HAM time!
def ham():
    print('HAM! HAM! HAM!')

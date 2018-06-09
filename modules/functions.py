# -*- coding: utf-8 -*-
import os
import sys
import ctypes
import platform
import subprocess
from modules import prefsConfig
from PyQt5 import QtGui, QtCore, QtWidgets

# Set Path from INI file
PROJECTPATH = prefsConfig.PROJECTPATH
INI_PATH = prefsConfig.INI_PATH

# File/Directory Path Dictionary for easy access by any methods
selected_path = {'Path': ''}
selected_file = {'File': ''}
file_manager = {'Windows': 'Explorer',
                'Darwin': 'Finder',
                'Linux': 'File Manager'}

# Declare global var here
colwidth = [200, 200, 200, 200, 200, 200, 200, 200, 200]


# Create Tabs Dynamically from Assets' List
def create_tabs(self, category, projectname):
    c = category
    p = projectname

    for each in c:
        self.tab = QtWidgets.QWidget()

        self.columnView = QtWidgets.QColumnView(self.tab)
        self.assets["columnView{0}".format(each)] = self.columnView
        self.columnView.setAlternatingRowColors(False)
        self.columnView.setResizeGripsVisible(True)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.addWidget(self.columnView)

        self.tabWidget.addTab(self.tab, each)

        columnview_tabs(self.columnView, each, p)

    # DEBUG USE
    # keys = sorted(self.assets.keys())
    # print(keys)


# Create new ColumnView tabs to for each categories
def columnview_tabs(columnview, category, projectname):
    project = projectname
    defaultpath = (PROJECTPATH + project + "/Assets/" + category)

    if os.path.isdir(defaultpath):
        print("Load..." + defaultpath)
        columnview.setEnabled(True)

        tab = columnview

        tab.fsm = QtWidgets.QFileSystemModel()
        tab.fsm.setReadOnly(False)
        tab.rootindex = tab.fsm.setRootPath(defaultpath)
        tab.setModel(tab.fsm)
        tab.setRootIndex(tab.rootindex)

        # List for Column Width for QColumnView
        tab.setColumnWidths(colwidth)

        # Return selected item attributes in Model View for Preview Pane
        @QtCore.pyqtSlot(QtCore.QModelIndex)
        def get_fileinfo(index):
            indexItem = tab.fsm.index(index.row(), 0, index.parent())

            # Retrieve File Attributes
            fileName = str(tab.fsm.fileName(indexItem))
            fileSize = tab.fsm.size(indexItem)
            fileType = str(tab.fsm.type(indexItem))
            fileDate = tab.fsm.lastModified(indexItem)

            filePath = str(tab.fsm.filePath(indexItem))

            # Split fileType into array for easy formatting
            ftl = fileType.split(' ')

            # Format the File Attributes into String
            fileNameLabel = fileName
            fileSizeLabel = get_filesize(fileSize)
            fileTypeLabel = ftl[0].upper() + ' file'
            # fileTypeLabel = fileType
            fileDateLabel = fileDate.toString('yyyy/MM/dd' + ' ' + 'h:m AP')

            # Assign the File Attributes' String into respective labels
            tab.filename.setText(fileNameLabel)
            tab.filesize.setText(fileSizeLabel)
            tab.filetype.setText(fileTypeLabel)
            tab.filedate.setText(fileDateLabel)

            # For Debug Panel (feel free to comment/remove it)
            print(fileNameLabel)
            print(fileSizeLabel)
            print(fileTypeLabel)
            print(fileDateLabel)

            selected_path['Path'] = filePath
            selected_file['File'] = fileName
            # print selected_path['Path']
            # print selected_file['File']

            # Retrieve filePath for Thumbnail Preview in __init__
            picPath = tab.fsm.filePath(indexItem)
            picType = fileType[0:-5]

            picTypes = ['jpg', 'jpeg', 'bmp', 'png', 'gif', 'bmp', 'ico', 'tga', 'tif', 'tiff']

            # Omit format that doesn't on specific OS
            system = platform.system()
            if system == 'Darwin':
                # picTypes.remove('gif')
                picTypes.remove('ico')

            # Generate thumbnails for Preview Pane
            for each in picTypes:
                max_size = 150  # Thumbnails max size in pixels

                if each.lower() == picType.lower():
                    tb = QtGui.QPixmap()
                    tb.load(picPath)
                    tb_scaled = tb.scaled(max_size, max_size,
                                          QtCore.Qt.KeepAspectRatio,
                                          QtCore.Qt.SmoothTransformation)

                    tab.pvThumbs.setPixmap(tb_scaled)
                    break

                else:
                    fileInfo = QtCore.QFileInfo(picPath)  # Retrieve info like icons, path, etc
                    fileIcon = QtWidgets.QFileIconProvider().icon(fileInfo)
                    icon = fileIcon.pixmap(48, 48, QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    # icon_scaled = icon.scaled(max_size, max_size,
                    #                           QtCore.Qt.KeepAspectRatio,
                    #                           QtCore.Qt.SmoothTransformation)

                    tab.pvThumbs.setPixmap(icon)

            return filePath

        # When an item clicked in the columnView tab, execute get_fileinfo method
        tab.clicked.connect(get_fileinfo)

        # ContextMenu (Right Click Menu)
        tab.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        def openMenu(position):
            menu = QtWidgets.QMenu()

            openAction = menu.addAction('Open ' + selected_file['File'])
            openAction.triggered.connect(lambda: open_file(selected_path['Path']))

            revealAction = menu.addAction(('Reveal in ' + file_manager[platform.system()]))
            revealAction.triggered.connect(lambda: reveal_os(selected_path['Path']))

            menu.addSeparator()

            quitAction = menu.addAction("Quit")
            quitAction.triggered.connect(QtWidgets.QApplication.quit)

            menu.exec_(tab.mapToGlobal(position))

        # When Right Click, execute openMenu
        tab.customContextMenuRequested.connect(openMenu)

        # Preview widget layout and features goes here as a function
        def preview(widget, preview_tab):

            # -------------------- TEXT LABELS STARTS HERE -------------------- #

            # File Category Labels
            catName = QtWidgets.QLabel('Name:')
            catSize = QtWidgets.QLabel('Size:')
            catType = QtWidgets.QLabel('Type:')
            catDate = QtWidgets.QLabel('Modified:')

            # File Attributes Labels
            preview_tab.filename = QtWidgets.QLabel()
            preview_tab.filesize = QtWidgets.QLabel()
            preview_tab.filetype = QtWidgets.QLabel()
            preview_tab.filedate = QtWidgets.QLabel()

            # Align Right for Prefix Labels
            align_right = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter

            catName.setAlignment(align_right)
            catSize.setAlignment(align_right)
            catType.setAlignment(align_right)
            catDate.setAlignment(align_right)

            # File Attributes Layout
            sublayout_text = QtWidgets.QGridLayout()

            sublayout_text.addWidget(catName, 0, 0)
            sublayout_text.addWidget(catSize, 1, 0)
            sublayout_text.addWidget(catType, 2, 0)
            sublayout_text.addWidget(catDate, 3, 0)

            # File Attributes Value for Preview Pane
            sublayout_text.addWidget(preview_tab.filename, 0, 1)
            sublayout_text.addWidget(preview_tab.filesize, 1, 1)
            sublayout_text.addWidget(preview_tab.filetype, 2, 1)
            sublayout_text.addWidget(preview_tab.filedate, 3, 1)

            # Arrange layout to upper part of widget
            sublayout_text.setRowStretch(4, 1)

            # -------------------- THUMBNAILS STARTS HERE -------------------- #

            # Preview Thumbnails (pvThumbs)
            preview_tab.pvThumbs = QtWidgets.QLabel()

            sublayout_pic = QtWidgets.QVBoxLayout()
            sublayout_pic.addWidget(preview_tab.pvThumbs)
            sublayout_pic.setAlignment(QtCore.Qt.AlignCenter)

            # -------------------- PREVIEW PANE STARTS HERE -------------------- #

            # Set Preview Pane to QColumnView setPreviewWidget
            preview_pane = QtWidgets.QVBoxLayout(widget)
            preview_pane.addLayout(sublayout_pic)
            preview_pane.addLayout(sublayout_text)

            preview_tab.setPreviewWidget(widget)

        preview_widget = QtWidgets.QWidget()
        preview(preview_widget, tab)

    else:
        print(defaultpath + " doesn't exists!")
        columnview.setDisabled(True)


# Retrieve directories in PROJECTPATH comboBox, clear existing tabs and create new tabs
def project_list(self):
    project = self.comboBox.currentText()
    prefsConfig.update_setting(INI_PATH, 'Settings', 'CurrentProject', project)

    # Clear all tabs except Help
    count = 0

    while count < 10:
        count = count + 1
        self.tabWidget.removeTab(1)

    # Force clear existing self.category and self.assets value
    self.category = []
    self.assets = {}

    cat = self.category
    ASSETSPATH = (PROJECTPATH + project + "/Assets/")

    for item in os.listdir(ASSETSPATH):
        if not item.startswith('_') and not item.startswith('.') \
                and os.path.isdir(os.path.join(ASSETSPATH, item)):
            cat.append(item)

    # Generate Tabs automagically
    create_tabs(self, cat, project)


# Retrieve directories in PROJECTPATH comboBox and update the categories tabs
# OLD LEGACY DO NOT USE WILL BE REMOVED
def project_list_OLD(self):
    project = self.comboBox.currentText()
    prefsConfig.update_setting(INI_PATH, 'Settings', 'CurrentProject', project)

    def update_tabs(columnview, category):
        newpath = (PROJECTPATH + project + "/Assets/" + category)

        if os.path.isdir(newpath):
            print(newpath)
            columnview.setEnabled(True)

            tab = columnview

            tab.fsm = QtWidgets.QFileSystemModel()
            tab.fsm.setReadOnly(False)

            tab.rootindex = tab.fsm.setRootPath(newpath)

            tab.setModel(tab.fsm)
            tab.setRootIndex(tab.rootindex)

            tab.setColumnWidths(colwidth)

        else:
            print(newpath + " doesn't exists!")
            columnview.setDisabled(True)

    cats = self.category
    views = sorted(self.assets.values())

    # Using Python zip lists to pair values at the same list index
    # This allows for dynamic instead of hard coded lists
    for view, cat in zip(views, cats):
        update_tabs(view, cat)


# Check if PROJECTPATH is valid and reset to home directory if error
def projectpath_valid(INI_PATH, PROJECTPATH):
    exists = os.path.exists(PROJECTPATH)
    if exists:
        print('Project Path is valid')
        return True
    else:
        home = os.path.expanduser('~')
        system = platform.system()

        if system == 'Darwin':
            home = (home + '/')

        prefsConfig.update_setting(INI_PATH, 'Settings', 'ProjectPath', home.replace('\\', '/'))

        a = QtWidgets.QApplication(sys.argv)
        a.setWindowIcon(QtGui.QIcon('icons/logo.ico'))

        w = QtWidgets.QWidget()
        m = QtWidgets.QMessageBox

        # Move PyQt Window position to center of the screen
        qtRectangle = w.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        w.move(qtRectangle.topLeft())

        warning_text = ("Project Path doesn't exists!"
                        + "\n\nProject Path has been set to " + home + " temporarily."
                        + "\n\nPlease restart Assets Browser.")

        m.warning(w, 'Warning', warning_text, m.Ok)

        w.show()


# Clear Layout?
def clear_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


# Toggle Debug Display
def show_debug(self):
    t = self.textEdit

    if self.checkBoxDebug.isChecked():
        t.clear()
        t.setHidden(False)
        t.setEnabled(True)

    else:
        t.setHidden(True)
        t.setEnabled(False)


# Redirect stdout to QTextEdit widget. Example usage in main.py:
# sys.stdout = OutLog( edit, sys.stdout)
# sys.stderr = OutLog( edit, sys.stderr, QtGui.QColor(255,0,0) )
class OutLog:
    def __init__(self, edit, out=None, color=None):
        self.edit = edit
        self.out = None
        self.color = color

    def write(self, m):
        if self.color:
            tc = self.edit.textColor()
            self.edit.setTextColor(self.color)

        self.edit.moveCursor(QtGui.QTextCursor.End)
        self.edit.insertPlainText(m)

        if self.color:
            self.edit.setTextColor(tc)

        if self.out:
            self.out.write(m)


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


# Repurpose from https://stackoverflow.com/a/32009595/8337847
def get_filesize(size, precision=2):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    suffixIndex = 0

    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1  # Increment the index of the suffix
        size = size / 1024  # Apply the division

    # Return using String formatting. f for float and s for string.
    return "%.*f %s" % (precision, size, suffixes[suffixIndex])

    # Alternative solution to the above: hurry.filesize
    # https://pypi.python.org/pypi/hurry.filesize/


# Reveal in OS function (works across all major platform)
def reveal_os(path):
    system = platform.system()

    if system == 'Windows':
        winpath = path.replace("/", "\\")
        if os.path.isdir(path):
            cmd = str('explorer /e,' + winpath)
            subprocess.call(cmd)
        elif os.path.exists(path):
            cmd = str('explorer /select,' + winpath)
            subprocess.call(cmd)
        else:
            print('Is this a valid OS?')

    elif system == 'Darwin':  # OSX/macOS
        subprocess.call(['open', '-R', path])

        # Alternative method for older OSX?
        # subprocess.Popen(['open', '-R', '%s' % (path)])

    elif system == 'Linux':
        dirpath = '/'.join(path.split('/')[0:-1])  # Omit filename from path
        subprocess.Popen(['xdg-open', dirpath])

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
        subprocess.call(["xdg-open", target])
    else:
        os.startfile(target)


# Check High DPI Support
def highdpi_check():
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        print('High DPI Scaling Enabled')

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
        print('High DPI Pixmaps Enabled')


# Workaround to show setWindowIcon on Win7 taskbar instead of default Python icon
def setTaskbarIcon():
    if platform.system() == 'Windows':
        myappid = u'taukeke.python.assetsbrowser'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


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

# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import platform
from PyQt4 import QtGui
from PyQt4 import QtCore
from modules import prefsConfig


# Retrieve PROJECTPATH value from INI
PROJECTPATH = prefsConfig.PROJECTPATH
CURRENTPROJECT = prefsConfig.CURRENTPROJECT
INI_PATH = prefsConfig.INI_PATH


# Emit PyQt signal to debug's textEdit
class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


# File/Directory Path Dictionary for easy access for any methods
selected_path = {'Path': ''}
file_manager = {'Windows': 'Explorer', 'Darwin': 'Finder', 'Linux': 'File Manager'}


# Create new ColumnView tabs to reduce DRY for categories
def columnview_tabs(columnview, category):

    # Select top most project from Project comboBox as default project
    project = (os.listdir(PROJECTPATH))[0]
    defaultpath = (PROJECTPATH + project + "/Assets/" + category)

    if os.path.isdir(defaultpath):
        print defaultpath
        columnview.setEnabled(True)

        tab = columnview

        tab.fsm = QtGui.QFileSystemModel()
        tab.fsm.setReadOnly(False)

        tab.rootindex = tab.fsm.setRootPath(defaultpath)

        tab.setModel(tab.fsm)
        tab.setRootIndex(tab.rootindex)

        # ====================================================

        # List for Column Width for QColumnView
        colwidth = [150]
        tab.setColumnWidths(colwidth)

        # ====================================================

        # Return selected item attributes in Model View for Preview Pane
        @QtCore.pyqtSlot(QtCore.QModelIndex)
        def get_fileinfo(index):
            indexItem = tab.fsm.index(index.row(), 0, index.parent())

            # Retrieve File Attributes
            fileName = str(tab.fsm.fileName(indexItem))
            fileSize = tab.fsm.size(indexItem)
            fileType = str(tab.fsm.type(indexItem))
            fileDate = tab.fsm.lastModified(indexItem)

            # global filePath
            filePath = str(tab.fsm.filePath(indexItem))

            # Format the File Attributes into String
            fileNameLabel = fileName
            fileSizeLabel = get_filesize(fileSize)
            fileTypeLabel = fileType.upper()  # Convert fileType to UPPERCASE
            fileDateLabel = fileDate.toString('yyyy/MM/dd' + ' ' + 'h:m AP')

            # Assign the File Attributes' String into respective labels
            tab.filename.setText(fileNameLabel)
            tab.filesize.setText(fileSizeLabel)
            tab.filetype.setText(fileTypeLabel)
            tab.filedate.setText(fileDateLabel)

            # For Debug Panel (feel free to comment/remove it)
            print fileNameLabel
            print fileSizeLabel
            print fileTypeLabel
            print fileDateLabel

            selected_path['Path'] = filePath

            # Retrieve filePath for Thumbnail Preview in __init__
            picPath = tab.fsm.filePath(indexItem)
            picType = fileType[0:-5]

            picTypes = ['jpg', 'jpeg', 'bmp', 'png', 'gif', 'bmp', 'ico', 'tga', 'tif', 'tiff']

            # JPEG and GIF format are broken with PyQt4 for macOS/OSX so
            # a workaround by omitting the format from thumbnail preview
            system = platform.system()
            if system == 'Darwin':
                picTypes.remove('jpg')
                picTypes.remove('jpeg')
                picTypes.remove('gif')

            # Generate thumbnails for Preview Pane
            for each in picTypes:
                if each.lower() == picType.lower():
                    max_size = 250  # Thumbnails max size in pixels

                    tb = QtGui.QPixmap(picPath)
                    tb_scaled = tb.scaled(max_size, max_size,
                                          QtCore.Qt.KeepAspectRatio,
                                          QtCore.Qt.SmoothTransformation)

                    tab.pvThumbs.setPixmap(tb_scaled)
                    break
                else:
                    fileInfo = QtCore.QFileInfo(picPath)  # Retrieve info like icons, path, etc
                    fileIcon = QtGui.QFileIconProvider().icon(fileInfo)
                    icon = fileIcon.pixmap(128, 128, QtGui.QIcon.Normal, QtGui.QIcon.On)

                    tab.pvThumbs.setPixmap(icon)

            return filePath

        # ====================================================

        # When an item clicked in the columnView tab, execute get_fileinfo method
        tab.clicked.connect(get_fileinfo)

        # ====================================================

        # ContextMenu (Right Click Menu) Test
        tab.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        quitAction = QtGui.QAction('Quit', tab)
        quitAction.triggered.connect(QtGui.QApplication.quit)
        tab.addAction(quitAction)

        # spamAction = QtGui.QAction('SPAM', tab)
        # spamAction.triggered.connect(spam)
        # tab.addAction(spamAction)
        #
        # hamAction = QtGui.QAction('HAM', tab)
        # hamAction.triggered.connect(ham)
        # tab.addAction(hamAction)

        revealAction = QtGui.QAction(('Reveal in ' + file_manager[platform.system()]), tab)
        revealAction.triggered.connect(lambda: reveal_os(selected_path['Path']))
        tab.addAction(revealAction)

        # ====================================================

        # Preview widget layout and features goes here as a function
        def preview(previewWidget, tab):

            # -------------------- TEXT LABELS STARTS HERE -------------------- #

            # File Category Labels
            catName = QtGui.QLabel('Name: ')
            catSize = QtGui.QLabel('Size: ')
            catType = QtGui.QLabel('Type: ')
            catDate = QtGui.QLabel('Modified: ')

            # File Attributes Labels
            tab.filename = QtGui.QLabel()
            tab.filesize = QtGui.QLabel()
            tab.filetype = QtGui.QLabel()
            tab.filedate = QtGui.QLabel()

            # Align Right for Prefix Labels
            align_right = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter

            catName.setAlignment(align_right)
            catSize.setAlignment(align_right)
            catType.setAlignment(align_right)
            catDate.setAlignment(align_right)

            # File Attributes Layout
            sublayout_text = QtGui.QGridLayout()

            sublayout_text.addWidget(catName, 0, 0)
            sublayout_text.addWidget(catSize, 1, 0)
            sublayout_text.addWidget(catType, 2, 0)
            sublayout_text.addWidget(catDate, 3, 0)

            # File Attributes Value for Preview Pane
            sublayout_text.addWidget(tab.filename, 0, 1)
            sublayout_text.addWidget(tab.filesize, 1, 1)
            sublayout_text.addWidget(tab.filetype, 2, 1)
            sublayout_text.addWidget(tab.filedate, 3, 1)

            # Arrange layout to upper part of widget
            sublayout_text.setRowStretch(4, 1)

            # -------------------- THUMBNAILS STARTS HERE -------------------- #

            # Preview Thumbnails (pvThumbs)
            tab.pvThumbs = QtGui.QLabel()
            tab.pvThumbs.setPixmap(QtGui.QPixmap())

            sublayout_pic = QtGui.QVBoxLayout()
            sublayout_pic.addWidget(tab.pvThumbs)
            sublayout_pic.setAlignment(QtCore.Qt.AlignCenter)

            # -------------------- PREVIEW PANE STARTS HERE -------------------- #

            # Set Preview Pane to QColumnView setPreviewWidget
            preview_pane = QtGui.QVBoxLayout(previewWidget)
            preview_pane.addLayout(sublayout_pic)
            preview_pane.addLayout(sublayout_text)

            tab.setPreviewWidget(previewWidget)

        # ====================================================

        previewWidget = QtGui.QWidget()
        preview(previewWidget, tab)

    else:
        print (defaultpath + " doesn't exists!")
        columnview.setDisabled(True)


# Retrieve directories in PROJECTPATH comboBox and update the categories tabs
def project_list(self):
    project = self.comboBox.currentText()
    prefsConfig.update_setting(INI_PATH, 'Settings', 'CurrentProject', project)

    def update_tabs(columnview, category):
        newpath = (PROJECTPATH + project + "/Assets/" + category)

        if os.path.isdir(newpath):
            print newpath
            columnview.setEnabled(True)

            tab = columnview

            tab.fsm = QtGui.QFileSystemModel()
            tab.fsm.setReadOnly(False)

            tab.rootindex = tab.fsm.setRootPath(newpath)

            tab.setModel(tab.fsm)
            tab.setRootIndex(tab.rootindex)

            # List for Column Width for QColumnView
            colwidth = [150]
            tab.setColumnWidths(colwidth)

        else:
            print (newpath + " doesn't exists!")
            columnview.setDisabled(True)

    update_tabs(self.columnViewBG, 'BG')
    update_tabs(self.columnViewCH, 'CH')
    update_tabs(self.columnViewFX, 'FX')
    update_tabs(self.columnViewProps, 'Props')
    update_tabs(self.columnViewVehicles, 'Vehicles')

    # Return project for use in assetDialog.py
    return project


def show_debug(self):
    if self.checkBoxDebug.isChecked():
        self.textEdit.clear()
        self.textEdit.setHidden(False)
        self.textEdit.setEnabled(True)
    else:
        self.textEdit.setHidden(True)
        self.textEdit.setEnabled(False)


def always_on_top(self):
    if self.actionAlwaysOnTop.isChecked():
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        print "Always on Top Enabled"
    else:
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
        print "Always on Top Disabled"
    self.show()


# Repurpose from https://stackoverflow.com/a/32009595/8337847
def get_filesize(size, precision=2):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    suffixIndex = 0

    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1    # Increment the index of the suffix
        size = size/1024    # Apply the division

    # Return using String formatting. f for float and s for string.
    return "%.*f %s" % (precision, size, suffixes[suffixIndex])

    # Alternative solution to the above: hurry.filesize
    # https://pypi.python.org/pypi/hurry.filesize/


def close_app():
    sys.exit()


def restart_app():
    os.execv(sys.executable, [sys.executable] + sys.argv)


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
            print 'YOLOOOOOOO'

    elif system == 'Darwin':  # OSX/macOS
        subprocess.call(['open', '-R', path])

        # Alternative method for older OSX?
        # subprocess.Popen(['open', '-R', '%s' % (path)])

    elif system == 'Linux':
        subprocess.Popen(['xdg-open', path])

    else:
        print 'FILE/DIRECTORY IS NOT VALID!'


# When testing or in doubt, it's HAM time!
def ham():
    print 'HAM! HAM! HAM!'


# Show CWD (Current Work Directory) as a QMessageBox
def show_cwd():
    widget = QtGui.QWidget()
    cwd = os.getcwd()
    QtGui.QMessageBox.information(widget, "Information", cwd)

# -*- coding: utf-8 -*-
import os
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from modules import prefsConfig


# Call prefsConfig.get_setting to retrieve projectPath value from INI
projectPath = prefsConfig.get_setting(prefsConfig.INI_PATH, 'Settings', 'ProjectPath')


# Emit PyQt signal to debug's textEdit
class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


# Create directories for new asset
def createdir_asset(path, asset):
    asset_name = asset                      # Declare name of Asset to work with
    asset_path = str(path)                  # Declare path where Asset directory is to be located
    full_path = (asset_path + asset_name)   # Concatenate Asset full path
    print ('Assets will be created at ' + full_path)

    # Check whether Asset directory already exist
    if os.path.exists(full_path):
        pass
    else:
        os.mkdir(full_path, 0755)

    # Declare names for child folders
    folder1 = "Scenes"
    folder2 = "Textures"
    folder3 = "References"
    folder4 = None
    folder5 = "WIP"
    folderList = [folder1, folder2, folder3, folder4, folder5]

    # Check if child folder exists & creates if None
    if os.path.exists(folder1):
        pass
    else:
        for folder in folderList:
            if folder is None:
                pass
            else:
                os.mkdir(os.path.join(full_path, folder))


# Retrieve directories in INI ProjectPath comboBox and update the categories tabs
def project_list(self):
    projectName = self.comboBox.currentText()
    path = (projectPath + projectName + "/Assets/")

    def update_tabs(columnview, category):
        path_list = (projectPath + projectName + "/Assets/" + category)
        print path_list

        self.fsm = QtGui.QFileSystemModel()
        self.fsm.setReadOnly(False)

        self.rootindex = self.fsm.setRootPath(path_list)

        tab = columnview

        tab.setModel(self.fsm)
        tab.setRootIndex(self.rootindex)

        # List for Column Width for QColumnView
        colwidth = [150, 150, 150]
        tab.setColumnWidths(colwidth)

    update_tabs(self.columnViewBG, 'BG')
    update_tabs(self.columnViewCH, 'CH')
    update_tabs(self.columnViewFX, 'FX')

    # Return path for use in assetDialog.py
    return path


def show_debug(self):
    if self.checkBoxDebug.isChecked():
        self.textEdit.clear()
        self.textEdit.setVisible(True)
    else:
        self.textEdit.setVisible(False)


def always_on_top(self):
    if self.actionAlwaysOnTop.isChecked():
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        print "Always on Top Enabled"
    else:
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
        print "Always on Top Disabled"
    self.show()


# Repurpose from https://stackoverflow.com/a/32009595/8337847
# Alternative way - hurry.filesize https://pypi.python.org/pypi/hurry.filesize/
def get_filesize(size, precision=2):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    suffixIndex = 0

    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1    # Increment the index of the suffix
        size = size/1024    # Apply the division

    # Return using String formatting. f for float and s for string.
    return "%.*f %s" % (precision, size, suffixes[suffixIndex])


def close_app():
    sys.exit()


def restart_app():
    os.execv(sys.executable, [sys.executable] + sys.argv)


# When testing or in doubt, it's HAM time!
def ham():
    print 'HAM! HAM! HAM!'


# Show CWD (Current Work Directory) as a QMessageBox
def spam():
    widget = QtGui.QWidget()
    spam = os.getcwd()
    QtGui.QMessageBox.information(widget, "Information", spam)

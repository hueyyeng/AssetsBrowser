# -*- coding: utf-8 -*-
import os
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from modules import prefsConfig


# Call prefsConfig.get_setting to retrieve projectPath value from INI
projectPath = prefsConfig.get_setting(prefsConfig.INI_PATH, 'Settings', 'ProjectPath')


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

    # Check whether child folder exists & creates if not
    if os.path.exists(folder1):
        pass
    else:
        for folder in folderList:
            if folder is None:
                pass
            else:
                os.mkdir(os.path.join(full_path, folder))


def project_list(self):
    projectName = self.comboBox.currentText()
    path = (projectPath + projectName + "/Assets/")

    def spam(column, category):
        path_list = (projectPath + projectName + "/Assets/" + category)
        print path_list

        self.fsm = QtGui.QFileSystemModel()
        self.fsm.setReadOnly(False)

        rootindex = self.fsm.setRootPath(path_list)

        column.setModel(self.fsm)
        column.setRootIndex(rootindex)

    spam(self.columnViewBG, 'BG')
    spam(self.columnViewCH, 'CH')
    spam(self.columnViewFX, 'FX')

    # Return path for use in assetDialog.py
    return path


def show_debug():
    widget = QtGui.QWidget()
    spam = os.getcwd()
    QtGui.QMessageBox.information(widget, "Information", spam)


def always_on_top(self):
    if self.actionAlwaysOnTop.isChecked():
        self.setWindowFlags(
            self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        print "Always on Top Enabled"
    else:
        self.setWindowFlags(
            self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
        print "Always on Top Disabled"
    self.show()


def close_app():
    sys.exit()


def restart_app():
    os.execv(sys.executable, [sys.executable] + sys.argv)


# When testing or in doubt, it's HAM time!
def ham():
    print 'HAM! HAM! HAM!'

# -*- coding: utf-8 -*-
import sys
from modules import functions
from ui import ui_about
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class About(QtWidgets.QDialog, ui_about.Ui_AboutDialog):

    def __init__(self, parent=None):
        super(About, self).__init__(parent)
        self.setupUi(self)
        self.buttonBox.clicked.connect(self.close)
        functions.window_icon(self)

        # Redefine path for graphics/icons when executed from main.py
        self.labelGraphic.setPixmap(QtGui.QPixmap('icons/about.png'))


def showAboutDialog():
    window = About()
    window.exec_()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = About()
    window.show()
    sys.exit(app.exec_())
"""About Dialog"""
import sys
from pathlib import Path

from PyQt5 import QtGui, QtWidgets

import ui.functions
from ui.window.ui_about import Ui_AboutDialog


class About(QtWidgets.QDialog, Ui_AboutDialog):
    def __init__(self, parent=None):
        super(About, self).__init__(parent)
        self.setupUi(self)
        self.buttonBox.clicked.connect(self.close)
        logo = Path.cwd() / 'icons' / 'about.png'
        self.labelGraphic.setPixmap(QtGui.QPixmap(str(logo)))
        ui.functions.set_window_icon(self)


def show_dialog():
    dialog = About()
    dialog.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = About()
    window.show()
    sys.exit(app.exec_())

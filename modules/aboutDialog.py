# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from ui import ui_about


class About(QtGui.QDialog, ui_about.Ui_AboutDialog):

    def __init__(self, parent=None):
        super(About, self).__init__(parent)
        self.setupUi(self)
        self.buttonBox.clicked.connect(self.close)

        # Redefine path for graphics/icons when executed from main.py
        self.setWindowIcon(QtGui.QIcon('icons/logo.ico'))
        self.labelGraphic.setPixmap(QtGui.QPixmap('icons/about.png'))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = About()
    window.show()
    sys.exit(app.exec_())
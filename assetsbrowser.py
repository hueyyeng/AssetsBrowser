"""Assets Browser Mainwindow"""
import os
import sys
import logging
from PyQt5 import QtGui, QtCore, QtWidgets

from config import configurations, constants
from helpers.exceptions import ApplicationAlreadyExists
import helpers.functions
import helpers.utils
import ui.functions
from ui.dialog import about, asset, preferences
from ui.help import repath
from ui.window import ui_main

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PROJECT_PATH = constants.PROJECT_PATH
INI_PATH = constants.INI_PATH
THEME = constants.THEME


class AssetsBrowser(QtWidgets.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, parent=None):
        super(AssetsBrowser, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Assets Browser [PID: %d]' % QtWidgets.QApplication.applicationPid())
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint)

        # 1.1 Initialize main window
        ui.functions.center_screen(self)
        ui.functions.font_size_overrides(self)
        ui.functions.set_window_icon(self)
        QtWidgets.QApplication.setStyle(THEME)

        # 1.2 Menu action goes here
        self.actionAbout.triggered.connect(about.show_dialog)
        self.actionAlwaysOnTop.triggered.connect(lambda: ui.functions.always_on_top(self))
        self.actionPreferences.triggered.connect(preferences.show_dialog)
        self.actionQuit.triggered.connect(helpers.functions.close_app)

        # 1.3 Setup input/button here
        self.pushBtnNew.clicked.connect(asset.show_dialog)
        self.checkBoxDebug.clicked.connect(lambda: helpers.functions.show_debug(self))

        # 1.3.1 Debug textbox
        self.textEdit.clear()
        self.textEdit.setHidden(True)
        self.textEdit.setEnabled(False)

        # 2. Redirect stdout/stderr to QTextEdit widget for debug log
        sys.stdout = OutLog(self.textEdit, sys.stdout)
        sys.stderr = OutLog(self.textEdit, sys.stderr, QtGui.QColor(255, 0, 0))
        formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=formatter)

        # 3. Project List Dropdown ComboBox
        self.comboBox.fsm = QtWidgets.QFileSystemModel()
        self.comboBox.rootindex = self.comboBox.fsm.setRootPath(PROJECT_PATH)
        self.comboBox.setModel(self.comboBox.fsm)
        self.comboBox.setRootModelIndex(self.comboBox.rootindex)
        self.comboBox.setCurrentIndex(1)
        self.comboBox.activated[str].connect(lambda: helpers.functions.project_list(self))

        current_project = self._current_project()

        # 4.1 Create empty list and dictionary for ColumnView tabs
        self.category = []
        self.assets = {}
        assets_path = (PROJECT_PATH + current_project + "/Assets/")

        # 4.2 Warn user if Assets directory doesn't exists
        if not os.path.isdir(assets_path):
            warning_text = (
                    "Assets directory is unavailable.\n"
                    + "\n"
                    + "Please ensure you have access to it."
            )
            helpers.utils.alert_window("Warning", warning_text)
            helpers.functions.close_app()

        # 4.3 Populate categories list of Assets folder
        for category in os.listdir(assets_path):
            name_prefix = category.startswith(('_', '.'))
            assets_directory = os.path.join(assets_path, category)
            if not name_prefix and os.path.isdir(assets_directory):
                self.category.append(category)

        # 4.4.1 Generate Tabs using create_tabs
        helpers.functions.create_tabs(self, self.category, current_project)
        self.splitter.setSizes([150, 500])

        # 4.4.2 Help Tab
        html_file = 'ui/help/help.html'
        temp_html_path = ('file:///' + str(repath(html_file)))
        self.textBrowserHelp.setSource(QtCore.QUrl(temp_html_path))

    def _current_project(self):
        """Set current project from Project list dropdown."""
        projects = []
        for project in os.listdir(PROJECT_PATH):
            if not project.startswith(('_', '.')) and os.path.isdir(os.path.join(PROJECT_PATH, project)):
                projects.append(project)
        configurations.update_setting(INI_PATH, 'Settings', 'CurrentProject', projects[0])
        current_project = configurations.current_project()
        return current_project

    def __del__(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


class OutLog():
    def __init__(self, edit, out=None, color=None):
        """Redirect stdout to QTextEdit widget.

        Parameters
        ----------
        edit : QtWidgets.QTextEdit
            QTextEdit object.
        out : object
            Alternate stream (can be the original sys.stdout).
        color : QtGui.QColor
            QColor object (i.e. color stderr a different color).

        Returns
        -------
        None

        """
        self.edit = edit
        self.out = out
        self.color = color

    def write(self, text):
        """Write stdout print values to QTextEdit widget.

        Parameters
        ----------
        text : str
            Print values from stdout.

        Returns
        -------
        None

        """
        if self.color:
            text_color = self.edit.textColor()
            self.edit.setTextColor(text_color)
        if self.out:
            self.out.write(text)
        self.edit.moveCursor(QtGui.QTextCursor.End)
        self.edit.insertPlainText(text)

    def flush(self):
        """Flush Outlog when process terminates.

        This prevent Exit Code 120 from happening so the process
        can finished with Exit Code 0.

        Returns
        -------
        None

        """
        self.out.flush()


if __name__ == "__main__":
    # 1. Raise error if invalid path
    helpers.functions.valid_path(INI_PATH, PROJECT_PATH)

    # 2. Setup OS related settings
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    ui.functions.taskbar_icon()

    # 3. Initialize QApplication instance
    app = QtWidgets.QApplication.instance()
    if app is not None:
        raise ApplicationAlreadyExists(app)

    app = QtWidgets.QApplication(sys.argv)
    ui.functions.hidpi_check(app)
    ui.functions.theme_loader(app)

    # 4. Launch main window
    window = AssetsBrowser()
    window.show()
    sys.exit(app.exec_())

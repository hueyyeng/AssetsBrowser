"""Assets Browser Mainwindow"""
import logging
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

import helpers.functions
import helpers.utils
import ui.functions
from config import configurations
from config.constants import TOML_PATH
from config.utils import check_config_file
from helpers.exceptions import ApplicationAlreadyExists
from helpers.widgets import ColumnViewWidget
from ui.dialog import about, asset, preferences
from ui.window import ui_main

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

EXIT_CODE_REBOOT = -123


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
        QtWidgets.QApplication.setStyle(configurations.get_setting('UI', 'Theme'))

        # 1.2 Menu action goes here
        self.actionAbout.triggered.connect(about.show_dialog)
        self.actionAlwaysOnTop.triggered.connect(lambda: ui.functions.always_on_top(self))
        self.actionPreferences.triggered.connect(preferences.show_dialog)
        self.actionQuit.triggered.connect(helpers.functions.close_app)

        # 1.3 Setup input/button here
        self.pushBtnNew.clicked.connect(asset.show_dialog)
        self.checkBoxDebug.clicked.connect(self._show_debug)

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
        self.project_path = configurations.get_setting('Settings', 'ProjectPath')
        self.comboBox.fsm = QtWidgets.QFileSystemModel()
        self.comboBox.rootindex = self.comboBox.fsm.setRootPath(self.project_path)
        self.comboBox.setModel(self.comboBox.fsm)
        self.comboBox.setRootModelIndex(self.comboBox.rootindex)
        self.comboBox.setCurrentIndex(1)
        self.comboBox.activated[str].connect(self.project_list)

        # 4.1 Create empty list and dictionary for ColumnView tabs
        self.category = []
        self.assets = {}
        self.current_project = self._current_project()
        assets_path = os.path.join(self.project_path, self.current_project, "Assets")

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
        self.create_tabs(self.category, self.current_project)
        self.splitter.setSizes([150, 500])

        # 4.4.2 Help Tab
        absolute_path = os.path.abspath(os.path.dirname(__file__))
        help_file = os.path.join(absolute_path, 'ui', 'help', 'help.html')
        self.textBrowserHelp.setSource(QtCore.QUrl.fromLocalFile(help_file))

    def create_tabs(self, categories: list, project: str):
        """Create QColumnView tabs.

        Create QColumnView tabs dynamically from Assets' List.

        Parameters
        ----------
        categories : :obj:`list` of :obj:`str`
            Array of categories in str format.
        project : str
            The project name.

        Notes
        -----
        Uses ColumnViewWidget that inherit QColumnView with custom properties

        """
        for category in categories:
            self.column_view = ColumnViewWidget()
            self.column_view.setAlternatingRowColors(False)
            self.column_view.setResizeGripsVisible(True)

            self.assets[f"column_view{category}"] = self.column_view

            self.tab = QtWidgets.QWidget()
            self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab)
            self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.horizontalLayout.addWidget(self.column_view)

            self.tabWidget.addTab(self.tab, category)
            helpers.functions.create_column_view(self.column_view, category, project)

    def project_list(self):
        """List Project directories in PROJECT_PATH comboBox.

        Retrieve directories in PROJECT_PATH comboBox, clear existing tabs and create new tabs.

        """
        # 1. Update TOML CurrentProject with chosen project from comboBox
        project = self.comboBox.currentText()
        configurations.update_setting('Settings', 'CurrentProject', project)

        # 2. Clear all tabs except Help
        count = 0
        while count < 10:
            count = count + 1
            self.tabWidget.removeTab(1)

        # 3. Force clear existing self.category and self.assets value
        self.category = []
        self.assets = {}

        # 4. Populate self.category list with valid Assets directory name
        assets_path = (self.project_path + project + "/Assets/")
        for item in os.listdir(assets_path):
            prefix = item.startswith(('_', '.'))
            is_directory = os.path.isdir(os.path.join(assets_path, item))
            if not prefix and is_directory:
                self.category.append(item)

        # 5. Create tabs using self.category list and selected project
        self.create_tabs(self.category, project)

    def _current_project(self):
        """Set current project from Project list dropdown."""
        projects = []
        for project in os.listdir(self.project_path):
            if not project.startswith(('_', '.')) and os.path.isdir(os.path.join(self.project_path, project)):
                projects.append(project)
        configurations.update_setting('Settings', 'CurrentProject', projects[0])
        current_project = configurations.get_setting('Settings', 'CurrentProject')
        return current_project

    def _show_debug(self):
        """Toggle Debug Display."""
        text = self.textEdit
        if self.checkBoxDebug.isChecked():
            text.clear()
            text.setHidden(False)
            text.setEnabled(True)
        else:
            text.setHidden(True)
            text.setEnabled(False)

    def __del__(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


class OutLog():
    def __init__(self, edit: QtWidgets.QTextEdit, out=None, color=None):
        """Redirect stdout to QTextEdit widget.

        Parameters
        ----------
        edit : QtWidgets.QTextEdit
            QTextEdit object.
        out : object or None
            Alternate stream (can be the original sys.stdout).
        color : QtGui.QColor or None
            QColor object (i.e. color stderr a different color).

        """
        self.edit = edit
        self.out = out
        self.color = color

    def write(self, text: str):
        """Write stdout print values to QTextEdit widget.

        Parameters
        ----------
        text : str
            Print values from stdout.

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

        """
        self.out.flush()


if __name__ == "__main__":
    # 1.1 Check for config file and create one if doesn't exists
    check_config_file(TOML_PATH)

    # 1.2 Raise error if invalid project path
    helpers.utils.valid_project_path(configurations.get_setting('Settings', 'ProjectPath'))

    # 2. Setup OS related settings
    ui.functions.taskbar_icon()
    # os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"  # Temporary disable as scaling is wrong on Ubuntu 16.04 LTS

    # 3.1 Launch main window
    current_exit_code = EXIT_CODE_REBOOT
    while current_exit_code == EXIT_CODE_REBOOT:
        # 3.2 Initialize QApplication instance
        app = QtWidgets.QApplication.instance()
        if app is not None:
            raise ApplicationAlreadyExists(app)
        app = QtWidgets.QApplication(sys.argv)
        ui.functions.theme_loader(app)
        window = AssetsBrowser()
        window.show()
        exit_code = app.exec_()
        app = None

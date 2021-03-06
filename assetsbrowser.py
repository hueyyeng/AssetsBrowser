"""Assets Browser MainWindow"""
import logging
import os
import sys
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets

import helpers.functions
import helpers.utils
import ui.functions
from config import configurations
from config.constants import TOML_PATH
from config.utils import check_config_file
from helpers.exceptions import (
    ApplicationAlreadyExists,
)
from helpers.widgets import ColumnViewWidget
from ui.dialog import (
    about,
    applications_list,
    asset,
    asset_item,
    asset_item_format,
    preferences,
)
from ui.window import ui_main

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

EXIT_CODE_REBOOT = -123


class AssetsBrowser(QtWidgets.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, parent=None):
        super(AssetsBrowser, self).__init__(parent)
        self.setupUi(self)
        ui.functions.set_window_icon(self)
        self._setup_window_properties()
        self._setup_menu_actions()
        self._setup_ui_buttons()
        self._setup_debug_log()
        self._setup_project_list_dropdown()
        self._setup_initial_tabs()
        self._setup_help_tab()

    def _setup_window_properties(self):
        """Setup Window Properties"""
        self.setWindowTitle('Assets Browser [PID: %d]' % QtWidgets.QApplication.applicationPid())
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint)
        self.splitter.setSizes([150, 500])
        ui.functions.center_screen(self)

    def _setup_menu_actions(self):
        # 1.2 Menu action goes here
        self.actionNewAsset.triggered.connect(asset.show_dialog)
        self.actionNewAssetItem.triggered.connect(asset_item.show_dialog)
        self.actionManageFormat.triggered.connect(asset_item_format.show_dialog)
        self.actionApplicationsList.triggered.connect(applications_list.show_dialog)
        self.actionAbout.triggered.connect(about.show_dialog)
        self.actionAlwaysOnTop.triggered.connect(lambda: ui.functions.always_on_top(self))
        self.actionPreferences.triggered.connect(preferences.show_dialog)
        self.actionQuit.triggered.connect(helpers.functions.close_app)

    def _setup_ui_buttons(self):
        # 1.3 Setup input/button here
        self.pushBtnNewAsset.clicked.connect(asset.show_dialog)
        self.pushBtnNewAssetItem.clicked.connect(asset_item.show_dialog)
        self.pushBtnManageFormat.clicked.connect(asset_item_format.show_dialog)
        self.debugCheckBox.clicked.connect(self.show_debug)

    def _setup_debug_log(self):
        """Setup Debug Log"""
        # 1. Debug textbox
        self.textEdit.clear()
        self.textEdit.setHidden(True)
        self.textEdit.setEnabled(False)

        # 2. Redirect stdout/stderr to QTextEdit widget for debug log
        sys.stdout = OutLog(self.textEdit, sys.stdout)
        sys.stderr = OutLog(self.textEdit, sys.stderr, QtGui.QColor(255, 0, 0))
        formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=formatter)

    def _setup_project_list_dropdown(self):
        """Setup Project List Dropdown"""
        self.project_path = configurations.get_setting('Settings', 'ProjectPath')
        self.combobox_fsm = QtWidgets.QFileSystemModel()
        self.projectComboBox.setModel(self.combobox_fsm)
        root_idx = self.combobox_fsm.setRootPath(self.project_path)
        self.projectComboBox.setRootModelIndex(root_idx)
        self.combobox_fsm.directoryLoaded.connect(self.populate_project_list)
        self.projectComboBox.activated[str].connect(self.select_project)

    def _setup_initial_tabs(self):
        """Setup initial tabs

        Create ColumnView tabs using TOML CurrentProject value

        """
        self.select_project()

    def _setup_help_tab(self):
        """Setup Help tab"""
        help_file = Path(__file__).parent / 'ui' / 'help' / 'help.html'
        self.textBrowserHelp.setSource(QtCore.QUrl.fromLocalFile(str(help_file)))

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
            tab = QtWidgets.QWidget()
            self.tabWidget.addTab(tab, category)
            self.horizontalLayout = QtWidgets.QHBoxLayout(tab)
            self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.horizontalLayout.addWidget(ColumnViewWidget(category, project))

    def populate_project_list(self, path):
        """Populate Project directories name in Project List comboBox.

        This is a workaround to set the current project on startup as Qt will only
        populate the combobox after initializing QApplication instance due to the
        way FileSystemModel works.

        By using directoryLoaded signal, this function will be called and populate the
        combobox using setCurrentIndex and findText to retrieve the current project index.

        Parameters
        ----------
        path : str
            Project directory path

        """
        # 1. Loop and add the project directories name
        fsm_index = self.combobox_fsm.index(path)
        for i in range(self.combobox_fsm.rowCount(fsm_index)):
            project_idx = self.combobox_fsm.index(i, 0, fsm_index)
            self.projectComboBox.addItem(project_idx.data(), self.combobox_fsm.filePath(project_idx))

        # 2. Set the current project based on TOML settings
        self.projectComboBox.setCurrentIndex(
            self.projectComboBox.findText(
                configurations.get_setting('Settings', 'CurrentProject'),
                QtCore.Qt.MatchContains,
            )
        )

    def select_project(self, project=None):
        """Select Project from Project List comboBox.

        Select project, clear existing tabs and create new tabs using the subdirectories
        in the project's Assets directory.

        Parameters
        ----------
        project : str or None
            Project name. By default, None

        """
        # 1. Use CurrentProject value from TOML on startup
        if not project:
            project = configurations.get_setting('Settings', 'CurrentProject')
        else:
            project = self.projectComboBox.currentText()
            configurations.update_setting('Settings', 'CurrentProject', project)

        # 2. Raised warning if Assets directory not found in project path
        assets_path = Path(self.project_path) / project / 'Assets'
        if not assets_path.is_dir():
            warning_text = (
                    "Assets directory is unavailable.\n\n"
                    "The Assets directory is either missing in the selected project\n"
                    "directory or you do not have permission to access it.\n\n"
            )
            helpers.utils.alert_window("Warning", warning_text)
            helpers.functions.close_app()

        # 3. Clear all tabs except Help
        count = 0
        total_tabs = self.tabWidget.count()
        while count < total_tabs:
            count += 1
            self.tabWidget.removeTab(1)

        # 4. Create tabs from Assets' subfolders
        self.categories = []
        asset_categories = [a for a in os.listdir(str(assets_path)) if not a.startswith(('_', '.'))]
        for category in asset_categories:
            category_subfolder = assets_path / category
            if category_subfolder.is_dir():
                self.categories.append(str(category))
        self.create_tabs(self.categories, project)

    def show_debug(self):
        """Toggle Debug Display."""
        text = self.textEdit
        if self.debugCheckBox.isChecked():
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
        app.setStyleSheet(open('ui/stylesheet.css').read())
        ui.functions.theme_loader(app)
        window = AssetsBrowser()
        window.show()
        exit_code = app.exec_()
        app = None

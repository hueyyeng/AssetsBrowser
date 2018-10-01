import os
import sys
import logging
from PyQt5 import QtGui, QtCore, QtWidgets
from config import configurations, constants
from modules import functions, utils
from ui.dialog import about, asset, preferences
from ui.help import repath
from ui.window import main

logger = logging.getLogger(__name__)

# Set Path from INI file
PROJECT_PATH = constants.PROJECT_PATH
INI_PATH = constants.INI_PATH
THEME = constants.THEME


class AssetsBrowser(QtWidgets.QMainWindow, main.Ui_MainWindow):
    def __init__(self, parent=None):
        super(AssetsBrowser, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Assets Browser [PID: %d]' % QtWidgets.QApplication.applicationPid())
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint)
        functions.center_screen(self)
        functions.font_size_overrides(self)
        functions.set_window_icon(self)
        QtWidgets.QApplication.setStyle(THEME)

        # Redirect stdout/stderr to QTextEdit widget for debug log
        sys.stdout = OutLog(self.textEdit, sys.stdout)
        sys.stderr = OutLog(self.textEdit, sys.stderr, QtGui.QColor(255, 0, 0))

        # Project List Dropdown ComboBox
        self.comboBox.fsm = QtWidgets.QFileSystemModel()
        self.comboBox.rootindex = self.comboBox.fsm.setRootPath(PROJECT_PATH)
        self.comboBox.setModel(self.comboBox.fsm)
        self.comboBox.setRootModelIndex(self.comboBox.rootindex)
        self.comboBox.setCurrentIndex(1)
        self.comboBox.activated[str].connect(lambda: functions.project_list(self))

        current_project = self.current_project()

        # Create empty list and dictionary for ColumnView tabs
        self.category = []
        self.assets = {}

        assets_path = (PROJECT_PATH + current_project + "/Assets/")

        # Warn user if Assets directory doesn't exists
        try:
            os.path.isdir(assets_path)
        except OSError:
            warning_text = (
                    "Assets directory is unavailable."
                    + "\n"
                    + "\n"
                    + "Please ensure you have access to it."
            )
            utils.alert_window(text=warning_text, title="Warning")
            functions.close_app()

        # Populate categories list of Assets folder
        for category in os.listdir(assets_path):
            name_prefix = category.startswith(('_', '.'))
            assets_directory = os.path.join(assets_path, category)
            if not name_prefix and os.path.isdir(assets_directory):
                self.category.append(category)

        # Generate Tabs using create_tabs
        functions.create_tabs(self, self.category, current_project)

        # Splitter Size Config
        self.splitter.setSizes([150, 500])

        # Help Tab
        html_file = 'ui/help/help.html'
        temp_html_path = ('file:///' + str(repath(html_file)))
        self.textBrowserHelp.setSource(QtCore.QUrl(temp_html_path))

        # Menu Action
        self.actionAbout.triggered.connect(about.show_dialog)
        self.actionPreferences.triggered.connect(preferences.show_dialog)
        self.actionQuit.triggered.connect(functions.close_app)

        # Create New Asset Button
        self.pushBtnNew.clicked.connect(asset.show_dialog)

        # When calling functions from imported modules that inherit the QMainWindow
        # but located outside its scope, use 'lambda:' followed by the method as
        # though it was defined within the same class for easier code maintenance
        self.actionAlwaysOnTop.triggered.connect(lambda: functions.always_on_top(self))

        # Show Debug CheckBox and Disabled the Debug textEdit
        self.checkBoxDebug.clicked.connect(lambda: functions.show_debug(self))
        self.textEdit.clear()
        self.textEdit.setHidden(True)
        self.textEdit.setEnabled(False)

    @staticmethod
    def current_project():
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
        edit : PyQt5.QtWidgets.QTextEdit
            QTextEdit object.
        out : object
            Alternate stream (can be the original sys.stdout).
        color : PyQt5.QtGui.QColor
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
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    functions.taskbar_icon()

    valid_path = functions.valid_path(INI_PATH, PROJECT_PATH)
    if valid_path:
        app = QtWidgets.QApplication.instance()
        if app is None:
            app = QtWidgets.QApplication(sys.argv)
            functions.hidpi_check(app)
        else:
            logger.info('QApplication instance already exists: %s' % str(app))

        window = AssetsBrowser()
        window.show()
        sys.exit(app.exec_())

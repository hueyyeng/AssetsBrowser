"""Assets Browser Custom Widgets"""
import logging
import platform
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets

from config.configurations import get_setting
from config.constants import IMAGE_FORMAT
from helpers.enums import FileManager
from helpers.utils import get_file_size, open_file, reveal_in_os
from ui.enums import IconRadio, PreviewRadio

logger = logging.getLogger(__name__)

ICON_THUMBNAILS_MODE = IconRadio(get_setting('Advanced', 'IconThumbnails'))
ICON_THUMBNAILS_SIZE = QtCore.QSize(32, 32)
MAX_SIZE = PreviewRadio(get_setting('Advanced', 'Preview')).size()


class ColumnViewFileIcon(QtWidgets.QFileIconProvider):
    def icon(self, file_info: QtCore.QFileInfo):
        if ICON_THUMBNAILS_MODE.value == -3:
            return QtGui.QIcon()

        path = file_info.filePath()
        icon = super().icon(file_info)
        if path.lower().endswith(IMAGE_FORMAT):
            file_icon = QtGui.QPixmap(ICON_THUMBNAILS_SIZE)
            file_icon.load(path)
            icon = QtGui.QIcon(file_icon)
        return icon


class ColumnViewWidget(QtWidgets.QColumnView):
    def __init__(self, category, project):
        super().__init__()
        default_path = Path(get_setting('Settings', 'ProjectPath')) / project / "Assets" / category
        logger.debug("Load... %s", default_path)

        self.setAlternatingRowColors(False)
        self.setResizeGripsVisible(True)
        self.setColumnWidths([200] * 9)  # Column width multiply by the amount of columns
        self.setEnabled(True)
        self.fsm = QtWidgets.QFileSystemModel()
        self.fsm.setReadOnly(False)
        self.fsm.setIconProvider(ColumnViewFileIcon())
        self.setModel(self.fsm)
        self.setRootIndex(self.fsm.setRootPath(str(default_path)))
        self.clicked.connect(self.get_file_info)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)

        # File Category Labels
        self.preview_category_name = QtWidgets.QLabel('Name:')
        self.preview_category_size = QtWidgets.QLabel('Size:')
        self.preview_category_type = QtWidgets.QLabel('Type:')
        self.preview_category_date = QtWidgets.QLabel('Modified:')

        # Align Right for Prefix Labels
        align_right = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        self.preview_category_name.setAlignment(align_right)
        self.preview_category_size.setAlignment(align_right)
        self.preview_category_type.setAlignment(align_right)
        self.preview_category_date.setAlignment(align_right)

        # File Attributes Labels
        self.preview_file_name = QtWidgets.QLabel()
        self.preview_file_size = QtWidgets.QLabel()
        self.preview_file_type = QtWidgets.QLabel()
        self.preview_file_date = QtWidgets.QLabel()

        # File Attributes Layout and Value for Preview Pane
        self.sublayout_text = QtWidgets.QGridLayout()
        self.sublayout_text.addWidget(self.preview_category_name, 0, 0)
        self.sublayout_text.addWidget(self.preview_category_size, 1, 0)
        self.sublayout_text.addWidget(self.preview_category_type, 2, 0)
        self.sublayout_text.addWidget(self.preview_category_date, 3, 0)
        self.sublayout_text.addWidget(self.preview_file_name, 0, 1)
        self.sublayout_text.addWidget(self.preview_file_size, 1, 1)
        self.sublayout_text.addWidget(self.preview_file_type, 2, 1)
        self.sublayout_text.addWidget(self.preview_file_date, 3, 1)
        self.sublayout_text.setRowStretch(4, 1)  # Arrange layout to upper part of widget

        # Preview Thumbnails
        self.preview = QtWidgets.QLabel()
        self.sublayout_thumbnail = QtWidgets.QVBoxLayout()
        self.sublayout_thumbnail.addWidget(self.preview)
        self.sublayout_thumbnail.setAlignment(QtCore.Qt.AlignCenter)

        # Set Preview Pane for QColumnView
        self.preview_widget = QtWidgets.QWidget()
        self.preview_pane = QtWidgets.QVBoxLayout(self.preview_widget)
        self.preview_pane.addLayout(self.sublayout_thumbnail)
        self.preview_pane.addLayout(self.sublayout_text)
        self.setPreviewWidget(self.preview_widget)

    # Custom context menu handling for directory or file
    def context_menu(self, pos):
        """Custom context menu.

        Display different set of menu actions if directory or file.

        Parameters
        ----------
        pos : QtCore.QPoint

        """
        menu = QtWidgets.QMenu()
        idx = self.indexAt(pos)
        is_selection = idx.isValid()
        # Only show context menu if the cursor position is over a valid item
        if is_selection:
            selected_item = self.fsm.index(idx.row(), 0, idx.parent())
            file_name = str(self.fsm.fileName(selected_item))
            file_name = file_name[:50] + '...' if len(file_name) > 50 else file_name
            file_path = str(self.fsm.filePath(selected_item))

            is_dir = self.fsm.isDir(selected_item)
            if not is_dir:
                open_action = menu.addAction('Open ' + file_name)
                open_action.triggered.connect(lambda: open_file(file_path))

            reveal_action = menu.addAction(
                'Reveal in ' + getattr(FileManager, platform.system().upper()).value
            )
            reveal_action.triggered.connect(lambda: reveal_in_os(file_path))

            menu.exec_(self.mapToGlobal(pos))
            self.clearSelection()

    # Return selected item attributes in Model View for Preview Pane
    def get_file_info(self, idx):
        """Get file info.

        Retrieve file information for display in Preview tab.

        Parameters
        ----------
        idx : QtCore.QModelIndex
            QModelIndex using decorator method.

        Returns
        -------
        str
            File path.

        """
        selected_item = self.fsm.index(idx.row(), 0, idx.parent())

        # Retrieve File Attributes
        file_name = self.fsm.fileName(selected_item)
        file_size = self.fsm.size(selected_item)
        file_type = self.fsm.type(selected_item).split(' ')[0]
        file_date = self.fsm.lastModified(selected_item)
        file_path = self.fsm.filePath(selected_item)

        # Assign the File Attributes' string into respective labels
        self.preview_file_name.setText(file_name)
        self.preview_file_size.setText(get_file_size(file_size))
        self.preview_file_type.setText(file_type.upper() + ' file')
        self.preview_file_date.setText(file_date.toString('yyyy/MM/dd h:m AP'))

        # Retrieve image path for Thumbnail Preview
        image_path = self.fsm.filePath(selected_item)

        # Generate thumbnails for Preview Pane
        if image_path.lower().endswith(IMAGE_FORMAT):
            image = QtGui.QImageReader()
            image.setFileName(image_path)
            scaled_size = image.size()
            scaled_size.scale(MAX_SIZE, MAX_SIZE, QtCore.Qt.KeepAspectRatio)
            image.setScaledSize(scaled_size)
            thumbnail = QtGui.QPixmap.fromImage(image.read())
        else:
            file_info = QtCore.QFileInfo(image_path)  # Retrieve info like icons, path, etc
            file_icon = QtWidgets.QFileIconProvider().icon(file_info)
            thumbnail = file_icon.pixmap(48, 48, QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.preview.setPixmap(thumbnail)
        return file_path

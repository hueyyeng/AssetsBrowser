"""Assets Browser Custom Widgets"""
import platform

from PyQt5 import QtCore, QtGui, QtWidgets

from config.constants import IMAGE_FORMAT
from helpers.constants import FILE_MANAGER, SELECTED_FILE
from helpers.utils import get_file_size, open_file, reveal_in_os


class ColumnViewWidget(QtWidgets.QColumnView):
    def __init__(self):
        super().__init__()

        # File Category Labels
        preview_category_name = QtWidgets.QLabel('Name:')
        preview_category_size = QtWidgets.QLabel('Size:')
        preview_category_type = QtWidgets.QLabel('Type:')
        preview_category_date = QtWidgets.QLabel('Modified:')

        # Align Right for Prefix Labels
        align_right = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        preview_category_name.setAlignment(align_right)
        preview_category_size.setAlignment(align_right)
        preview_category_type.setAlignment(align_right)
        preview_category_date.setAlignment(align_right)

        # File Attributes Labels
        self.preview_file_name = QtWidgets.QLabel()
        self.preview_file_size = QtWidgets.QLabel()
        self.preview_file_type = QtWidgets.QLabel()
        self.preview_file_date = QtWidgets.QLabel()

        # File Attributes Layout and Value for Preview Pane
        sublayout_text = QtWidgets.QGridLayout()
        sublayout_text.addWidget(preview_category_name, 0, 0)
        sublayout_text.addWidget(preview_category_size, 1, 0)
        sublayout_text.addWidget(preview_category_type, 2, 0)
        sublayout_text.addWidget(preview_category_date, 3, 0)
        sublayout_text.addWidget(self.preview_file_name, 0, 1)
        sublayout_text.addWidget(self.preview_file_size, 1, 1)
        sublayout_text.addWidget(self.preview_file_type, 2, 1)
        sublayout_text.addWidget(self.preview_file_date, 3, 1)
        sublayout_text.setRowStretch(4, 1)  # Arrange layout to upper part of widget

        # Preview Thumbnails
        self.preview = QtWidgets.QLabel()
        sublayout_thumbnail = QtWidgets.QVBoxLayout()
        sublayout_thumbnail.addWidget(self.preview)
        sublayout_thumbnail.setAlignment(QtCore.Qt.AlignCenter)

        # Set Preview Pane for QColumnView
        preview_widget = QtWidgets.QWidget()
        preview_pane = QtWidgets.QVBoxLayout(preview_widget)
        preview_pane.addLayout(sublayout_thumbnail)
        preview_pane.addLayout(sublayout_text)
        self.setPreviewWidget(preview_widget)

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
            file_path = str(self.fsm.filePath(selected_item))
            SELECTED_FILE['File'] = file_name
            SELECTED_FILE['Path'] = file_path

            is_dir = self.fsm.isDir(selected_item)
            if not is_dir:
                open_action = menu.addAction('Open ' + SELECTED_FILE['File'])
                open_action.triggered.connect(lambda: open_file(SELECTED_FILE['Path']))

            reveal_action = menu.addAction(('Reveal in ' + FILE_MANAGER[platform.system()]))
            reveal_action.triggered.connect(lambda: reveal_in_os(SELECTED_FILE['Path']))

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
        file_name = str(self.fsm.fileName(selected_item))
        file_size = self.fsm.size(selected_item)
        file_type = str(self.fsm.type(selected_item))
        file_date = self.fsm.lastModified(selected_item)
        file_path = str(self.fsm.filePath(selected_item))

        SELECTED_FILE['File'] = file_name
        SELECTED_FILE['Path'] = file_path

        # Split file_type into array for easy formatting
        file_type_list = file_type.split(' ')

        # Assign the File Attributes' string into respective labels
        self.preview_file_name.setText(file_name)
        self.preview_file_size.setText(get_file_size(file_size))
        self.preview_file_type.setText(file_type_list[0].upper() + ' file')
        self.preview_file_date.setText(file_date.toString('yyyy/MM/dd h:m AP'))

        # Retrieve file_path for Thumbnail Preview in __init__
        image_path = self.fsm.filePath(selected_item)
        image_type = file_type[0:-5]
        image_types = IMAGE_FORMAT

        # Generate thumbnails for Preview Pane
        max_size = 150  # Thumbnails max size in pixels
        thumbnail_object = QtGui.QPixmap()
        thumbnail_object.load(image_path)
        if image_type in image_types:
            thumbnail = thumbnail_object.scaled(
                max_size,
                max_size,
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation,
            )
        else:
            file_info = QtCore.QFileInfo(image_path)  # Retrieve info like icons, path, etc
            file_icon = QtWidgets.QFileIconProvider().icon(file_info)
            thumbnail = file_icon.pixmap(48, 48, QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.preview.setPixmap(thumbnail)
        return file_path

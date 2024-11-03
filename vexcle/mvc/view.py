# Import built-in modules
import logging
import os
from typing import Union

# Import third-party modules
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

# Import local modules
from vexcle.widgets import CustomTableView
from vexcle.widgets import DropLabel


class View(QtWidgets.QWidget):
    build_item_single = QtCore.Signal(str)

    def __init__(self):
        """Initialize the View class."""
        super().__init__()
        self.drag_file = None
        self.master_layout = QtWidgets.QVBoxLayout(self)
        self.group_main_widgets = QtWidgets.QGroupBox(self)
        self.startup_view = DropLabel()
        self.table = CustomTableView()
        self.progress_bar = QtWidgets.QProgressBar()
        self.push_button = QtWidgets.QPushButton("Export to excel")

        self.setup_ui()

    def setup_ui(self):
        """Setup the UI."""
        self.setMinimumHeight(616)
        self.setMinimumWidth(655)

        self.progress_bar.hide()
        self.push_button.setVisible(False)
        self.setup_layout()
        self.group_main_widgets.setVisible(False)

    def setup_layout(self):
        """Setup the layout."""
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.push_button)
        self.group_main_widgets.setLayout(layout)
        self.master_layout.addWidget(self.group_main_widgets)
        self.master_layout.addWidget(self.startup_view)
        self.setLayout(self.master_layout)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        """Accept the drag and drop event."""
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    @staticmethod
    def _get_valid_url(event: QtGui.QDropEvent) -> Union[None, str]:
        """Get the valid url from the event.

        Args:
            event: Event from drag and drop process.

        Returns:
            If the url is valid, return the url. Otherwise, return None.

        """
        if event.mimeData().hasUrls and (len(event.mimeData().urls()) == 1):
            url = event.mimeData().urls()[0]
            path = str(url.toLocalFile())
            if os.path.exists(path) and os.path.isdir(path):
                return path
        return None

    def dropEvent(self, event: QtGui.QDropEvent):
        path = self._get_valid_url(event)
        if path:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            self.build_item_single.emit(path)
        else:
            logger = logging.getLogger(__name__)
            logger.warning("Please drop the folder try again.")

# Import built-in modules
import logging
import os

# Import third-party modules
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets


class CustomTableView(QtWidgets.QTableWidget):
    def __init__(self):
        super(CustomTableView, self).__init__()
        self.setObjectName("TableView")
        self.setup()

    def setup(self):
        header = self.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        vh = self.verticalHeader()
        vh.setVisible(False)
        vh.setMinimumHeight(1000)

    def resizeEvent(self, event):
        """ Resize all sections to content and user interactive """
        super(CustomTableView, self).resizeEvent(event)
        header = self.horizontalHeader()
        for column in range(header.count()):
            header.setSectionResizeMode(column,
                                        QtWidgets.QHeaderView.ResizeToContents)
            width = header.sectionSize(column)
            header.setSectionResizeMode(column,
                                        QtWidgets.QHeaderView.Interactive)
            header.resizeSection(column, width)

    def set_data(self, headers, data):
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels([header.NAME for header in headers])
        self.setRowCount(len(data))
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding))
        for index, info in enumerate(data):
            for column, header in enumerate(headers):
                item = QtWidgets.QTableWidgetItem()

                # if key == "thumbnail":
                #     self
                # else:
                item.setText(str(info[header.TEXT]))
                self.setItem(index, column, item)


class Thumbnail(QtWidgets.QLabel):
    def __init__(self, image_path):
        super(Thumbnail, self).__init__()
        self._pixomap = QtGui.QPixmap(image_path)
        self.setPixmap(self._pixomap)


class DropLabel(QtWidgets.QLabel):
    """Custom label that supports dropping and adds a file browser."""

    STYLE_DROPLABEL_NORMAL = """
    QLabel {
        background-color: #2f2f2f;
        border: 2px dotted #404040;
        color: #666666
    }
    """

    # Style of the DropLabel when having a selection hovering over it.
    STYLE_DROPLABEL_HOVER = """
    QLabel {
        background-color: #262626;
        border: 2px dotted #505050;
        color: #666666
    }
    """

    file_dropped = QtCore.Signal(str)
    clicked = QtCore.Signal()

    def __init__(self):
        """Initialize the DropLabel instance."""
        super(DropLabel, self).__init__()

        self.setAcceptDrops(True)

        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setWordWrap(True)
        self.set_style(hover=False)
        self.setText("drop a folder.")

    def set_style(self, hover=True):
        """Set style for the widget.

        We need to set the style over a string. Using a style sheet won't work
        because we are updating the style in the main window afterwards.

        Args:
            hover (bool, optional): If True use hover style, otherwise use
                normal style.

        """
        style = self.STYLE_DROPLABEL_HOVER if hover else \
            self.STYLE_DROPLABEL_NORMAL
        self.setStyleSheet(style)

    def dragEnterEvent(self, event):  # pylint: disable=invalid-name
        """Overwrite dragEnterEvent to set mimeData."""
        event.accept()
        self.set_style(hover=True)

    def dragLeaveEvent(self, event):  # pylint: disable=invalid-name
        """Overwrite dragEnterEvent to set mimeData."""
        event.accept()
        self.set_style(hover=False)

    @staticmethod
    def dragMoveEvent(event):  # pylint: disable=invalid-name
        """Overwrite dragMoveEvent to accept drags."""
        event.setDropAction(QtCore.Qt.CopyAction)
        event.accept()

    @staticmethod
    def _get_valid_url(event):
        """Accepts only single existing directory with any kind of content:
        files, subdirectories etc.

        Args:
            event (QtGui.QDropEvent): Event from drag and drop process.

        Returns:
            str: Valid url if the content is valid.

        """
        if event.mimeData().hasUrls and (len(event.mimeData().urls()) == 1):
            url = event.mimeData().urls()[0]
            path = str(url.toLocalFile())
            if os.path.exists(path) and os.path.isdir(path):
                return path
        return None

    def dropEvent(self, event):  # pylint: disable=invalid-name
        """Fire file_dropped signal."""
        path = self._get_valid_url(event)
        if path:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            self.file_dropped.emit(path)
        else:
            logger = logging.getLogger(__name__)
            logger.warning('Please drop the folder try again.')

    def mousePressEvent(self, event):  # pylint: disable=invalid-name
        """Emit signal when clicked the label.

        Args:
            event (QtQore.QEvent): Event instance.

        """
        super(DropLabel, self).mousePressEvent(event)
        self.clicked.emit()


class MessageDisplay(QtWidgets.QDialog):
    """Shows dialogues as stand alone application i.e. can be called from scripts
    that have no QApplication running.
    """

    INFO = QtWidgets.QMessageBox.information
    WARNING = QtWidgets.QMessageBox.warning
    CRITICAL = QtWidgets.QMessageBox.critical
    ABOUT = QtWidgets.QMessageBox.about

    def __init__(self, title, message, dialog=None):
        """
        Args:
            title (str): Window title.
            message (str): Text of body.
            dialog (QtWidgets.QMessageBox): information, warning, critical, about
                                         Default is INFO.

        """
        if not dialog:
            dialog = MessageDisplay.INFO
        self.app = QtWidgets.QApplication.instance()
        if self.app is None:
            self.app = QtWidgets.QApplication([])
        super(MessageDisplay, self).__init__()
        dialog(self, title, message)

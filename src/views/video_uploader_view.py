"""Video Uploader view implementation."""

from PySide6.QtCore import QLoggingCategory, qCInfo
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)

from src.views.base_view import BaseView


class VideoUploaderView(BaseView):
    """Display the video uploader interface."""

    # We need to declare this in this way just to handle the known issue: use-after-free
    # in python, in this case PySide6 when you create a category, PySide6 is creating a buffer
    # and this buffet pointing a different memory directions, for that reason fail.
    _CATEGORY = "skeleton.view.video_uploader"
    _log = QLoggingCategory(_CATEGORY)

    def __init__(self, parent=None):
        """Initialize the video uploader view.

        Parameters
        ----------
        parent : QWidget, optional
            Parent widget for the view.
        """
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Build the video uploader user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        # Video Form
        form_layout = QFormLayout()
        form_layout.setHorizontalSpacing(10)
        form_layout.setVerticalSpacing(10)
        # Title Field
        self._title_edit = QLineEdit()
        self._title_edit.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed,)
        form_layout.addRow(self.bind_text(
            QLabel(), lambda: self.tr("Title")), self._title_edit)
        # File Field
        file_layout = QHBoxLayout()
        file_layout.setSpacing(10)
        self._file_edit = QLineEdit()
        self._file_edit.setReadOnly(True)
        self._select_file_button = self.bind_text(
            QPushButton(), lambda: self.tr("&Select"))
        file_layout.addWidget(self._file_edit)
        file_layout.addWidget(self._select_file_button)
        form_layout.addRow(self.bind_text(
            QLabel(), lambda: self.tr("File")), file_layout)
        layout.addLayout(form_layout)
        # Platform select box
        platform_layout = QHBoxLayout()
        platform_layout.setSpacing(10)
        platform_layout.addWidget(self.bind_text(
            QLabel(), lambda: self.tr("Platform")))
        self._instagram_option = self.bind_text(
            QCheckBox(), lambda: self.tr("Instagram"))
        self._youtube_option = self.bind_text(
            QCheckBox(), lambda: self.tr("YouTube"))
        platform_layout.addWidget(self._instagram_option)
        platform_layout.addWidget(self._youtube_option)
        platform_layout.addStretch()
        layout.addLayout(platform_layout)
        # Description Field box
        self._description_edit = QPlainTextEdit()
        self._description_edit.setMinimumHeight(100)
        layout.addWidget(self.bind_text(
            QLabel(), lambda: self.tr("Description")))
        layout.addWidget(self._description_edit)
        # We want the same Logs field in all the views, for that reason
        # we have used the base_view to config the Logs field
        self.setup_log_panel(
            layout, ("skeleton.view.video_uploader", "skeleton.model.video_uploader"))
        # We want the same bottom buttons, for that reason
        # we have used the base_view to config the navigation buttons
        self.setup_navigation_buttons(layout)
        self._select_file_button.clicked.connect(
            self._action_select_file_button)

    def _action_select_file_button(self):
        """When we want to select the video to upload we need to select with this method"""
        qCInfo(self._log, "The video_button was clicked")
        path, _ = QFileDialog.getOpenFileName(
            self, self.tr("Select video"), "",
            "Videos (*.mp4 *.mov *.mkv *.avi);;All files (*)")
        if path:
            self._file_edit.setText(path)

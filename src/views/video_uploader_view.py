"""Video Uploader view implementation."""

from PySide6.QtCore import QLoggingCategory, qCDebug
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
        super().setup_ui()
        qCDebug(self._log, f"The class VideoUploaderView was created")

    def setup_ui(self):
        """Build the video uploader user interface."""
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
        self._content_layout.addLayout(form_layout)
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
        self._content_layout.addLayout(platform_layout)
        # Description Field box
        self._description_edit = QPlainTextEdit()
        self._description_edit.setMinimumHeight(100)
        self._content_layout.addWidget(self.bind_text(
            QLabel(), lambda: self.tr("Description")))
        self._content_layout.addWidget(self._description_edit)
        self._upload_video_button = self.bind_text(
            QPushButton(), lambda: self.tr("Upload &Video"))
        self._content_layout.addWidget(self._upload_video_button)
        self._select_file_button.clicked.connect(self._action_select_file_button)
        self._upload_video_button.clicked.connect(self._action_upload_video_button)
        qCDebug(self._log, f"The class VideoUploaderView was configured")

    def _action_select_file_button(self):
        """When we want to select the video to upload we need to select with this method"""
        qCDebug(self._log, "The select_file was clicked")
        path, _ = QFileDialog.getOpenFileName(
            self, self.tr("Select video"), "",
            "Videos (*.mp4 *.mov *.mkv *.avi);;All files (*)")
        if path:
            self._file_edit.setText(path)

    def _action_upload_video_button(self):
        """When we want to upload the video we need to click this button"""
        qCDebug(self._log, "The upload_video was clicked")
        pass
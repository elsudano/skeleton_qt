"""Model for the home view."""

from PySide6.QtCore import QLoggingCategory
from src.models.model import Model


class VideoUploaderModel(Model):
    """Provide application data and behaviour used by the Video Uploader view."""

    _log = QLoggingCategory("skeleton.model.video_uploader")

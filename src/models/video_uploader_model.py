"""Model for the home view."""

from PySide6.QtCore import QLoggingCategory

from src.models.model import Model


class VideoUploaderModel(Model):
    """Provide application data and behaviour used by the Video Uploader view."""

    # We need to declare this in this way just to handle the known issue: use-after-free
    # in python, in this case PySide6 when you create a category, PySide6 is creating a buffer
    # and this buffet pointing a different memory directions, for that reason fail.
    _CATEGORY = "skeleton.model.video_uploader"
    _log = QLoggingCategory(_CATEGORY)
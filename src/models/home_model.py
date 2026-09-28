"""Model for the home view."""

from PySide6.QtCore import QLoggingCategory
from src.models.model import Model


class HomeModel(Model):
    """Provide application data and behaviour used by the home view."""

    _log = QLoggingCategory("skeleton.model.home")

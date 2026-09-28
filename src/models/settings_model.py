"""Model for the settings view."""

from PySide6.QtCore import QLoggingCategory
from src.models.model import Model


class SettingsModel(Model):
    """Provide application data and behaviour used by the settings view."""

    _log = QLoggingCategory("skeleton.model.settings")

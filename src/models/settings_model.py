from PySide6.QtCore import QCoreApplication
from src.models.model import Model


class SettingsModel(Model):
    """Model for the settings view."""

    def get_title(self) -> str:
        """Return the settings title.

        Returns
        -------
        str
            Settings title. Model is a plain object
        """
        return QCoreApplication.translate("SettingsModel", "Settings")

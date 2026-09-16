from PySide6.QtCore import QCoreApplication
from src.models.model import Model


class HomeModel(Model):
    """Model for the home view."""

    def get_welcome_message(self) -> str:
        """Return the welcome message.

        Returns
        -------
        str
            Welcome message.
        """
        return QCoreApplication.translate("HomeModel", "Welcome to Skeleton Qt")

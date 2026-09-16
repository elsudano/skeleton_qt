from src.models.model import Model


class SettingsModel(Model):
    """Model for the settings view."""

    def get_title(self) -> str:
        """Return the settings title.

        Returns
        -------
        str
            Settings title.
        """
        return "Settings"

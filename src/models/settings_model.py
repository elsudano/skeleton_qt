from src.models.model import Model

class SettingsModel(Model):
    """Provide the application logic for the settings view."""

    def __init__(self):
        """Initialize the settings model."""
        super().__init__()

    def get_title(self):
        """Return the settings title.

        Returns
        -------
        str
            Settings title.
        """
        return "Application Settings"
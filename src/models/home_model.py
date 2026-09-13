from src.models.model import Model

class HomeModel(Model):
    """Provide the application logic for the home view."""

    def __init__(self):
        """Initialize the home model."""
        super().__init__()

    def get_welcome_message(self):
        """Return the welcome message.

        Returns
        -------
        str
            Welcome message displayed by the home view.
        """
        return "Welcome to the Qt Skeleton"
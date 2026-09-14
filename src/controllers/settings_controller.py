from src.controllers.controller import Controller

class SettingsController(Controller):
    """Coordinate communication between the settings view and model."""

    def __init__(self, view, model):
        """Initialize the settings controller.

        Parameters
        ----------
        view : SettingsView
            Settings view managed by the controller.
        model : SettingsModel
            Settings model containing the application logic.
        """
        super().__init__(view, model)
        self._load_settings()

    def _load_settings(self):
        """Load the settings information into the view."""
        title = self._model.get_title()
        self._view.set_title(title)
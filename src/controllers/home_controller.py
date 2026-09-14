from src.controllers.controller import Controller

class HomeController(Controller):
    """Coordinate communication between the home view and model."""

    def __init__(self, view, model):
        """Initialize the home controller.

        Parameters
        ----------
        view : HomeView
            Home view managed by the controller.
        model : HomeModel
            Home model containing the application logic.
        """
        super().__init__(view, model)
        self._connect_signals()

    def _connect_signals(self):
        """Connect view signals to controller handlers."""
        self._view.welcome_requested.connect(self._show_welcome_message)

    def _show_welcome_message(self):
        """Request the welcome message from the model."""
        message = self._model.get_welcome_message()
        self._view.set_message(message)
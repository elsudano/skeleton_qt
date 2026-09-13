from abc import ABC

class Controller(ABC):
    """Base class for application controllers.

    Coordinates communication between views and models.
    """

    def __init__(self, view, model):
        """Initialize the controller.

        Parameters
        ----------
        view : View
            View managed by the controller.
        model : Model
            Model containing the application logic.
        """
        super().__init__()
        self._view = view
        self._model = model
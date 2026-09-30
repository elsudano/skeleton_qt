"""Route Designer view implementation."""

from PySide6.QtCore import QLoggingCategory

from src.views.base_view import BaseView


class RouteDesignerView(BaseView):
    """Display the route designer interface."""

    # We need to declare this in this way just to handle the known issue: use-after-free
    # in python, in this case PySide6 when you create a category, PySide6 is creating a buffer
    # and this buffet pointing a different memory directions, for that reason fail.
    _CATEGORY = "skeleton.view.route_designer"
    _log = QLoggingCategory(_CATEGORY)

    def __init__(self, parent=None):
        """Initialize the route designer view.

        Parameters
        ----------
        parent : QWidget, optional
            Parent widget for the view.
        """
        super().__init__(parent)
        self.setup_ui()
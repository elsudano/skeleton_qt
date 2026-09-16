from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

class BaseView(QWidget):
    """Base class for application views."""

    navigation_requested = Signal(str)

    def __init__(self, parent=None):
        """Initialize the view.

        Parameters
        ----------
        parent : QWidget, optional
            Parent widget.
        """
        super().__init__(parent)

    def request_navigation(self, name: str):
        """Request navigation to another view.

        Parameters
        ----------
        name : str
            View identifier.
        """
        self.navigation_requested.emit(name)
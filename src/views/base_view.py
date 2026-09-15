from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

class BaseView(QWidget):
    """Base class for application views.

    Provides the common structure for views displayed inside the main window.
    """
    navigation_requested = Signal(str)

    def __init__(self, parent=None):
        """Initialize the view.

        Parameters
        ----------
        parent : QWidget, optional
            Parent widget.
        """
        super().__init__(parent)

    def setup_ui(self):
        """Build the graphical user interface.

        This method must be implemented by concrete views.
        """
        raise NotImplementedError

    def request_navigation(self, name: str):
        """Request navigation to another feature.

        Parameters
        ----------
        name : str
            Name of the requested feature.
        """
        self.navigation_requested.emit(name)
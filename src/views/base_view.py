from PySide6.QtCore import QEvent, Signal
from PySide6.QtWidgets import QWidget

class BaseView(QWidget):
    """Base class for application views."""

    navigation_requested = Signal(str)
    retranslated = Signal()

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

    def retranslate_ui(self):
        """Re-apply translatable texts. Override it; never touch user data."""

    def changeEvent(self, event):
        """Qt sends LanguageChange when a translator is installed or removed."""
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate_ui()
            self.retranslated.emit()
        super().changeEvent(event)
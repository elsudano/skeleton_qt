from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QLabel, QPushButton, QVBoxLayout,)
from src.views.base_view import BaseView

class HomeView(BaseView):
    """Display the home application view."""

    welcome_requested = Signal()

    def __init__(self, parent=None):
        """Initialize the home view.

        Parameters
        ----------
        parent : QWidget, optional
            Parent widget.
        """
        super().__init__(parent)

        self._message_label = None
        self._welcome_button = None

        self.setup_ui()

    def setup_ui(self):
        """Build the graphical user interface."""
        layout = QVBoxLayout(self)

        self._message_label = QLabel(self.tr("Press the button"))
        self._welcome_button = QPushButton(self.tr("Show welcome message"))

        layout.addWidget(self._message_label)
        layout.addWidget(self._welcome_button)

        self._welcome_button.clicked.connect(self._on_welcome_clicked)

    def _on_welcome_clicked(self):
        """Emit the signal requesting the welcome message."""
        self.welcome_requested.emit()

    def set_message(self, message):
        """Display a message in the view.

        Parameters
        ----------
        message : str
            Message to display.
        """
        self._message_label.setText(message)
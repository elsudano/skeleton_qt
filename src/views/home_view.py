from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton
from src.views.base_view import BaseView
from src.views.views import Views

class HomeView(BaseView):
    """Home view."""

    welcome_requested = Signal()

    def __init__(self, parent=None):
        """Initialize the home view.

        Parameters
        ----------
        parent : QWidget, optional
            Parent widget.
        """
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Build the home user interface."""
        layout = QVBoxLayout(self)
        self._message_label = QLabel(self.tr("Press the button"))
        self._welcome_button = QPushButton(self.tr("Show welcome message"))
        self._settings_button = QPushButton(self.tr("Show Settings"))
        layout.addWidget(self._message_label)
        layout.addWidget(self._welcome_button)
        layout.addWidget(self._settings_button)
        self._welcome_button.clicked.connect(self.welcome_requested.emit)
        self._settings_button.clicked.connect(lambda: self.request_navigation(Views.SETTINGS))

    def _set_message(self, message: str):
        """Set the message displayed by the view.

        Parameters
        ----------
        message : str
            Message to display.
        """
        self._message_label.setText(message)
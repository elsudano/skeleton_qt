from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QLabel, QPushButton, QVBoxLayout,)
from src.views.base_view import BaseView
from src.core.routes import Routes

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
        self._settings_button = None
        self.setup_ui()

    def setup_ui(self):
        """Build the graphical user interface."""
        layout = QVBoxLayout(self)
        self._message_label = QLabel(self.tr("Press the button"))
        self._welcome_button = QPushButton(self.tr("Show welcome message"))
        self._settings_button = QPushButton(self.tr("Settings"))
        layout.addWidget(self._message_label)
        layout.addWidget(self._welcome_button)
        layout.addWidget(self._settings_button)
        self._welcome_button.clicked.connect(self._on_welcome_clicked)
        self._settings_button.clicked.connect(self._on_settings_clicked)

    def _on_welcome_clicked(self):
        """Emit the signal requesting the welcome message."""
        self.welcome_requested.emit()

    def _on_settings_clicked(self):
        """Request navigation to the settings feature."""
        self.request_navigation(Routes.SETTINGS)

    def set_message(self, message: str):
        """Display a message in the view.

        Parameters
        ----------
        message : str
            Message to display.
        """
        self._message_label.setText(message)
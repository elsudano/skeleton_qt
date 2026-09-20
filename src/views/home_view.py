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
        self._has_message = False
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
        self.retranslate_ui()

    def retranslate_ui(self):
        """Apply translatable texts without touching the view's data."""
        self._welcome_button.setText(self.tr("Show welcome message"))
        self._settings_button.setText(self.tr("Show Settings"))
        if not self._has_message:
            self._message_label.setText(self.tr("Press the button"))

    @property
    def has_message(self) -> bool:
        """Return True if the label shows a message supplied by the model."""
        return self._has_message

    def _set_message(self, message: str):
        """Set the message displayed by the view.

        Parameters
        ----------
        message : str
            Message to display.
        """
        self._has_message = True
        self._message_label.setText(message)
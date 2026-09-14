from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QLabel, QPushButton, QVBoxLayout,)
from src.views.base_view import BaseView

class SettingsView(BaseView):
    """Display the application settings view."""

    home_requested = Signal()

    def __init__(self, parent=None):
        """Initialize the settings view.

        Parameters
        ----------
        parent : QWidget, optional
            Parent widget.
        """
        super().__init__(parent)
        self._title_label = None
        self._home_button = None
        self.setup_ui()

    def setup_ui(self):
        """Build the graphical user interface."""
        layout = QVBoxLayout(self)
        self._title_label = QLabel(self.tr("Settings"))
        self._home_button = QPushButton(self.tr("Back to Home"))
        layout.addWidget(self._title_label)
        layout.addWidget(self._home_button)
        self._home_button.clicked.connect(self._on_home_clicked)

    def _on_home_clicked(self):
        """Emit the signal requesting the home view."""
        self.home_requested.emit()

    def set_title(self, title):
        """Display the settings title.

        Parameters
        ----------
        title : str
            Title to display.
        """
        self._title_label.setText(title)
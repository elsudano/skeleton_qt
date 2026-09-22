"""Settings view."""

from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout

from src.views.base_view import BaseView
from src.views.views import Views


class SettingsView(BaseView):
    """Settings view."""

    def __init__(self, parent=None):
        """Initialize the settings view.

        Parameters
        ----------
        parent : QWidget, optional
            Parent widget.
        """
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Build the settings user interface."""
        layout = QVBoxLayout(self)
        self._title_label = self.bind_text(QLabel(), lambda: self.tr("View of Settings"))
        self._back_button = self.bind_text(QPushButton(), lambda: self.tr("Back"))
        layout.addWidget(self._title_label)
        layout.addWidget(self._back_button)
        self._back_button.clicked.connect(lambda: self.request_navigation(Views.HOME))

    def set_title(self, title):
        """Set the title displayed by the view.

        Parameters
        ----------
        title : callable or str
            Callable returning the title (it follows the active language)
            or a plain string.
        """
        self.bind_text(self._title_label, title)

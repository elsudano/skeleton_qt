"""Settings view implementation."""

from PySide6.QtCore import QLoggingCategory, Signal, qCInfo
from PySide6.QtWidgets import QCheckBox, QLabel, QListWidget, QPushButton, QVBoxLayout
from src.core import config
from src.views.base_view import BaseView
from src.views.views import Views


class SettingsView(BaseView):
    """Display application settings and runtime logging controls."""

    _log = QLoggingCategory("skeleton.view.settings")

    logging_gui_changed = Signal(bool)
    logging_categories_changed = Signal(object)

    def __init__(self, parent=None):
        """Initialize the settings view.

        Parameters
        ----------
        controller : Controller
            Global application controller.
        parent : QWidget, optional
            Parent widget for the view."""
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Build the settings user interface."""
        layout = QVBoxLayout(self)
        if config.LOG_OUTPUT_GUI in config.LOG_OUTPUTS:
            self._logging_label = self.bind_text(
                QLabel(), lambda: self.tr("GUI logging"))
            self._logging_output = QCheckBox()
            self.bind_text(self._logging_output,
                           lambda: self.tr("Enable GUI logging"))
            self._logging_output.setChecked(config.LOG_GUI_ENABLED)
            self._logging_output.toggled.connect(self._on_gui_logging_toggled)
            layout.addWidget(self._logging_label)
            layout.addWidget(self._logging_output)
            self._categories_label = self.bind_text(
                QLabel(), lambda: self.tr("Logging categories"))
            self._categories = QListWidget()
            self._categories.setSelectionMode(
                QListWidget.SelectionMode.ExtendedSelection)
            for category in config.LOG_CATEGORIES:
                self._categories.addItem(category)
            self._categories.selectAll()
            self._categories.itemSelectionChanged.connect(
                self._emit_categories)
            layout.addWidget(self._categories_label)
            layout.addWidget(self._categories)
        self.setup_log_panel(
            layout, ("skeleton.view.settings", "skeleton.model.settings"))
        # We want the same bottom buttons, for that reason
        # we have used the base_view to config the navigation buttons
        self.setup_navigation_buttons(layout)

    def _on_gui_logging_toggled(self, enabled: bool):
        """Notify the controller about the GUI logging state.

        Parameters
        ----------
        enabled : bool
            Whether GUI log delivery should be enabled."""
        qCInfo(self._log, f"GUI logging enabled: {enabled}")
        self.logging_gui_changed.emit(enabled)

    def _emit_categories(self):
        """Emit the currently selected logging categories.

        Parameters
        ----------
        categories : Iterable[str]
            Logging categories selected by the user."""
        selected = {item.text() for item in self._categories.selectedItems()}
        qCInfo(self._log, f"The categories: {selected} were selected")
        self.logging_categories_changed.emit(selected)

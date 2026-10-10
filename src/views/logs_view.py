"""Global log view implementation."""

from PySide6.QtCore import QLoggingCategory, Signal, qCDebug, qCInfo
from PySide6.QtWidgets import (
    QLabel,
    QPlainTextEdit,
    QPushButton,
)

from src.core.category_discovery import CategoryDiscovery
from src.views.base_view import Base_View
from src.views.custom_widgets.checkable_combobox import CheckableComboBox


class Logs_View(Base_View):
    """Display the complete application log history and incoming messages."""

    # We need to declare this in this way just to handle the known issue: use-after-free
    # in python, in this case PySide6 when you create a category, PySide6 is creating a buffer
    # and this buffet pointing a different memory directions, for that reason fail.
    _CATEGORY = "skeleton.view.logs_view"
    _log = QLoggingCategory(_CATEGORY)

    clear_requested = Signal()
    category_filter_changed = Signal(tuple)

    def __init__(self, parent=None):
        """Initialize the log view.

        Parameters
        ----------
        parent : QWidget, optional
            Parent widget for the view."""
        super().__init__(parent)
        self._all_records = []
        self.setup_ui()
        super().setup_ui()
        qCInfo(self._log, "The class Logs_View was created")
        qCDebug(self._log, "The class Logs_View was created")

    def setup_ui(self):
        """Build the log viewer interface."""
        self._log_text = QPlainTextEdit()
        self._log_text.setReadOnly(True)
        self._log_text.setMaximumBlockCount(2000)
        self._clear_button = self.bind_text(
            QPushButton(), lambda: self.tr("Clear logs")
        )
        self._category_filter_label = self.bind_text(
            QLabel(), lambda: self.tr("Categories:")
        )
        categories = CategoryDiscovery.discover_from_source("src")
        self._category_filter = CheckableComboBox()
        for category in categories:
            self._category_filter.add_item(category)
        self._content_layout.addWidget(self._category_filter_label)
        self._content_layout.addWidget(self._category_filter)
        self._content_layout.addWidget(self._log_text)
        self._content_layout.addWidget(self._clear_button)
        self._category_filter.selection_changed.connect(self._on_category_selection_changed)
        self._clear_button.clicked.connect(self.clear_requested.emit)
        qCDebug(self._log, "The class Logs_View was configured")

    def _on_category_selection_changed(self):
        """Handle changes in category filter selection.

        Emits a signal to request a log refresh with the new filter.
        """
        qCDebug(self._log, f"Category filter changed to: {sorted(self._category_filter.checked_items())}")
        self.category_filter_changed.emit(sorted(self._category_filter.checked_items()))
        self._refresh_logs()

    def _refresh_logs(self):
        """Refresh the log display based on the current filter."""
        selected_categories = self._category_filter.checked_items()
        if not selected_categories:
            # Show all logs
            self._log_text.clear()
            for record in self._all_records:
                self._log_text.appendPlainText(record.formatted)
        else:
            # Filter logs by selected categories
            self._log_text.clear()
            for record in self._all_records:
                if record.category in selected_categories or any(
                    record.category.startswith(f"{cat}.") for cat in selected_categories
                ):
                    self._log_text.appendPlainText(record.formatted)
        qCDebug(self._log, f"Logs refreshed with {len(self._all_records)} records (filtered to {len(selected_categories) if selected_categories else 'all'} categories)")

    def load_history(self, lines):
        """Load persisted log lines into the viewer.

        Parameters
        ----------
        lines : Iterable[str]
            Log lines to display."""
        self._log_text.setPlainText("\n".join(lines))
        qCDebug(self._log, "The Logs history was loaded")
        # Parse lines to extract category, level, message and formatted text
        for line in lines:
            parts = line.split(" - ", 2)
            if len(parts) >= 3:
                category = parts[0]
                level = parts[1]
                message = parts[2]
                formatted = line
                self._all_records.append(type('obj', (object,), {
                    'category': category,
                    'level': level,
                    'message': message,
                    'formatted': formatted
                })())

    def append_log(self, category: str, level: str, message: str, formatted: str):
        """Append a log message to the global log viewer.

        Parameters
        ----------
        category : str
            Logging category that produced the message.
        level : str
            Human-readable logging level.
        message : str
            Log message text.
        formatted : str
            Fully formatted message ready for display."""
        # Store the record for filtering
        self._all_records.append(type('obj', (object,), {
            'category': category,
            'level': level,
            'message': message,
            'formatted': formatted
        })())

        # Apply filter to display
        if not self._category_filter.checked_items():
            # Show all if no filter is selected
            self._log_text.appendPlainText(formatted)
        elif category in self._category_filter.checked_items() or any(
            category.startswith(f"{cat}.") for cat in self._category_filter.checked_items()
        ):
            self._log_text.appendPlainText(formatted)

    def clear(self):
        """Clear displayed log messages."""
        qCDebug(self._log, "The Logs history was cleaned")
        self._log_text.clear()
        self._all_records.clear()
        self._category_filter.clear()

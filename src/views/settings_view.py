"""Settings view implementation."""

from PySide6.QtCore import QLoggingCategory, Signal, qCInfo, qCDebug
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from src.core import config
from src.views.base_view import BaseView
from src.views.custom_widgets.checkable_combobox import CheckableComboBox


class SettingsView(BaseView):
    """Display application settings and runtime logging controls."""

    # We need to declare this in this way just to handle the known issue: use-after-free
    # in python, in this case PySide6 when you create a category, PySide6 is creating a buffer
    # and this buffet pointing a different memory directions, for that reason fail.
    _CATEGORY = "skeleton.view.settings"
    _log = QLoggingCategory(_CATEGORY)

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
        super().setup_ui()
        qCInfo(self._log, f"The class SettingsView was created")
        qCDebug(self._log, f"The class SettingsView was created")

    def setup_ui(self):
        """Build the settings user interface."""
        columns_layout = QHBoxLayout()

        # Left column: user interface preferences and enabled platforms.
        left_column = QVBoxLayout()
        left_column.addWidget(self._section_header(
            lambda: self.tr("User interface")))

        left_column.addWidget(self._section_header(
            lambda: self.tr("Enabled platforms")))
        platforms_toggles_row = QHBoxLayout()
        self._youtube_option = self.bind_text(
            QCheckBox(), lambda: self.tr("YouTube"))
        self._instagram_option = self.bind_text(
            QCheckBox(), lambda: self.tr("Instagram"))
        platforms_toggles_row.addWidget(self._youtube_option)
        platforms_toggles_row.addWidget(self._instagram_option)
        platforms_toggles_row.addStretch()
        left_column.addLayout(platforms_toggles_row)
        left_column.addStretch()

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)

        # Right column: logging system configuration.
        right_column = QVBoxLayout()
        right_column.addWidget(self._section_header(
            lambda: self.tr("Logging system")))

        # "Enable logging" and "Clear log file on exit" live in the same
        # row; "Enable logging" only exists when GUI output is configured,
        # "Clear log file on exit" is independent of that setting.
        logging_toggles_row = QHBoxLayout()
        if config.LOG_OUTPUT_GUI in config.LOG_OUTPUTS:
            self._logging_output = self.bind_text(
                QCheckBox(), lambda: self.tr("Enable logging"))
            self._logging_output.setChecked(config.LOG_GUI_ENABLED)
            self._logging_output.toggled.connect(
                self._on_gui_logging_toggled)
            logging_toggles_row.addWidget(self._logging_output)

            self._categories = CheckableComboBox()
            for category in config.LOG_CATEGORIES:
                self._categories.add_item(category, checked=True)
            self._categories.selection_changed.connect(
                self._emit_categories)

        self._clear_file_on_exit_option = self.bind_text(
            QCheckBox(), lambda: self.tr("Clear log file on exit"))
        self._clear_file_on_exit_option.setChecked(True)
        logging_toggles_row.addWidget(self._clear_file_on_exit_option)
        logging_toggles_row.addStretch()
        right_column.addLayout(logging_toggles_row)

        # "Log Type:" and its dropdown always share a row, right below the
        # toggles, only when the dropdown above was actually created.
        if config.LOG_OUTPUT_GUI in config.LOG_OUTPUTS:
            log_type_row = QHBoxLayout()
            log_type_row.addWidget(self.bind_text(
                QLabel(), lambda: self.tr("Log Type:")))
            log_type_row.addWidget(self._categories)
            right_column.addLayout(log_type_row)

        file_row = QHBoxLayout()
        file_row.addWidget(self.bind_text(
            QLabel(), lambda: self.tr("Logs File:")))
        self._log_file_edit = QLineEdit()
        self._log_file_edit.setReadOnly(True)
        self._select_log_file_button = self.bind_text(
            QPushButton(), lambda: self.tr("&Select"))
        self._select_log_file_button.clicked.connect(
            self._action_select_log_file_button)
        file_row.addWidget(self._log_file_edit)
        file_row.addWidget(self._select_log_file_button)
        right_column.addLayout(file_row)
        right_column.addStretch()

        # Equal stretch factors keep the split at 50/50 no matter how the
        # view is resized, so the separator always sits in the middle.
        columns_layout.addLayout(left_column, 1)
        columns_layout.addWidget(separator)
        columns_layout.addLayout(right_column, 1)
        self._content_layout.addLayout(columns_layout)
        qCDebug(self._log, f"The class SettingsView was configured")

    def _section_header(self, text_source) -> QLabel:
        """Create a bold section header label bound to the active language.

        Parameters
        ----------
        text_source : callable
            Callable returning the translated header text.

        Returns
        -------
        QLabel
            Bold label kept in sync with the active language."""
        label = self.bind_text(QLabel(), text_source)
        font = label.font()
        font.setBold(True)
        label.setFont(font)
        qCDebug(self._log, f"We have set the bold property in {text_source()} font header.")
        return label

    def _action_select_log_file_button(self):
        """Open a file dialog to pick the log file to display."""
        qCDebug(self._log, "The select_log_file_button was clicked")
        path, _ = QFileDialog.getOpenFileName(
            self, self.tr("Select log file"), "",
            "Log files (*.log);;All files (*)")
        if path:
            self._log_file_edit.setText(path)

    def _on_gui_logging_toggled(self, enabled: bool):
        """Notify the controller about the GUI logging state.

        Parameters
        ----------
        enabled : bool
            Whether GUI log delivery should be enabled."""
        qCDebug(self._log, f"GUI logging enabled: {enabled}")
        self.logging_gui_changed.emit(enabled)

    def _emit_categories(self):
        """Emit the currently selected logging categories."""
        selected = self._categories.checked_items()
        qCDebug(self._log, f"The categories: {selected} were selected")
        self.logging_categories_changed.emit(selected)

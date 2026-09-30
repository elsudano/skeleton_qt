"""Home view implementation."""

from PySide6.QtCore import QLoggingCategory, qCCritical, qCInfo
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QVBoxLayout

from src.core.config import BUTTON_MINIMUM_HEIGHT_SIZE, BUTTON_MINIMUM_WIDTH_SIZE
from src.views.base_view import BaseView
from src.views.views import Views


class HomeView(BaseView):
    """Display the home view and handle its user interactions."""

    # We need to declare this in this way just to handle the known issue: use-after-free
    # in python, in this case PySide6 when you create a category, PySide6 is creating a buffer
    # and this buffet pointing a different memory directions, for that reason fail.
    _CATEGORY = "skeleton.view.home"
    _log = QLoggingCategory(_CATEGORY)
    _buttons_per_row = 2

    def __init__(self, parent=None):
        """Initialize the home view.

        Parameters
        ----------
        controller : Controller
            Global application controller used for navigation and events.
        parent : QWidget, optional
            Parent widget for the view."""
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Build the home user interface."""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # We can create a new button in Home just adding a new one in this list
        buttons = (
            ("_video_button", lambda: self.tr(
                "Video &Uploader"), self._action_video_button),
            ("_route_button", lambda: self.tr(
                "Route &Designer"), self._action_route_button),
            ("_settings_button", lambda: self.tr(
                "&Settings"), self._action_settings_button),
            ("_logs_button", lambda: self.tr("&Logs"), self._action_logs_button),
            ("_empty1_button", lambda: self.tr(
                "&Empty1"), self._action_empty1_button),
        )
        for row_start in range(0, len(buttons), self._buttons_per_row):
            row_layout = QHBoxLayout()
            row_layout.setSpacing(10)
            for attr_name, text, callback in buttons[row_start:row_start + self._buttons_per_row]:
                button = self.bind_text(QPushButton(), text)
                button.setMinimumHeight(BUTTON_MINIMUM_HEIGHT_SIZE)
                button.setMinimumWidth(BUTTON_MINIMUM_WIDTH_SIZE)
                button.setSizePolicy(
                    QSizePolicy.Policy.Expanding,
                    QSizePolicy.Policy.Fixed,
                )
                if callback is not None:
                    button.clicked.connect(callback)
                setattr(self, attr_name, button)
                row_layout.addWidget(button)
            layout.addLayout(row_layout)
        # We want the same Logs field in all the views, for that reason
        # we have used the base_view to config the Logs field
        self.setup_log_panel(
            layout, ("skeleton.view.home", "skeleton.model.home",))
        # We want the same bottom buttons, for that reason
        # we have used the base_view to config the navigation buttons
        self.setup_navigation_buttons(layout)

    def _action_video_button(self):
        """This will be the actions that we can make when we press video_button"""
        qCInfo(self._log, "The video_button was clicked")
        self.request_navigation(Views.VIDEO_UPLOADER)

    def _action_route_button(self):
        """This will be the actions that we can make when we press route_button"""
        qCInfo(self._log, "The route_button was clicked")
        self.request_navigation(Views.ROUTE_DESIGNER)

    def _action_settings_button(self):
        """This will be the actions that we can make when we press settings_button"""
        qCInfo(self._log, "The settings_button was clicked")
        self.request_navigation(Views.SETTINGS)

    def _action_empty1_button(self):
        """This will be the actions that we can make when we press empty1_button.

        DEMO ONLY: also logs a CRITICAL message to prove every QtMsgType level
        (DEBUG/INFO/WARNING/CRITICAL/FATAL) flows through the same logging
        pipeline."""
        qCInfo(self._log, "The empty1_button was clicked")
        qCCritical(self._log, "Demo CRITICAL message: This message ")

    def _action_logs_button(self):
        """This will be the actions that we can make when we press logs_button"""
        qCInfo(self._log, "The logs_button was clicked")
        self.request_navigation(Views.LOGS)

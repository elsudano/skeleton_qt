"""Home view implementation."""

from PySide6.QtCore import QLoggingCategory, qCInfo
from PySide6.QtWidgets import (
    QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout)
from src.views.base_view import BaseView
from src.views.views import Views


class HomeView(BaseView):
    """Display the home view and handle its user interactions."""

    _log = QLoggingCategory("skeleton.view.home")

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
        # Horizontal Box for Buttons
        buttons_line1_layout = QHBoxLayout()
        buttons_line1_layout.setSpacing(10)
        self._video_button = self.bind_text(
            QPushButton(), lambda: self.tr("&Video"),)
        self._route_button = self.bind_text(
            QPushButton(), lambda: self.tr("&Route"),)
        self._settings_button = self.bind_text(
            QPushButton(), lambda: self.tr("&Settings"),)
        for button in (self._video_button, self._route_button, self._settings_button,):
            button.setMinimumHeight(50)
            button.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed,)
            buttons_line1_layout.addWidget(button)
        layout.addLayout(buttons_line1_layout)
        # Horizontal Box for Buttons
        buttons_line2_layout = QHBoxLayout()
        buttons_line2_layout.setSpacing(10)
        self._empty1_button = self.bind_text(
            QPushButton(), lambda: self.tr("&Empty1"),)
        self._empty2_button = self.bind_text(
            QPushButton(), lambda: self.tr("&Empty2"),)
        self._logs_button = self.bind_text(
            QPushButton(), lambda: self.tr("&Logs"),)
        for button in (self._empty1_button, self._empty2_button, self._logs_button,):
            button.setMinimumHeight(50)
            button.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed,)
            buttons_line2_layout.addWidget(button)
        layout.addLayout(buttons_line2_layout)
        # Label for Logs field
        logs_label = self.bind_text(QLabel(), lambda: self.tr("Logs"),)
        layout.addWidget(logs_label)
        # We want the same Logs field in all the views, for that reason
        # we have used the base_view to config the Logs field
        self.setup_log_panel(
            layout, ("skeleton.view.home", "skeleton.model.home",),)
        # We want the same bottom buttons, for that reason
        # we have used the base_view to config the navigation buttons
        self.setup_navigation_buttons(layout)
        self._video_button.clicked.connect(self._action_video_button)
        self._route_button.clicked.connect(self._action_route_button)
        self._settings_button.clicked.connect(self._action_settings_button)
        self._empty1_button.clicked.connect(self._action_empty1_button)
        self._empty2_button.clicked.connect(self._action_empty2_button)
        self._logs_button.clicked.connect(self._action_logs_button)

    def _action_video_button(self):
        """This will be the actions that we can make when we press video_button"""
        qCInfo(self._log, "The video_button was clicked")
        self.request_navigation(Views.VIDEO_UPLOADER)

    def _action_route_button(self):
        """This will be the actions that we can make when we press route_button"""
        qCInfo(self._log, "The route_button was clicked")
        self.request_navigation(Views.ROUTE)

    def _action_settings_button(self):
        """This will be the actions that we can make when we press settings_button"""
        qCInfo(self._log, "The settings_button was clicked")
        self.request_navigation(Views.SETTINGS)

    def _action_empty1_button(self):
        """This will be the actions that we can make when we press empty1_button"""
        qCInfo(self._log, "The empty1_button was clicked")
        self.request_navigation(Views.EMPTY1)

    def _action_empty2_button(self):
        """This will be the actions that we can make when we press empty2_button"""
        qCInfo(self._log, "The empty2_button was clicked")
        self.request_navigation(Views.EMPTY2)

    def _action_logs_button(self):
        """This will be the actions that we can make when we press logs_button"""
        qCInfo(self._log, "The logs_button was clicked")
        self.request_navigation(Views.LOGS)

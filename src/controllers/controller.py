"""Global controller coordinating view and model lifecycle and communication."""

from PySide6.QtCore import QLoggingCategory, QObject, qCInfo
from src.core.logging import LoggingManager
from src.models.home_model import HomeModel
from src.models.video_uploader_model import VideoUploaderModel
from src.models.logs_model import LogsModel
from src.models.settings_model import SettingsModel
from src.views.home_view import HomeView
from src.views.video_uploader_view import VideoUploaderView
from src.views.logs_view import LogsView
from src.views.settings_view import SettingsView
from src.views.views import Views


class Controller(QObject):
    """Coordinate view and model creation, caching, navigation, and signal-based communication."""

    # We need to declare this in this way just to handle the known issue: use-after-free
    # in python, in this case PySide6 when you create a category, PySide6 is creating a buffer
    # and this buffet pointing a different memory directions, for that reason fail.
    _CATEGORY = "skeleton.controller"
    _log = QLoggingCategory(_CATEGORY)

    def __init__(self, navigation_container, logging_manager: LoggingManager):
        """Initialize the controller.

        Parameters
        ----------
        main_window : MainWindow
            Main application window used as the navigation host.
        logging_manager : LoggingManager
            Central logging infrastructure used to distribute log messages."""
        super().__init__()
        self._navigation_container = navigation_container
        self._logging_manager = logging_manager
        self._cache = {}
        self._register_views()
        self._logging_manager.message_logged.connect(self._on_log_message)

    def _register_views(self):
        """Register the available view factories."""
        self._factories = {
            Views.HOME: (HomeView, HomeModel),
            Views.VIDEO_UPLOADER: (VideoUploaderView, VideoUploaderModel),
            Views.SETTINGS: (SettingsView, SettingsModel),
            Views.LOGS: (LogsView, lambda: LogsModel(self._logging_manager)),
        }

    def _create_view_model(self, name: str):
        """Create and cache a view and model tuple.

        Parameters
        ----------
        name : str
            Identifier of the view to create.

        Returns
        -------
        Tuple[BaseView, Model]
            Newly created view and its associated model."""
        qCInfo(self._log, f"Creating view: {name}")
        view_factory, model_factory = self._factories[name]
        view = view_factory()
        model = model_factory()
        self._cache[name] = (view, model)
        self._connect_view(view, model)
        self._initialize_view(view, model)
        self._navigation_container.addWidget(view)
        if isinstance(view, LogsView):
            history = model.file_lines()
            view.load_history(history)
            if not history:
                records = model.records()
                for record in records:
                    view.append_log(record.category, record.level,
                                    record.message, record.formatted)
        else:
            records = self._logging_manager.records()
            for record in records:
                view.append_log(record.category, record.level,
                                record.message, record.formatted)
        return view, model

    def _get_view_model(self, name: str):
        """Return a cached view and model tuple, creating it lazily when necessary.

        Parameters
        ----------
        name : str
            Identifier of the requested view.

        Returns
        -------
        Tuple[BaseView, Model]
            Cached or newly created view and model."""
        if name not in self._cache:
            return self._create_view_model(name)
        return self._cache[name]

    def _connect_view(self, view, model):
        """Connect view signals to controller handlers.

        Parameters
        ----------
        name : str
            Identifier of the view being connected.
        view : BaseView
            View whose signals should be connected.
        model : Model
            Model associated with the view."""
        view.navigation_requested.connect(self.navigate)
        if isinstance(view, HomeView):
            pass
        if isinstance(view, SettingsView):
            view.logging_gui_changed.connect(
                self._logging_manager.set_gui_enabled)
            view.logging_categories_changed.connect(
                self._logging_manager.set_categories)
        if isinstance(view, LogsView):
            view.clear_requested.connect(view.clear)

    def _initialize_view(self, view, model):
        """Initialize view data from its model.

        Parameters
        ----------
        view : BaseView
            View to initialize.
        model : Model
            Model associated with the view."""
        pass

    def _on_log_message(self, category: str, level: str, message: str, formatted: str):
        """Forward a log message to every cached view that accepts it.

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
        for view, _ in self._cache.values():
            view.append_log(category, level, message, formatted)

    def navigate(self, name: str):
        """Navigate to a view and make it the current view.

        Parameters
        ----------
        name : str
            Identifier of the target view."""
        qCInfo(self._log, f"Navigating to view: {name}")
        view, _ = self._get_view_model(name)
        self._navigation_container.setCurrentWidget(view)

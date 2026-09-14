from PySide6.QtWidgets import QApplication
from src.controllers.home_controller import HomeController
from src.controllers.settings_controller import SettingsController
from src.core.navigation import Navigation
from src.models.home_model import HomeModel
from src.models.settings_model import SettingsModel
from src.views.main_window import MainWindow
from src.views.home_view import HomeView
from src.views.settings_view import SettingsView

class Application:
    """Manage the application lifecycle and components."""

    def __init__(self, qt_application):
        """Initialize the application.

        Parameters
        ----------
        qt_application : QApplication
            Qt application instance.
        """
        self._qt_application = qt_application
        self._window = None
        self._navigation = None
        self._views = {}
        self._models = {}
        self._controllers = {}

    def start(self):
        """Initialize and display the application."""
        self._create_components()
        self._configure_navigation()
        self._configure_window()
        self._window.show()

    def _create_components(self):
        """Create application components."""
        self._create_main_window()
        self._create_navigation()
        self._create_home()
        self._create_settings()

    def _create_main_window(self):
        """Create the main application window."""
        self._window = MainWindow()

    def _create_navigation(self):
        """Create the application navigation manager."""
        self._navigation = Navigation()

    def _create_home(self):
        """Create and store the home components."""
        model = HomeModel()
        view = HomeView()
        controller = HomeController(view=view, model=model,)
        self._models["home"] = model
        self._views["home"] = view
        self._controllers["home"] = controller

    def _create_settings(self):
        """Create and store the settings components."""
        model = SettingsModel()
        view = SettingsView()
        controller = SettingsController(view=view, model=model,)
        self._models["settings"] = model
        self._views["settings"] = view
        self._controllers["settings"] = controller

    def _configure_navigation(self):
        """Configure application views and navigation events."""
        for name, view in self._views.items():
            self._navigation.add_view(name, view)
        self._views["home"].settings_requested.connect(lambda: self._navigation.show_view("settings"))
        self._views["settings"].home_requested.connect(lambda: self._navigation.show_view("home"))
        self._navigation.show_view("home")

    def _configure_window(self):
        """Configure the main application window."""
        self._window.set_central_widget(self._navigation.widget())
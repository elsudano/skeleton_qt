from PySide6.QtWidgets import QApplication
from src.core.feature_registry import FeatureRegistry
from src.core.navigation import Navigation
from src.views.main_window import MainWindow
from src.core.feature_definitions import FEATURES
from src.core.routes import Routes

class Application:
    """Manage the application lifecycle and components."""

    def __init__(self, qt_application: QApplication):
        """Initialize the application.

        Parameters
        ----------
        qt_application : QApplication
            Qt application instance.
        """
        self._qt_application = qt_application
        self._window = None
        self._navigation = None
        self._feature_registry = None
        self._initialize_infrastructure()
        self._register_features()

    def start(self):
        """Initialize and display the application."""
        self._configure_window()
        self._configure_menus()
        self.navigate_to(Routes.HOME)
        self._window.show()

    def _initialize_infrastructure(self):
        """Initialize the application infrastructure."""
        self._window = MainWindow()
        self._navigation = Navigation()
        self._feature_registry = FeatureRegistry()

    def navigate_to(self, name: str):
        """Navigate to a registered feature.

        The feature is created lazily the first time it is
        requested.

        Parameters
        ----------
        name : str
            Name of the requested feature.
        """
        feature = self._feature_registry.get(name)
        self._connect_feature_navigation(feature)
        if not self._navigation.has_view(name):
            self._navigation.add_view(name=name,view=feature.view,)
        self._navigation.show_view(name)

    def _connect_feature_navigation(self, feature):
        """Connect navigation signals for a feature.

        Parameters
        ----------
        feature : FeatureInstance
            Feature whose navigation signals must be connected.
        """
        if feature.navigation_connected:
            return
        feature.view.navigation_requested.connect(self.navigate_to)
        feature.navigation_connected = True

    def _register_features(self):
        """Register all available application features."""
        for feature in FEATURES:
            self._feature_registry.register(
                name=feature.name,
                factory=feature.factory,
        )

    def _configure_window(self):
        """Configure the main application window."""
        self._window.set_central_widget(self._navigation.widget())

    def _configure_menus(self):
        """Configure the application menus."""
        self._window.add_action(menu_name="views", action_name=Routes.HOME, title=self._window.tr("Home"), callback=lambda: self.navigate_to(Routes.HOME),)
        self._window.add_action(menu_name="views", action_name=Routes.SETTINGS, title=self._window.tr("Settings"), callback=lambda: self.navigate_to(Routes.SETTINGS),)
        self._window.add_action(menu_name="file", action_name="exit", title=self._window.tr("Exit"), callback=self._qt_application.quit,)

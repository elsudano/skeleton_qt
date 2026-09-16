from PySide6.QtCore import QObject
from src.models.home_model import HomeModel
from src.models.settings_model import SettingsModel
from src.views.home_view import HomeView
from src.views.settings_view import SettingsView
from src.views.views import Views

class Controller(QObject):
    """Global application controller."""

    def __init__(self, navigation_container):
        """Initialize the controller.

        Parameters
        ----------
        navigation_container : QStackedWidget
            Container used to display views.
        """
        super().__init__()
        self._navigation_container = navigation_container
        self._cache = {}
        self._register_views()

    def _register_views(self):
        """Register available views."""
        self._factories = {
            Views.HOME: (HomeView, HomeModel),
            Views.SETTINGS: (SettingsView, SettingsModel),
        }

    def _create_view_model(self, name: str):
        """Create and cache a view and model tuple.

        Parameters
        ----------
        name : str
            View identifier.

        Returns
        -------
        tuple
            View and model pair.
        """
        view_factory, model_factory = self._factories[name]
        view = view_factory()
        model = model_factory()
        pair = (view, model)
        self._cache[name] = pair
        self._connect_view(view)
        self._navigation_container.addWidget(view)
        return pair

    def _get_view_model(self, name: str):
        """Return a cached view and model tuple.

        Parameters
        ----------
        name : str
            View identifier.

        Returns
        -------
        tuple
            View and model pair.
        """
        if name not in self._cache:
            return self._create_view_model(name)
        return self._cache[name]

    def _connect_view(self, view):
        """Connect view signals to controller handlers.

        Parameters
        ----------
        view : BaseView
            View whose signals should be connected.
        """
        view.navigation_requested.connect(self.navigate)

    def navigate(self, name: str):
        """Navigate to a view.

        Parameters
        ----------
        name : str
            View identifier.
        """
        view, _ = self._get_view_model(name)
        self._navigation_container.setCurrentWidget(view)

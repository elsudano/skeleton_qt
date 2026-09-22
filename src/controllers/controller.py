"""Global application controller."""

from PySide6.QtCore import QObject
from src.models.home_model import HomeModel
from src.models.settings_model import SettingsModel
from src.views.home_view import HomeView
from src.views.settings_view import SettingsView
from src.views.views import Views

class Controller(QObject):
    """Global application controller.

    Coordinates communication between Views and Models. Views are created
    lazily on first navigation and cached for the lifetime of the controller.
    """

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
        self._cache[name] = (view, model)
        self._connect_view(view, model)
        self._initialize_view(view, model)
        self._navigation_container.addWidget(view)
        return view, model

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

    def _connect_view(self, view, model):
        """Connect view signals to controller handlers.

        Parameters
        ----------
        view : BaseView
            View whose signals should be connected.
        model : Model
            Model associated with the view.
        """
        view.navigation_requested.connect(self.navigate)
        if isinstance(view, HomeView):
            view.welcome_requested.connect(
                lambda: view.set_message(model.get_welcome_message)
            )

    def _initialize_view(self, view, model):
        """Initialize view data from its model.

        Parameters
        ----------
        view : BaseView
            View to initialize.
        model : Model
            Model associated with the view.
        """
        if isinstance(view, SettingsView):
            view.set_title(model.get_title)

    def navigate(self, name: str):
        """Navigate to a view.

        Parameters
        ----------
        name : str
            View identifier.
        """
        view, _ = self._get_view_model(name)
        self._navigation_container.setCurrentWidget(view)

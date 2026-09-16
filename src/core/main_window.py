from PySide6.QtWidgets import QMainWindow, QStackedWidget
from src.core import config

class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self._menu_registry = {}
        self._setup_window()

    def _setup_window(self):
        """Configure the main window."""
        self.setWindowTitle(self.tr(config.WINDOW_TITLE))
        self.resize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self._navigation_container = QStackedWidget()
        self.setCentralWidget(self._navigation_container)

    def create_menus(self, menus):
        """Create and register application menus.

        Parameters
        ----------
        menus : tuple of tuple
            Menu definitions containing the internal name and translated title.
        """
        for name, title in menus:
            menu = self.menuBar().addMenu(title)
            self._menu_registry[name] = menu

    def add_action(self, menu_name: str, action):
        """Add an action to a registered menu.

        Parameters
        ----------
        menu_name : str
            Internal menu name.
        action : QAction
            Action to add.

        Raises
        ------
        KeyError
            If the menu does not exist.
        """
        self._menu_registry[menu_name].addAction(action)

    def add_separator(self, menu_name: str):
        """Add a separator to a registered menu.

        Parameters
        ----------
        menu_name : str
            Internal menu name.

        Raises
        ------
        KeyError
            If the menu does not exist.
        """
        self._menu_registry[menu_name].addSeparator()

    @property
    def navigation_container(self):
        """Return the navigation container.

        Returns
        -------
        QStackedWidget
            Navigation container.
        """
        return self._navigation_container
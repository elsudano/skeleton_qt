from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QMenu
from src.core.config import WINDOW_HEIGHT, WINDOW_WIDTH

class MainWindow(QMainWindow):
    """Main application window.

    Provides the permanent application window and the navigation container
    used to display application views, and create the window menus.
    """

    def __init__(self):
        """Initialize the main application window."""
        super().__init__()
        self._menus = {}
        self._setup_window()
        self._setup_menus()

    def _setup_window(self):
        """Configure the main window properties."""
        self.setWindowTitle(self.tr("Skeleton Qt"))
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

    def _create_menu(self, name: str, title: str) -> QMenu:
        """Create and register an application menu.

        Parameters
        ----------
        name : str
            Internal menu name.
        title : str
            Menu title displayed to the user.

        Returns
        -------
        QMenu
            Created menu.
        """
        menu = self.menuBar().addMenu(title)
        self._menus[name] = menu
        return menu

    def _setup_menus(self):
        """Create the application menu bar."""
        self._create_menu(name="file", title=self.tr("File"),)
        self._create_menu(name="views", title=self.tr("Views"),)

    def add_separator(self, menu_name: str):
        """Add a separator to an application menu.

        Parameters
        ----------
        menu_name : str
            Internal name of the target menu.
        """
        self._menus[menu_name].addSeparator()

    def add_action(self, menu_name: str, action_name: str, title: str, callback,):
        """Add a generic action to an application menu.

        Parameters
        ----------
        menu_name : str
            Internal name of the target menu.
        action_name : str
            Internal action name.
        title : str
            Action title displayed to the user.
        callback : Callable
            Function called when the action is triggered.
        """
        menu = self._menus[menu_name]
        action = QAction(title, self)
        action.setObjectName(action_name)
        action.triggered.connect(callback)
        menu.addAction(action)

    def set_central_widget(self, widget):
        """Set the central application widget.

        Parameters
        ----------
        widget : QWidget
            Widget to use as the central widget.
        """
        self.setCentralWidget(widget)
from PySide6.QtGui import QAction
from src.controllers.controller import Controller
from src.core.main_window import MainWindow
from src.views.views import Views

class Application:
    """Compose and start the application."""

    _menus = None
    _menu_actions = None

    def __init__(self, qt_application):
        """Initialize the application.

        Parameters
        ----------
        qt_application : QApplication
            Qt application instance.
        """
        self._qt_application = qt_application
        self._main_window = MainWindow()
        self._controller = Controller(self._main_window.navigation_container)
        self._menus = (
            ("file", "&File"),
            ("views", "&Views"),
        )
        
        self._menu_actions = (
            ("&Exit","file",self._qt_application.quit,),
            ("&Home","views",lambda: self._controller.navigate(Views.HOME),),
            ("&Settings","views",lambda: self._controller.navigate(Views.SETTINGS),),
        )
        self._setup_menus()
        self._controller.navigate(Views.HOME)

    def _setup_menus(self):
        """Create menus and configure their actions."""
        self._main_window.create_menus(self._menus)
        for title, menu_name, callback in self._menu_actions:
            action = QAction(self._main_window.tr(title),self._main_window,)
            action.triggered.connect(callback)
            self._main_window.add_action(menu_name, action)

    def start(self):
        """Show the application window."""
        self._main_window.show()
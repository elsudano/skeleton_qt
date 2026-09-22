"""Application composition and lifecycle."""

from PySide6.QtCore import QTranslator
from PySide6.QtGui import QAction
from src.controllers.controller import Controller
from src.core import config
from src.core.main_window import MainWindow
from src.views.views import Views

class Application:
    """Compose and start the application."""

    def __init__(self, qt_application):
        """Initialize the application.

        Parameters
        ----------
        qt_application : QApplication
            Qt application instance.
        """
        self._qt_application = qt_application
        self._translator = None
        self._language = config.DEFAULT_LANGUAGE
        self._load_translation(self._language)
        self._main_window = MainWindow()
        self._controller = Controller(
            self._main_window.navigation_container
        )
        self._setup_menus()
        self._controller.navigate(Views.HOME)

    @property
    def language(self) -> str:
        """Return the active language code (e.g. ``"es_ES"``)."""
        return self._language

    def _load_translation(self, language: str = None):
        """Load and install a translation.

        Qt notifies every widget (``LanguageChange``) so bound texts are
        re-applied automatically.

        Parameters
        ----------
        language : str, optional
            Language code to load. Falls back to ``config.DEFAULT_LANGUAGE``.
        """
        language = language or config.DEFAULT_LANGUAGE
        translation_file = config.TRANSLATIONS_DIR / f"skeleton_{language}.qm"
        translator = QTranslator()
        if not translator.load(str(translation_file)):
            return
        if self._translator is not None:
            self._qt_application.removeTranslator(self._translator)
        self._qt_application.installTranslator(translator)
        self._translator = translator
        self._language = language

    def _setup_menus(self):
        """Create menus and configure their actions.

        Menu and action titles are string literals inside ``tr()`` calls so
        that ``pyside6-lupdate`` can extract them. They are translated with
        the ``MainWindow`` context to match the existing ``.ts``/``.qm``
        files, and passed as callables so they are re-translated when the
        language changes at runtime.
        """
        menu_definitions = (
            {"name": "file",
             "title": lambda: self._main_window.tr("&File")},
            {"name": "views",
             "title": lambda: self._main_window.tr("&Views")},
            {"name": "languages",
             "title": lambda: self._main_window.tr("&Languages")},
        )

        action_definitions = (
            {"title": lambda: self._main_window.tr("&Exit"),
             "menu_name": "file",
             "callback": self._qt_application.quit},
            {"title": lambda: self._main_window.tr("&Home"),
             "menu_name": "views",
             "callback": lambda: self._controller.navigate(Views.HOME)},
            {"title": lambda: self._main_window.tr("&Settings"),
             "menu_name": "views",
             "callback": lambda: self._controller.navigate(Views.SETTINGS)},
            {"title": lambda: self._main_window.tr("&Spain"),
             "menu_name": "languages",
             "callback": lambda: self._load_translation("es_ES")},
            {"title": lambda: self._main_window.tr("&English"),
             "menu_name": "languages",
             "callback": lambda: self._load_translation("en_US")},
        )

        for menu in menu_definitions:
            self._main_window.create_menu(menu["name"], menu["title"])

        for menu_action in action_definitions:
            action = QAction(menu_action["title"](), self._main_window)
            action.triggered.connect(menu_action["callback"])
            self._main_window.add_action(
                menu_action["menu_name"], action, menu_action["title"]
            )

    def start(self):
        """Show the application window."""
        self._main_window.show()

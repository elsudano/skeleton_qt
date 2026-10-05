"""Application composition, configuration, and startup."""

from PySide6.QtCore import QLoggingCategory, QObject, QTranslator, qCInfo, qCDebug
from PySide6.QtGui import QAction, QActionGroup

from src.controllers.controller import Controller
from src.core import config
from src.core.logging import LoggingManager
from src.core.main_window import MainWindow
from src.views.views import Views


class Application(QObject):
    """Compose and start the Qt application."""

    # We need to declare this in this way just to handle the known issue: use-after-free
    # in python, in this case PySide6 when you create a category, PySide6 is creating a buffer
    # and this buffet pointing a different memory directions, for that reason fail.
    _CATEGORY = "skeleton.core.application"
    _log = QLoggingCategory(_CATEGORY)

    def __init__(self, qt_application):
        """Initialize the application.

        Parameters
        ----------
        qt_application : QApplication
            Qt application instance used by the application.
        """
        super().__init__()
        self._qt_application = qt_application
        self._translator = None
        self._language = config.DEFAULT_LANGUAGE
        self._theme = config.DEFAULT_THEME
        self._apply_theme(self._theme)
        self._logging_manager = LoggingManager()
        self._qt_application.aboutToQuit.connect(self._logging_manager.close)
        self._main_window = MainWindow()
        self._controller = Controller(
            self._main_window.navigation_container,
            self._logging_manager,
        )
        self._load_translation(self._language)
        self._setup_menus()
        self._controller.navigate(Views.HOME)
        qCInfo(self._log, f"Application initialized")
        qCDebug(self._log, f"Application initialized")

    @property
    def theme(self) -> str:
        """Return the currently active theme.

        Returns
        -------
        str
            Active theme identifier.
        """
        return self._theme

    def set_theme(self, theme: str):
        """Apply a theme to the entire Qt application.

        Parameters
        ----------
        theme : str
            Theme identifier, either ``"light"`` or ``"dark"``.

        Raises
        ------
        ValueError
            If the theme identifier is not supported.
        FileNotFoundError
            If the selected theme stylesheet cannot be found.
        """
        self._apply_theme(theme)
        if hasattr(self, "_theme_actions"):
            self._theme_actions[theme].setChecked(True)

    def _apply_theme(self, theme: str):
        """Load and apply a theme stylesheet globally.

        Parameters
        ----------
        theme : str
            Theme identifier, either ``"light"`` or ``"dark"``.

        Raises
        ------
        ValueError
            If the theme identifier is not supported.
        FileNotFoundError
            If the selected theme stylesheet cannot be found.
        """
        if theme not in ("light", "dark"):
            raise ValueError(f"Unsupported application theme: {theme}")

        stylesheet_path = config.STYLES_DIR / f"{theme}.qss"
        stylesheet = stylesheet_path.read_text(encoding="utf-8")
        self._qt_application.setStyleSheet(stylesheet)
        self._theme = theme
        qCDebug(self._log, f"Application theme applied: {theme}")

    @property
    def language(self) -> str:
        """Return the active language code.

        Returns
        -------
        str
            Active language code.
        """
        return self._language

    def _load_translation(self, language: str = None):
        """Load and install a translation.

        Parameters
        ----------
        language : str
            Language code used to locate the translation source.
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
        qCDebug(self._log, self.tr("The Language was changed"))

    def _setup_menus(self):
        """Create application menus and actions."""
        menu_definitions = (
            ("file", lambda: self.tr("&File")),
            ("edit", lambda: self.tr("&Edit")),
            ("tools", lambda: self.tr("&Tools")),
            ("options", lambda: self.tr("&Options")),
            ("help", lambda: self.tr("&Help")),
        )
        for name, title in menu_definitions:
            self._main_window.create_menu(name, title)

        action_definitions = (
            ("home", lambda: self.tr("&Home"), "file",
             lambda: self._controller.navigate(Views.HOME)),
            ("separator", None, "file", None),
            ("exit", lambda: self.tr("E&xit"), "file", self._qt_application.quit),
            ("cut", lambda: self.tr("Cu&t"), "edit", lambda: None),
            ("copy", lambda: self.tr("&Copy"), "edit", lambda: None),
            ("paste", lambda: self.tr("&Paste"), "edit", lambda: None),
            ("video", lambda: self.tr("&Video Uploader"), "tools",
             lambda: self._controller.navigate(Views.VIDEO_UPLOADER)),
            ("route", lambda: self.tr("&Route Designer"), "tools",
             lambda: self._controller.navigate(Views.ROUTE_DESIGNER)),
            ("logs", lambda: self.tr("&Logs"), "tools",
             lambda: self._controller.navigate(Views.LOGS)),
            ("language_header", lambda: self.tr("Language:"), "options", None),
            ("es_ES", lambda: self.tr("&Spanish"), "options",
             lambda: self._load_translation("es_ES")),
            ("en_US", lambda: self.tr("&English"), "options",
             lambda: self._load_translation("en_US")),
            ("separator", None, "options", None),
            ("themes_header", lambda: self.tr("Theme:"), "options", None),
            ("light", lambda: self.tr("&Light"), "options",
             lambda checked=False: self.set_theme("light")),
            ("dark", lambda: self.tr("&Dark"), "options",
             lambda checked=False: self.set_theme("dark")),
            ("separator", None, "options", None),
            ("settings", lambda: self.tr("Set&tings"), "options",
             lambda: self._controller.navigate(Views.SETTINGS)),
            ("about", lambda: self.tr("&About"), "help",
             lambda: self._controller.navigate(Views.HOME)),
        )
        language_group = QActionGroup(self._main_window)
        language_group.setExclusive(True)
        self._language_actions = {}
        theme_group = QActionGroup(self._main_window)
        theme_group.setExclusive(True)
        self._theme_actions = {}

        for id, title_source, menu_name, callback in action_definitions:
            if id == "separator":
                self._main_window.add_separator(menu_name)
            elif id == "language_header":
                self._main_window.add_header(menu_name, title_source)
            elif id in ("es_ES", "en_US"):
                action = QAction(title_source(), self._main_window)
                action.setCheckable(True)
                action.setChecked(id == self._language)
                action.triggered.connect(callback)
                language_group.addAction(action)
                self._main_window.add_action(menu_name, action, title_source)
                self._language_actions[id] = action
            elif id == "themes_header":
                self._main_window.add_header(menu_name, title_source)
            elif id in ("light", "dark"):
                action = QAction(title_source(), self._main_window)
                action.setCheckable(True)
                action.setChecked(id == self._theme)
                action.triggered.connect(callback)
                theme_group.addAction(action)
                self._main_window.add_action(menu_name, action, title_source)
                self._theme_actions[id] = action
            else:
                action = QAction(title_source(), self._main_window)
                action.triggered.connect(callback)
                self._main_window.add_action(menu_name, action, title_source)
        qCDebug(self._log, self.tr("We have configured all the menus and the actions"))

    def start(self):
        """Show the application window and start the application lifecycle."""
        self._main_window.show()

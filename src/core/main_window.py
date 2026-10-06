"""Main application window and menu infrastructure."""

from PySide6.QtCore import QEvent, QLoggingCategory, qCDebug, qCInfo
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel, QMainWindow, QStackedWidget, QWidgetAction

from src.core import config
from src.core.text_binder import TextBinder


class MainWindow(QMainWindow):
    """Provide the main application window, menus, and navigation container."""

    # We need to declare this in this way just to handle the known issue: use-after-free
    # in python, in this case PySide6 when you create a category, PySide6 is creating a buffer
    # and this buffet pointing a different memory directions, for that reason fail.
    _CATEGORY = "skeleton.main_window"
    _log = QLoggingCategory(_CATEGORY)

    def __init__(self):
        """Initialize the main window.

        Parameters
        ----------
        parent : QWidget, optional
            Parent widget for the main window."""
        super().__init__()
        self._menu_registry = {}
        self._navigation_container = QStackedWidget()
        self._texts = TextBinder()
        self._setup_window()
        qCInfo(self._log, "The class MainWindow was created")
        qCDebug(self._log, "The class MainWindow was created")

    def _setup_window(self):
        """Configure the main window."""
        self.bind_text(self, lambda: self.tr("Skeleton Qt"), self.setWindowTitle)
        self.setWindowIcon(QIcon(str(config.ASSETS_DIR / "icon.ico")))
        self.resize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.setCentralWidget(self._navigation_container)
        qCDebug(self._log, "We have configured the MainWindow")

    def bind_text(self, widget, source, setter=None):
        """Bind a translatable text source to a widget setter.

        This method intentionally mirrors :meth:`BaseView.bind_text`.
        Both classes maintain their own :class:`TextBinder` instance because
        they manage independent UI scopes.

        Parameters
        ----------
        widget : QObject
            Widget that displays the text.
        source : callable or str
            Callable returning the text or a plain string applied as-is.
        setter : callable, optional
            Callable that receives the text. If omitted, ``widget.setText`` is used.

        Returns
        -------
        QObject
            The same widget, so it can be created and bound in one line."""
        qCDebug(self._log, f"We have translated {source()}")
        return self._texts.bind(widget, source, setter)

    def create_menu(self, name: str, title_source):
        """Create and register an application menu.

        Parameters
        ----------
        name : str
            Internal menu name used by :meth:`add_action`.
        title_source : callable or str
            Callable returning the menu title or a plain string applied as-is."""
        menu = self.menuBar().addMenu("")
        self._menu_registry[name] = menu
        self.bind_text(menu, title_source, menu.setTitle)
        qCDebug(self._log, f"We have created the {title_source()} menu.")

    def add_action(self, menu_name: str, action, text_source=None):
        """Add an action to a registered menu.

        Parameters
        ----------
        menu_name : str
            Internal menu name.
        action : QAction
            Action to add.
        text_source : callable or str, optional
            Callable returning the action text or a plain string applied as-is.

        Raises
        ------
        KeyError
            If the menu does not exist."""
        self._menu_registry[menu_name].addAction(action)
        if text_source is not None:
            self.bind_text(action, text_source)
        qCDebug(self._log, f"We have created the {text_source()} item in {menu_name} menu.")

    def add_header(self, menu_name: str, text_source=None):
        """Add a title header to a registered menu.

        Parameters
        ----------
        menu_name : str
            Internal menu name used by the menu registry.
        text_source : callable or str, optional
            Callable returning the header text or a plain string applied as-is.

        Raises
        ------
        KeyError
            If the menu does not exist.
        """
        label_header = QLabel("", self)
        font = label_header.font()
        font.setBold(True)
        label_header.setFont(font)
        label_header.setObjectName("menuSectionHeader")
        action = QWidgetAction(self)
        action.setDefaultWidget(label_header)
        self._menu_registry[menu_name].addAction(action)
        if text_source is not None:
            self.bind_text(label_header, text_source, label_header.setText)
        qCDebug(self._log, f"We have created the {text_source()} header in {menu_name} menu.")

    def add_separator(self, menu_name: str):
        """Add a separator to a registered menu.

        Parameters
        ----------
        menu_name : str
            Internal menu name.

        Raises
        ------
        KeyError
            If the menu does not exist."""
        self._menu_registry[menu_name].addSeparator()
        qCDebug(self._log, f"We have added a separator in {menu_name} menu.")

    @property
    def navigation_container(self) -> QStackedWidget:
        """Return the navigation container.

        Returns
        -------
        QStackedWidget
            Main stacked widget used to display application views."""
        return self._navigation_container

    def changeEvent(self, event):
        """Re-apply bound texts when Qt reports a language change.

        Parameters
        ----------
        event : QEvent
            Change event sent by Qt."""
        if event.type() == QEvent.Type.LanguageChange:
            self._texts.refresh()
        super().changeEvent(event)

from PySide6.QtWidgets import QStackedWidget, QWidget

class Navigation:
    """Manage application view navigation."""

    def __init__(self):
        """Initialize the navigation manager."""
        self._stacked_widget = QStackedWidget()
        self._views = {}

    def add_view(self, name: str, view: QWidget):
        """Add a view to the navigation system.

        Parameters
        ----------
        name : str
            Unique name identifying the view.
        view : QWidget
            View to add to the navigation system.

        Raises
        ------
        ValueError
            If the view name is already registered.
        """
        if name in self._views:
            raise ValueError(
                f"View '{name}' is already registered."
            )

        self._views[name] = view
        self._stacked_widget.addWidget(view)

    def has_view(self, name: str) -> bool:
        """Return whether a view is already added.

        Parameters
        ----------
        name : str
            View name.

        Returns
        -------
        bool
            True if the view is already added.
        """
        return name in self._views

    def show_view(self, name: str):
        """Display a view by its name.

        Parameters
        ----------
        name : str
            Name of the view to display.

        Raises
        ------
        KeyError
            If the requested view does not exist.
        """
        if name not in self._views:
            raise KeyError(
                f"View '{name}' is not registered."
            )

        self._stacked_widget.setCurrentWidget(self._views[name])

    def widget(self) -> QStackedWidget:
        """Return the navigation widget.

        Returns
        -------
        QStackedWidget
            Navigation container widget.
        """
        return self._stacked_widget
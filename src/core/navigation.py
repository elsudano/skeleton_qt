from PySide6.QtWidgets import QStackedWidget, QWidget

class Navigation:
    """Manage application view navigation."""

    def __init__(self):
        """Initialize the navigation manager."""
        self._stacked_widget = QStackedWidget()
        self._views = {}

    def add_view(self, name, view):
        """Add a view to the navigation system.

        Parameters
        ----------
        name : str
            Unique name identifying the view.
        view : QWidget
            View to add to the navigation system.
        """
        self._views[name] = view
        self._stacked_widget.addWidget(view)

    def show_view(self, name):
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
        view = self._views[name]
        self._stacked_widget.setCurrentWidget(view)

    def widget(self):
        """Return the widget used by the navigation system.

        Returns
        -------
        QStackedWidget
            Navigation container widget.
        """
        return self._stacked_widget
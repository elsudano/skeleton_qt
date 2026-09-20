class TextBinder:
    """Keep widget texts in sync with the active language.

    Each text is registered once, next to the widget that shows it. Its source
    is a callable returning the text, so it can be evaluated again whenever the
    language changes. Widgets that are not bound (user input, table contents...)
    are never touched.
    """

    def __init__(self):
        """Initialize an empty binder."""
        self._bindings = {}

    def bind(self, widget, source, setter: str = "setText"):
        """Show a text now and remember how to obtain it again.

        Binding the same widget and setter again replaces the previous source.

        Parameters
        ----------
        widget : QObject
            Widget, action or window that displays the text.
        source : callable or str
            Callable returning the text (``lambda: self.tr("Back")`` or a model
            getter). A plain ``str`` is applied as-is and never re-translated.
        setter : str, optional
            Name of the widget method that receives the text.

        Returns
        -------
        QObject
            The same widget, so it can be created and bound in one line.
        """
        self._bindings[(widget, setter)] = source
        getattr(widget, setter)(self._text_of(source))
        return widget

    def refresh(self):
        """Apply again every bound text (call it when the language changes)."""
        for key, source in list(self._bindings.items()):
            widget, setter = key
            text = self._text_of(source)
            try:
                getattr(widget, setter)(text)
            except RuntimeError:
                del self._bindings[key]

    @staticmethod
    def _text_of(source) -> str:
        """Return the text produced by a source."""
        return source() if callable(source) else source

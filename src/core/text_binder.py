"""Utility for keeping widget text synchronized with the active language."""


class TextBinder:
    """Keep widget texts in sync with the active language."""

    def __init__(self):
        """Initialize an empty binder."""
        self._bindings = {}

    def bind(self, widget, source, setter=None):
        """Show a text now and remember how to obtain it again.

        Binding the same widget and setter again replaces the previous source.

        Parameters
        ----------
        widget : QObject
            Widget, action, or window that displays the text.
        source : callable or str
            Callable returning the text or a plain string applied as-is.
        setter : callable, optional
            Callable that receives the text. If omitted, ``widget.setText`` is used.

        Returns
        -------
        QObject
            The same widget, so it can be created and bound in one line."""
        setter = setter or widget.setText
        self._bindings[(widget, setter)] = source
        setter(self._text_of(source))
        return widget

    def refresh(self):
        """Apply again every bound text."""
        for key, source in list(self._bindings.items()):
            widget, setter = key
            text = self._text_of(source)
            try:
                setter(text)
            except RuntimeError:
                del self._bindings[key]

    @staticmethod
    def _text_of(source) -> str:
        """Return the text produced by a source.

        Parameters
        ----------
        source : callable or str
            Callable returning the current text or a plain string.

        Returns
        -------
        str
            Text produced by the source."""
        return source() if callable(source) else source

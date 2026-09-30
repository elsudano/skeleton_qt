# src/views/checkable_combo_box.py
"""Collapsible dropdown widget that allows selecting more than one entry."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QComboBox


class CheckableComboBox(QComboBox):
    """Provide a collapsible dropdown whose entries can be checked individually.

    A plain ``QComboBox`` only allows a single selection and closes its
    popup on every click. This widget keeps the popup open while the user
    checks or unchecks entries, and shows the checked entries, joined by
    commas, as the collapsed text."""

    selection_changed = Signal()

    def __init__(self, parent=None):
        """Initialize the checkable combo box.

        Parameters
        ----------
        parent : QWidget, optional
            Parent widget for the combo box."""
        super().__init__(parent)
        self.setModel(QStandardItemModel(self))
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        # We intercept the press on the popup's view instead of relying on
        # the combo box's normal selection mechanism: entries below are
        # created without ItemIsSelectable, so a click never becomes a
        # "selection" and Qt never auto-closes the popup for us.
        self.view().pressed.connect(self._toggle_item)

    def add_item(self, text: str, checked: bool = False):
        """Add a checkable entry to the dropdown.

        Parameters
        ----------
        text : str
            Text of the entry.
        checked : bool, optional
            Initial checked state of the entry."""
        item = QStandardItem(text)
        item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
        item.setData(
            Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked,
            Qt.ItemDataRole.CheckStateRole,
        )
        self.model().appendRow(item)
        self._refresh_display_text()

    def checked_items(self) -> set[str]:
        """Return the text of every currently checked entry.

        Returns
        -------
        set[str]
            Checked entry texts."""
        model = self.model()
        return {
            model.item(row).text()
            for row in range(model.rowCount())
            if model.item(row).checkState() == Qt.CheckState.Checked
        }

    def _toggle_item(self, index):
        """Toggle the checked state of the entry under the press.

        Parameters
        ----------
        index : QModelIndex
            Index of the pressed entry."""
        item = self.model().itemFromIndex(index)
        item.setCheckState(
            Qt.CheckState.Unchecked
            if item.checkState() == Qt.CheckState.Checked
            else Qt.CheckState.Checked
        )
        self._refresh_display_text()
        self.selection_changed.emit()

    def _refresh_display_text(self):
        """Show the checked entries as the collapsed text of the combo box."""
        self.lineEdit().setText(", ".join(sorted(self.checked_items())))
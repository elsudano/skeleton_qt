"""Model for the Route Designer view."""

from PySide6.QtCore import QLoggingCategory

from src.models.model import Model


class RouteDesigner_Model(Model):
    """Provide application data and behavior used by the Route Designer view."""

    # We need to declare this in this way just to handle the known issue: use-after-free
    # in python, in this case PySide6 when you create a category, PySide6 is creating a buffer
    # and this buffet pointing a different memory directions, for that reason fail.
    _CATEGORY = "skeleton.model.route_designer"
    _log = QLoggingCategory(_CATEGORY)
from src.controllers.settings_controller import SettingsController
from src.models.settings_model import SettingsModel
from src.views.settings_view import SettingsView
from src.core.feature_registry import FeatureInstance


def create_settings() -> FeatureInstance:
    """Create the settings feature components.

    Returns
    -------
    FeatureInstance
        Settings model, view and controller.
    """
    model = SettingsModel()
    view = SettingsView()
    controller = SettingsController(view=view,model=model,)
    return FeatureInstance(model=model, view=view, controller=controller,)
from src.controllers.home_controller import HomeController
from src.models.home_model import HomeModel
from src.views.home_view import HomeView
from src.core.feature_registry import FeatureInstance


def create_home() -> FeatureInstance:
    """Create the home feature components.

    Returns
    -------
    FeatureInstance
        Home model, view and controller.
    """
    model = HomeModel()
    view = HomeView()
    controller = HomeController(view=view,model=model,)
    return FeatureInstance(model=model, view=view, controller=controller,)
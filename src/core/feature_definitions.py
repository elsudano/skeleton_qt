from dataclasses import dataclass
from typing import Callable
from src.core.routes import Routes
from src.features.home import create_home
from src.features.settings import create_settings


@dataclass(frozen=True)
class FeatureDefinition:
    """Define a feature available in the application."""

    name: str
    factory: Callable


FEATURES = (
    FeatureDefinition(
        name=Routes.HOME,
        factory=create_home,
    ),
    FeatureDefinition(
        name=Routes.SETTINGS,
        factory=create_settings,
    ),
)
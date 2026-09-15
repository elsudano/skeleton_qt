from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class FeatureInstance:
    """Store the components belonging to a feature."""

    model: Any
    view: Any
    controller: Any
    navigation_connected: bool = False


class FeatureRegistry:
    """Register and lazily create application features."""

    def __init__(self):
        """Initialize the feature registry."""
        self._factories = {}
        self._instances = {}

    def register(self, name: str, factory: Callable):
        """Register a feature factory.

        Parameters
        ----------
        name : str
            Unique feature name.
        factory : Callable
            Callable that creates the feature components.

        Raises
        ------
        ValueError
            If the feature name is already registered.
        """
        if name in self._factories:
            raise ValueError(
                f"Feature '{name}' is already registered."
            )

        self._factories[name] = factory

    def get(self, name: str) -> FeatureInstance:
        """Return a feature instance, creating it when necessary.

        Parameters
        ----------
        name : str
            Name of the requested feature.

        Returns
        -------
        FeatureInstance
            Feature components.

        Raises
        ------
        KeyError
            If the feature is not registered.
        """
        if name not in self._factories:
            raise KeyError(
                f"Feature '{name}' is not registered."
            )

        if name not in self._instances:
            self._instances[name] = self._factories[name]()

        return self._instances[name]

    def contains(self, name: str) -> bool:
        """Return whether a feature is registered.

        Parameters
        ----------
        name : str
            Feature name.

        Returns
        -------
        bool
            True if the feature is registered.
        """
        return name in self._factories
from abc import ABC

class Model(ABC):
    """Base class for application models.

    Provides the common base for models that contain application logic.
    """
    def __init__(self):
        """Initialize the model."""
        super().__init__()
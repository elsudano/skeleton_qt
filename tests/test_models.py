from src.models.home_model import HomeModel
from src.models.settings_model import SettingsModel


def test_home_model_returns_welcome_message(qapp):
    assert HomeModel().get_welcome_message() == "Welcome to Skeleton Qt"


def test_settings_model_returns_title(qapp):
    assert SettingsModel().get_title() == "Settings"

from include.classes.config import AppConfig

__all__ = ["BaseController"]


class BaseController:
    def __init__(self, control, *args, **kwargs) -> None:
        self.control = control
        self.app_config = AppConfig()

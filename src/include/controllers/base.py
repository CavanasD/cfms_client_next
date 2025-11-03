from typing import Generic
from typing import TypeVar
from include.classes.config import AppConfig

T = TypeVar('T')

__all__ = ["BaseController"]


class BaseController(Generic[T]):
    def __init__(self, control: T, *args, **kwargs) -> None:
        self.control = control
        self.app_config = AppConfig()

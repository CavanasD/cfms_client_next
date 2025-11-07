from typing import Optional, Any
import os
import threading

from flet_permission_handler import PermissionHandler
import yaml

from websockets.asyncio.client import ClientConnection
from include.constants import FLET_APP_STORAGE_DATA

PREFERENCES_PATH = f"{FLET_APP_STORAGE_DATA}/preferences.yaml"

__all__ = ["AppConfig"]


class AppConfig(object):
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(
        self,
    ):
        if getattr(self, "_initialized", False):
            return

        self.server_address: Optional[str] = None
        self.server_info: dict[str, Any] = {}
        self.disable_ssl_enforcement: bool = False
        self.username: Optional[str] = None
        self.token: Optional[str] = None
        self.token_exp: Optional[float] = None
        self.nickname: Optional[str] = None
        self.user_permissions: list[str] = []
        self.user_groups: list[str] = []
        self.conn: Optional[ClientConnection] = None
        self.ph_service: Optional[PermissionHandler] = None

        if not os.path.exists(PREFERENCES_PATH):
            self.init_preferences()

        with open(PREFERENCES_PATH, "r", encoding="utf-8") as file:
            self.preferences = yaml.safe_load(file)

        self._initialized = True

    def get_not_none_attribute(self, name):
        _attr = getattr(self, name)
        assert _attr is not None
        return _attr

    def init_preferences(self):
        doc = {
            "settings": {
                "language": "zh_CN",  # Default to Chinese
                "proxy_settings": None,
                "custom_proxy": "",
                "enable_conn_history_logging": False,
            }
        }

        with open(PREFERENCES_PATH, "w", encoding="utf-8") as f:
            yaml.safe_dump(doc, f)

    def dump_preferences(self):
        with open(PREFERENCES_PATH, "w", encoding="utf-8") as f:
            yaml.safe_dump(self.preferences, f)

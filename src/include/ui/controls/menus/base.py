from typing import Any

import flet as ft

from include.classes.config import AppConfig
from include.ui.controls.dialogs.base import AlertDialog

__all__ = ["RightMenuDialog"]


class RightMenuDialog(AlertDialog):
    def __init__(
        self,
        title: str | ft.Control | None = None,
        menu_items: list[dict[str, Any]] = [],
        modal: bool = False,
        ref: ft.Ref | None = None,
        visible: bool = True,
    ):
        # Validate menu_items structure
        required_keys = ["icon", "title", "subtitle", "on_click"]
        for item in menu_items:
            if not isinstance(item, dict) or not all(
                key in item for key in required_keys
            ):
                raise ValueError(
                    "Each item in menu_items must be a dict with keys: "
                    "'icon', 'title', 'subtitle', 'on_click'"
                )
            if not callable(item["on_click"]):
                raise ValueError("'on_click' must be callable")

        super().__init__(
            title=title, modal=modal, scrollable=True, ref=ref, visible=visible
        )
        self.app_config = AppConfig()
        # Create menu listview directly with ListTiles
        controls = []
        for item in menu_items:
            item_require = set(item.get("require", {}))
            if (item_require & set(self.app_config.user_permissions)) != item_require:
                continue

            item_icon = item["icon"]
            item_title = item["title"]
            item_subtitle = item["subtitle"]
            item_on_click = item["on_click"]
            item_ref = item.get("ref")  # Optional ref

            controls.append(
                ft.ListTile(
                    leading=item_icon,
                    title=item_title,
                    subtitle=item_subtitle,
                    on_click=item_on_click,
                    ref=item_ref,
                )
            )

        self.menu_listview = ft.ListView(
            controls=controls,
        )
        self.content = ft.Container(self.menu_listview, width=480)

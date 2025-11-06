from typing import Any, Type

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


class ContentMenu2(ft.ContextMenu):
    """
    A context menu that displays a list of menu items with icons, titles, subtitles, and click handlers.
    Each menu item is represented as a dictionary with the following structure:

    ```python
    {
        "primary_items": [
            {
                "icon": ft.Icon,
                "content": str | ft.Control,
                "on_click": ControlEventHandler[PopupMenuItem] | None,
                "ref": ft.Ref | None
            },
            {},  # divider
            ...
        ]
    }
    ```
    """

    def __init__(
        self,
        content: ft.Control,
        menu_items: list[dict[str, Any]] = [],
        ref: ft.Ref | None = None,
    ):
        self.app_config = AppConfig()

        # Validate menu_items structure
        required_keys = ["icon", "content", "on_click"]

        controls = []
        for item in menu_items:
            if not isinstance(item, dict):
                raise TypeError("Each item in menu_items must be a dict")

            if item == {}:
                controls.append(ft.PopupMenuItem())
                continue
            elif not all(key in item for key in required_keys):
                raise ValueError(
                    "Each item in menu_items must be a dict with keys: "
                    "'icon', 'content', 'on_click'"
                )

            item_require = set(item.get("require", {}))
            if (item_require & set(self.app_config.user_permissions)) != item_require:
                continue

            item_icon = item["icon"]
            item_content = item["content"]
            item_on_click = item.get("on_click")
            item_ref = item.get("ref")  # Optional ref

            if item_on_click is not None and not callable(item_on_click):
                raise ValueError("'on_click' must be callable")

            controls.append(
                ft.PopupMenuItem(
                    icon=item_icon,
                    content=item_content,
                    on_click=item_on_click,
                    ref=item_ref,
                )
            )

        self.gesture_detector = ft.GestureDetector(
            on_long_press_start=self.trigger_open_menu,
            on_secondary_tap_down=self.trigger_open_menu,  # pending github:flet-dev/flet/#5784
            content=content,
        )
        super().__init__(content=self.gesture_detector, items=controls, ref=ref)

    async def trigger_open_menu(
        self,
        event: (
            ft.TapEvent[ft.GestureDetector] | ft.LongPressStartEvent[ft.GestureDetector]
        ),
    ):
        await self.open(
            local_position=event.local_position,
            global_position=event.global_position,
        )

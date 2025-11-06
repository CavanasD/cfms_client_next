from datetime import datetime
from typing import TYPE_CHECKING

import flet as ft

from include.classes.config import AppConfig
from include.controllers.explorer.tile import (
    FileContextMenuController,
    DirectoryContextMenuController
)

from include.ui.controls.menus.base import ContentMenu2
from include.util.locale import get_translation

if TYPE_CHECKING:
    from include.ui.controls.views.explorer import FileListView

t = get_translation()
_ = t.gettext


class FileContextMenu(ContentMenu2):
    def __init__(
        self,
        file_id: str,
        filename: str,
        size: int,
        last_modified: float,
        parent_listview: "FileListView",
        ref: ft.Ref | None = None,
    ):
        self.page: ft.Page
        self.file_id = file_id
        self.filename = filename
        self.size = size
        self.last_modified = last_modified
        self.parent_listview = parent_listview

        self.app_config = AppConfig()

        # Instantiate ListTile
        self._listtile = ft.ListTile(
            leading=ft.Icon(ft.Icons.FILE_COPY),
            title=filename,
            subtitle=ft.Text(
                _("Last modified: {last_modified}\n").format(
                    last_modified=datetime.fromtimestamp(last_modified).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )
                + (f"{size / 1024 / 1024:.3f} MB" if size > 0 else "0 Byte")
            ),
            is_three_line=True,
            on_click=self.listtile_click,
        )

        self.controller = FileContextMenuController(self)

        super().__init__(
            self._listtile,
            ref=ref,
            menu_items=[
                {
                    "icon": ft.Icons.DELETE,
                    "content": _("Delete"),
                    "on_click": self.delete_button_click,
                },
                {
                    "icon": ft.Icons.DRIVE_FILE_RENAME_OUTLINE_OUTLINED,
                    "content": _("Rename"),
                    "on_click": self.rename_button_click,
                },
                {
                    "icon": ft.Icons.SETTINGS_OUTLINED,
                    "content": _("Set Permissions"),
                    "on_click": self.set_access_rules_button_click,
                    "require": {"set_access_rules"},
                },
                {
                    "icon": ft.Icons.INFO_OUTLINED,
                    "content": _("Properties"),
                    "on_click": self.open_document_info_click,
                },
            ],
        )

    async def listtile_click(self, event: ft.Event[ft.ListTile]):
        self.page.run_task(self.controller.action_open_file)

    async def delete_button_click(self, event: ft.Event[ft.ListTile]):
        self.page.run_task(self.controller.action_delete_file)

    async def rename_button_click(self, event: ft.Event[ft.ListTile]):
        self.page.run_task(self.controller.action_rename_file)

    async def set_access_rules_button_click(self, event: ft.Event[ft.ListTile]):
        self.page.run_task(self.controller.action_set_access_rules)

    async def open_document_info_click(self, event: ft.Event[ft.ListTile]):
        self.page.run_task(self.controller.action_open_document_info)


class DirectoryContextMenu(ContentMenu2):
    def __init__(
        self,
        parent_listview: "FileListView",
        directory_id: str,
        dir_name: str,
        created_at: float,
        ref: ft.Ref | None = None,
    ):

        self.page: ft.Page
        self.parent_listview = parent_listview
        self.controller = DirectoryContextMenuController(self)

        self.directory_id = directory_id
        self.dir_name = dir_name
        self.created_at = created_at

        # Instantiate ListTile
        self._listtile = ft.ListTile(
            leading=ft.Icon(ft.Icons.FOLDER),
            title=dir_name,
            subtitle=ft.Text(
                _("Created time: {created_time}").format(
                    created_time=datetime.fromtimestamp(self.created_at).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )
            ),
            on_click=self.listtile_click,
        )

        super().__init__(
            content=self._listtile,
            menu_items=[
                {
                    "icon": ft.Icons.DELETE,
                    "content": _("Delete"),
                    "on_click": self.delete_button_click,
                },
                {
                    "icon": ft.Icons.DRIVE_FILE_RENAME_OUTLINE_OUTLINED,
                    "content": _("Rename"),
                    "on_click": self.rename_button_click,
                },
                {
                    "icon": ft.Icons.LOCK_PERSON_OUTLINED,
                    "content": _("Grant Access"),
                    "on_click": None,
                },
                {
                    "icon": ft.Icons.SETTINGS_OUTLINED,
                    "content": _("Set Permissions"),
                    "on_click": self.set_access_rules_button_click,
                    "require": {"set_access_rules"},
                },
                {
                    "icon": ft.Icons.INFO_OUTLINED,
                    "content": _("Properties"),
                    "on_click": self.open_directory_info_click,
                },
            ],
            ref=ref,
        )

    async def listtile_click(self, event: ft.Event[ft.ListTile]):
        self.page.run_task(self.controller.action_open_directory)

    async def delete_button_click(self, event: ft.Event[ft.ListTile]):
        self.page.run_task(self.controller.action_delete_directory)

    async def rename_button_click(self, event: ft.Event[ft.ListTile]):
        self.page.run_task(self.controller.action_rename_directory)

    async def set_access_rules_button_click(self, event: ft.Event[ft.ListTile]):
        self.page.run_task(self.controller.action_set_access_rules)

    async def open_directory_info_click(self, event: ft.Event[ft.ListTile]):
        self.page.run_task(self.controller.action_open_directory_info)
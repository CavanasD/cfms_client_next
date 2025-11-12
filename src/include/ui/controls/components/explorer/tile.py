from datetime import datetime
from typing import TYPE_CHECKING

import flet as ft

from include.classes.config import AppConfig
from include.controllers.explorer.tile import (
    DirectoryGestureListTileController,
    FileContextMenuController,
    FileGestureListTileController,
)

from include.ui.controls.menus.base import ContextMenu2
from include.util.locale import get_translation

if TYPE_CHECKING:
    from include.ui.controls.views.explorer import FileListView

t = get_translation()
_ = t.gettext


class FileGestureListTile(ft.GestureDetector):
    def __init__(
        self,
        parent_listview: "FileListView",
        file_id: str,
        filename: str,
        size: int,
        last_modified: float,
        ref: ft.Ref | None = None,
    ):
        super().__init__(
            on_secondary_tap=self.gesturedetector_secondary_tap,
            on_long_press_start=self.gesturedetector_long_press_start,
            ref=ref,
        )
        self.page: ft.Page
        self.parent_listview = parent_listview
        self.controller = FileGestureListTileController(self)

        self.file_id = file_id
        self.filename = filename
        self.size = size
        self.last_modified = last_modified

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

        self.content = self._listtile

    async def listtile_click(self, event: ft.Event[ft.ListTile]):
        self.page.run_task(self.controller.action_open_file)

    async def gesturedetector_secondary_tap(self, event: ft.Event[ft.GestureDetector]):
        self.page.run_task(self.controller.action_open_context_menu)

    async def gesturedetector_long_press_start(
        self, event: ft.Event[ft.GestureDetector]
    ):
        self.page.run_task(self.controller.action_open_context_menu)


class DirectoryGestureListTile(ft.GestureDetector):
    def __init__(
        self,
        parent_listview: "FileListView",
        directory_id: str,
        dir_name: str,
        created_at: float,
        ref: ft.Ref | None = None,
    ):
        super().__init__(
            on_secondary_tap=self.gesturedetector_secondary_tap,
            on_long_press_start=self.gesturedetector_long_press_start,
            ref=ref,
        )
        self.page: ft.Page
        self.parent_listview = parent_listview
        self.controller = DirectoryGestureListTileController(self)

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

        self.content = self._listtile

    async def listtile_click(self, event: ft.Event[ft.ListTile]):
        self.page.run_task(self.controller.action_open_directory)

    async def gesturedetector_secondary_tap(self, event: ft.Event[ft.GestureDetector]):
        self.page.run_task(self.controller.action_open_context_menu)

    async def gesturedetector_long_press_start(
        self, event: ft.Event[ft.GestureDetector]
    ):
        self.page.run_task(self.controller.action_open_context_menu)

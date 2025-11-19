from typing import TYPE_CHECKING

import flet as ft

from include.ui.controls.contextmenus.explorer import DirectoryContextMenu, FileContextMenu
from include.ui.util.path import get_directory

from include.util.locale import get_translation

t = get_translation()
_ = t.gettext

if TYPE_CHECKING:
    from include.ui.controls.views.explorer import FileListView

# __all__ = ["get_directory"]


def update_file_controls(
    view: "FileListView",
    folders: list[dict],
    documents: list[dict],
    parent_id: str | None = None,
):
    view.controls = []  # reset

    async def parent_button_click(event: ft.Event[ft.ListTile]):
        view.parent_manager.indicator.back()
        view.parent_manager.current_directory_id = (
            None if parent_id == "/" else parent_id
        )
        await get_directory(view.parent_manager.current_directory_id, view=view)

    if (
        parent_id != None
        and view.parent_manager.current_directory_id
        != view.parent_manager.root_directory_id
    ):
        # print("parent_id: ", parent_id)
        view.controls = [
            ft.ListTile(
                leading=ft.Icon(ft.Icons.ARROW_BACK),
                title=ft.Text("<...>"),
                subtitle=ft.Text(_("Parent directory")),
                on_click=parent_button_click,
            )
        ]

    view.controls.extend(
        [
            DirectoryContextMenu(
                parent_listview=view,
                directory_id=folder["id"],
                dir_name=folder["name"],
                created_at=folder["created_time"],
            )
            for folder in folders
        ]
    )
    view.controls.extend(
        [
            FileContextMenu(
                parent_listview=view,
                file_id=document["id"],
                filename=document["title"],
                size=document["size"],
                last_modified=document["last_modified"],
            )
            for document in documents
        ]
    )
    view.update()

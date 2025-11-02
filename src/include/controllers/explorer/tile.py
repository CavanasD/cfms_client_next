from typing import TYPE_CHECKING
from include.ui.controls.menus.explorer import (
    DirectoryRightMenuDialog,
    DocumentRightMenuDialog,
)
from include.ui.util.path import get_directory, get_document

if TYPE_CHECKING:
    from include.ui.controls.components.explorer.tile import (
        FileGestureListTile,
        DirectoryGestureListTile,
    )


class FileGestureListTileController:
    def __init__(self, control: "FileGestureListTile") -> None:
        self.control = control

    async def action_open_file(self):
        await get_document(
            self.control.file_id,
            filename=self.control.filename,
            view=self.control.parent_listview,
        )

    async def action_open_context_menu(self):
        self.control.page.show_dialog(
            DocumentRightMenuDialog(self.control.file_id, self.control.parent_listview)
        )


class DirectoryGestureListTileController:
    def __init__(self, control: "DirectoryGestureListTile") -> None:
        self.control = control

    async def action_open_directory(self):
        self.control.parent_listview.parent_manager.indicator.go(self.control.dir_name)
        await get_directory(
            self.control.directory_id, view=self.control.parent_listview
        )

    async def action_open_context_menu(self):
        self.control.page.show_dialog(
            DirectoryRightMenuDialog(
                self.control.directory_id, self.control.parent_listview
            )
        )

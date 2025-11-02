from typing import TYPE_CHECKING
from include.controllers.base import BaseController

if TYPE_CHECKING:
    from include.ui.controls.views.explorer import FileListView


class FileListViewController(BaseController):
    def __init__(
        self,
        control: "FileListView",
    ):
        super().__init__(control)

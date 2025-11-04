from typing import TYPE_CHECKING, Optional
import os

import flet as ft

from include.classes.config import AppConfig
from include.classes.exceptions.request import RequestFailureError
from include.classes.exceptions.transmission import (
    FileHashMismatchError,
    FileSizeMismatchError,
)
from include.classes.ui.enum import SortMode, SortOrder
from include.ui.util.notifications import send_error
from include.util.requests import do_request
from include.util.connect import get_connection
from include.util.transfer import receive_file_from_server

if TYPE_CHECKING:
    from include.ui.controls.views.explorer import FileListView

from include.util.locale import get_translation
t = get_translation()
_ = t.gettext

_app_config = AppConfig()


async def get_directory(
    id: str | None,
    view: "FileListView",
    fallback: Optional[str] = None,
    _raise_on_error=False,
    _set_new_root=False,
):
    from include.ui.util.file_controls import update_file_controls

    view.parent_manager.hide_content()

    response = await do_request(
        action="list_directory",
        data={"folder_id": id},
        username=_app_config.username,
        token=_app_config.token,
    )

    if (code := response["code"]) != 200:
        update_file_controls(view, [], [], view.parent_manager.current_directory_id)
        if _raise_on_error:
            view.parent_manager.progress_ring.visible = False
            view.parent_manager.progress_ring.update()
            view.visible = True
            view.update()
            if fallback != None:
                await get_directory(fallback, view)
            raise RequestFailureError("Get directory failed", response)
        send_error(
            view.page,
            _("Load failed: ({code}) {message}").format(
                code=code, message=response["message"]
            ),
        )
    else:
        if _set_new_root:
            view.parent_manager.root_directory_id = id

        view.parent_manager.current_directory_id = id

        view.current_directories_data = response["data"]["folders"]
        view.current_files_data = response["data"]["documents"]
        view.current_parent_id = response["data"]["parent_id"]

        await view.parent_manager.sort_bar.controller.apply_sorting()

        # update_file_controls(
        #     view,
        #     response["data"]["folders"],
        #     response["data"]["documents"],
        #     response["data"]["parent_id"],
        # )

    view.parent_manager.show_content()


async def get_document(id: str | None, filename: str, view: "FileListView"):
    assert type(view.page) == ft.Page
    response = await do_request(
        action="get_document",
        data={"document_id": id},
        username=_app_config.username,
        token=_app_config.token,
    )

    task_data = response["data"]["task_data"]
    task_id = task_data["task_id"]
    task_start_time = task_data["start_time"]
    task_end_time = task_data["end_time"]

    assert view.page.platform
    if view.page.platform.value in ["android"]:
        file_path = f"/storage/emulated/0/{filename if filename else task_id[0:17]}"
    else:
        file_path = f"./{filename if filename else task_id[0:17]}"

    transfer_conn = await get_connection(
        view.page.session.store.get("server_uri"), max_size=1024**2 * 4
    )

    # build progress bar

    progress_bar = ft.ProgressBar()
    progress_info = ft.Text(text_align=ft.TextAlign.CENTER, color=ft.Colors.WHITE)
    progress_column = ft.Column(
        controls=[progress_bar, progress_info],
        alignment=(
            ft.MainAxisAlignment.START if os.name == "nt" else ft.MainAxisAlignment.END
        ),
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    view.page.overlay.append(progress_column)
    view.page.update()

    try:
        async for stage, *data in receive_file_from_server(
            transfer_conn, task_id=task_id, file_path=file_path
        ):
            match stage:
                case 0:
                    received_file_size, file_size = data
                    progress_bar.value = received_file_size / file_size
                    progress_info.value = (
                        f"{received_file_size / 1024 / 1024:.2f} MB"
                        f"/{file_size / 1024 / 1024:.2f} MB"
                    )
                case 1:
                    decrypted_chunks, total_chunks = data
                    progress_bar.value = decrypted_chunks / total_chunks
                    progress_info.value = _(
                        "Decrypting chunk [{decrypted_chunks}/{total_chunks}]"
                    ).format(
                        decrypted_chunks=decrypted_chunks,
                        total_chunks=total_chunks,
                    )
                case 2:
                    progress_bar.value = None
                    progress_info.value = _("Deleting temporary files")
                case 3:
                    progress_bar.value = None
                    progress_info.value = _("Verifying file")

            progress_column.update()
    except FileHashMismatchError as exc:
        send_error(view.page, _("File hash mismatch: {exc}").format(exc=str(exc)))
    except FileSizeMismatchError as exc:
        send_error(view.page, _("File size mismatch: {exc}").format(exc=str(exc)))
    finally:
        view.page.overlay.remove(progress_column)
        view.page.update()

from typing import Callable, Optional
import flet as ft
from include.ui.controls.dialogs.base import AlertDialog
from include.util.locale import get_translation
from functools import wraps
from typing import TypeVar, ParamSpec, Callable, Any
import asyncio
import inspect
from typing import Awaitable

__all__ = ["PendingResponseDialog", "wait"]

t = get_translation()
_ = t.gettext

P = ParamSpec("P")
R = TypeVar("R")


class PendingResponseDialog(AlertDialog):
    def __init__(
        self,
        action: Optional[str] = None,
        ref: ft.Ref | None = None,
        visible: bool = True,
    ):
        super().__init__(
            title=_("In Progress"),
            content=ft.Column(
                controls=[
                    ft.ProgressRing(),
                    ft.Text(
                        _(
                            "Waiting for a server response; this process may take some time."
                        )
                    ),
                    ft.Text(
                        _("Processing action: {action}").format(action=action),
                        italic=True,
                        size=12,
                        visible=bool(action),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            modal=True,
            scrollable=True,
            ref=ref,
            visible=visible,
        )


def wait(
    action: Optional[str] = None,
) -> Callable[[Callable[P, R]], Callable[P, Awaitable[R]]]:

    def _decorator(func: Callable[P, R]) -> Callable[P, Awaitable[R]]:

        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            self: Any = args[0]
            pending_dialog = PendingResponseDialog(action=action)
            # show dialog (synchronous call into Flet)
            self.control.page.show_dialog(pending_dialog)
            try:
                if inspect.iscoroutinefunction(func):
                    result: R = await func(*args, **kwargs)  # type: ignore
                else:
                    loop = asyncio.get_running_loop()
                    result: R = await loop.run_in_executor(
                        None, lambda: func(*args, **kwargs)
                    )
            finally:
                # close dialog (synchronous)
                pending_dialog.close()

            return result

        return wrapper

    return _decorator

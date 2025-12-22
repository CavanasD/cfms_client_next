import flet as ft
from include.util.locale import get_translation

t = get_translation()
_ = t.gettext


class VersionTypeBlock(ft.Container):
    """
    A row to show the stage and other info during
    the software test.
    """

    def __init__(
        self,
        visible: bool = True,
        ref: ft.Ref | None = None,
    ):
        super().__init__(expand=True, expand_loose=True, visible=visible, ref=ref)
        self.heading_letter = ft.Text("α", size=90, weight=ft.FontWeight.BOLD)
        self.trailing_info = ft.Column(
            controls=[
                ft.Text(_("Alpha Test"), size=24, weight=ft.FontWeight.BOLD),
                ft.Text(_("This software is currently in alpha testing phase.")),
                ft.Text(
                    _(
                        "Software at this stage may receive intensive updates, "
                        "but many problems may also appear and disappear in a "
                        "short period of time."
                    ),
                ),
                ft.Text(
                    _(
                        "Any issues encountered should be reported in time, "
                        "but may take a long time to get resolved."
                    )
                ),
            ],
            spacing=5,
            expand=True,
            expand_loose=True,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self._row = ft.Row(
            controls=[self.heading_letter, self.trailing_info],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            margin=ft.Margin(20, 0, 20, 0),
            spacing=15,
            expand=True,
            expand_loose=True,
        )

        self.content = self._row

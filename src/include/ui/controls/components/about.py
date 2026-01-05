import flet as ft
from include.util.locale import get_translation
from include.constants import CHANNEL
from include.classes.version import ChannelType

t = get_translation()
_ = t.gettext

__all__ = ["VersionTypeBlock"]


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

        __channel_mappings = {
            ChannelType.ALPHA: AlphaChannelInfoRow,
            ChannelType.BETA: BetaChannelInfoRow,
            ChannelType.STABLE: None,
        }

        self.content = (
            __channel_mappings[CHANNEL]() if CHANNEL != ChannelType.STABLE else None
        )


class AlphaChannelInfoRow(ft.Row):
    def __init__(
        self,
        visible: bool = True,
        ref: ft.Ref | None = None,
    ):
        super().__init__(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            margin=ft.Margin(20, 0, 20, 0),
            spacing=15,
            expand=True,
            expand_loose=True,
            ref=ref,
            visible=visible,
        )

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

        self.controls = [self.heading_letter, self.trailing_info]


class BetaChannelInfoRow(ft.Row):
    def __init__(
        self,
        visible: bool = True,
        ref: ft.Ref | None = None,
    ):
        super().__init__(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            margin=ft.Margin(20, 0, 20, 0),
            spacing=15,
            expand=True,
            expand_loose=True,
            ref=ref,
            visible=visible,
        )

        self.heading_letter = ft.Text("β", size=90, weight=ft.FontWeight.BOLD)
        self.trailing_info = ft.Column(
            controls=[
                ft.Text(_("Beta Test"), size=24, weight=ft.FontWeight.BOLD),
                ft.Text(_("This software is currently in beta testing phase.")),
                ft.Text(
                    _(
                        "Although the application at this stage is still in "
                        "testing, it has become relatively stable and is more "
                        "suitable for general users to try. After one or more "
                        "versions are released, the application may enter a "
                        "stable version."
                    ),
                ),
            ],
            spacing=5,
            expand=True,
            expand_loose=True,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.controls = [self.heading_letter, self.trailing_info]

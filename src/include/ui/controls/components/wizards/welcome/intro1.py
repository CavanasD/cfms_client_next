import flet as ft
from include.util.locale import get_translation

t = get_translation()
_ = t.gettext


class IntroPage1(ft.Container):
    def __init__(self):
        super().__init__()
        self.content = ft.Column(
            controls=[
                ft.Text(
                    _("Welcome to the CFMS Client Application"),
                    style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD),
                ),
                ft.Text(
                    _(
                        "This is a management system specifically designed for the secure "
                        "transmission and confidentiality of confidential information over"
                        " the internet, aiming to ensure process compliance through a "
                        "procedural approach."
                    ),
                    style=ft.TextStyle(size=16),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )

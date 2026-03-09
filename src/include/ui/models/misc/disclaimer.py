import sys

import flet as ft
from flet_material_symbols import Symbols
from flet_model import Model, route, Router

from include.classes.shared import AppShared
from include.ui.util.route import get_parent_route
from include.util.locale import get_translation

t = get_translation()
_ = t.gettext


__all__ = ["DisclaimerModel"]

DISCLAIMER = _(
    "Welcome to the Confidential File Management System (CFMS). This system is "
    "designed for the online distribution of confidential documents, aiming to help "
    "system administrators quickly build a user-friendly application ecosystem that "
    "closely meets their needs.\n\n"
    "Please note that while this system is designed to minimize unauthorized access, "
    "it **CANNOT** prevent information leaks caused by authorized users. Files will "
    "be decrypted locally on the client's device and will remain decrypted regardless "
    "of whether they are being accessed. Improper configuration could allow other "
    "applications installed on the same device to gain access to these files, "
    "potentially causing significant information leaks. **Preventing such issues is "
    "your responsibility.**\n\n"
    "For the reasons stated above, please exercise extreme caution before connecting "
    "to and logging into the target server to ensure information security and "
    "confidentiality.\n\n"
    "Please:\n\n"
    "- **DO NOT** launch this application in public places.\n\n"
    "- **DO NOT** launch this application and connect to the server in the presence of "
    "others who are unaware of the confidential information you are accessing.\n\n"
    "- Unless otherwise permitted, **DO NOT** distribute confidential information "
    "obtained from this application in any other non-confidential manner.\n\n"
    "- **DO NOT** launch this application on unprotected devices (devices without any "
    "measures in place to prevent unauthorized access) and use it to obtain any "
    "confidential information.\n\n"
    "- **DO NOT** disclose the existence and purpose of this application to anyone who "
    "is unaware of the confidential information you wish to access.\n\n"
    "- Regularly check the application's security settings to ensure all "
    "security-related configurations are up-to-date. Also, strive to update to "
    "the latest stable version promptly, as these may contain fixes for security "
    "vulnerabilities."
)


@route("disclaimer")
class DisclaimerModel(Model):
    """
    ViewModel for the Disclaimer screen.

    This model manages the state and logic for the disclaimer screen, including
    user interactions and data binding for the UI components.
    """

    # Layout configuration
    vertical_alignment = ft.MainAxisAlignment.START
    horizontal_alignment = ft.CrossAxisAlignment.BASELINE
    padding = 20
    spacing = 10
    can_pop = False

    def __init__(self, page: ft.Page, router: Router):
        super().__init__(page, router)
        # self.scroll = ft.ScrollMode.AUTO

        self.leading = ft.Icon(Symbols.WARNING, color=ft.Colors.YELLOW, size=40)
        self.title = ft.Text(_("Disclaimer"), size=24, weight=ft.FontWeight.BOLD)
        self.disclaimer_intro = ft.Text(
            _("Please read and accept the disclaimer before using the application."),
            size=14,
            color=ft.Colors.WHITE,
        )
        self.disclaimer_content = ft.Markdown(
            DISCLAIMER,
        )
        self.disclaimer_end = ft.Text(
            _(
                "You are solely responsible for any unintended disclosure of "
                "confidential information resulting from improper use of this "
                "application."
            ),
            weight=ft.FontWeight.BOLD,
        )
        self.accept_button = ft.Button(
            _("Accept"),
            on_click=self.accept_disclaimer,
        )
        self.reject_button = ft.Button(
            _("Reject and Quit"),
            on_click=self.reject_disclaimer,
            visible=not AppShared().is_mobile,
        )

        self.controls = [
            ft.SafeArea(self.leading),
            self.title,
            self.disclaimer_intro,
            ft.Divider(),
            ft.Column(
                [self.disclaimer_content],
                scroll=ft.ScrollMode.ALWAYS,
                expand=True,
                expand_loose=True,
            ),
            ft.Divider(),
            self.disclaimer_end,
            ft.ResponsiveRow(
                controls=[self.accept_button, self.reject_button],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ]

    async def accept_disclaimer(self, event: ft.Event[ft.Button]):
        AppShared().preferences["license"]["disclaimer_accepted"] = True
        AppShared().dump_preferences()
        await self.page.push_route(get_parent_route(self.page.route))

    async def reject_disclaimer(self, event: ft.Event[ft.Button]):
        await self.page.window.close()
        sys.exit(0)

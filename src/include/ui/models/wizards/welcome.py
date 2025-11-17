from flet_model import Model, Router, route
import flet as ft

from include.ui.controls.components.wizards.welcome.intro1 import IntroPage1
from include.util.locale import get_translation

t = get_translation()
_ = t.gettext


@route("welcome_wizard")
class WelcomeWizardModel(Model):

    # Layout configuration
    vertical_alignment = ft.MainAxisAlignment.START
    horizontal_alignment = ft.CrossAxisAlignment.BASELINE
    padding = 20
    spacing = 10
    scroll = ft.ScrollMode.AUTO

    def __init__(self, page: ft.Page, router: Router):
        super().__init__(page, router)
        self.page: ft.Page
        self.appbar = ft.AppBar(title=ft.Text(_("Intro Wizard")))
        self.intro_page1 = IntroPage1()
        self.controls = [
            self.intro_page1,
        ]
import flet as ft

from include.util.locale import get_translation

t = get_translation()
_ = t.gettext


class FloatingUpgradeButton(ft.FloatingActionButton):
    def __init__(self, ref: ft.Ref | None = None, visible=True):
        super().__init__(ref=ref, visible=visible)
        self.icon = ft.Icons.BROWSER_UPDATED_OUTLINED
        self.badge = None  # Badge can be added later when needed
        self.on_click = self.button_click
        self.tooltip = _("Check for Updates")

    async def button_click(self, event: ft.Event[ft.FloatingActionButton]):
        assert type(self.page) == ft.Page
        await self.page.push_route("/connect/about/")

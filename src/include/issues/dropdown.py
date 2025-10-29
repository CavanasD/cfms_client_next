import flet as ft


class SubRuleGroupEditEntriesArea(ft.ExpansionTile):
    def __init__(
        self,
        entry_type: str,  # "groups" | "rights"
        match_mode: str,
        ref: ft.Ref | None = None,
    ):
        self.page: ft.Page
        self.entry_type = entry_type
        self.match_mode = match_mode

        self.mode_dropdown = ft.Dropdown(
            options=[
                ft.DropdownOption(
                    "all",
                    "ALL",
                    leading_icon=ft.Icons.SELECT_ALL,
                ),
                ft.DropdownOption(
                    "any",
                    "ANY",
                    leading_icon=ft.Icons.FILE_COPY,
                ),
            ],
            label="Match Mode",
            value=self.match_mode,
            on_change=self.on_match_mode_changed,
            align=ft.Alignment.TOP_LEFT,
            dense=True,
            expand=True,
            expand_loose=True,
        )

        controls = [
            self.mode_dropdown,
        ]

        match self.entry_type:
            case "groups":
                title = "Groups"
            case "rights":
                title = "Rights"
            case _:
                raise ValueError(f"Invalid entry type '{self.entry_type}'")

        super().__init__(
            title=title,
            controls=controls,
            ref=ref,
            controls_padding=ft.Padding(top=15),
            initially_expanded=True,
        )

    async def on_match_mode_changed(self, event: ft.Event[ft.Dropdown]):
        self.match_mode = event.control.value
        print(f"Event data: {event.data}")
        print(f"Current self.match_mode: {self.match_mode}")


def main(page: ft.Page):
    page.title = "SubRuleGroupEditEntriesArea Demo"

    entries_area = SubRuleGroupEditEntriesArea(
        entry_type="groups",
        match_mode="all",
    )

    page.add(entries_area)


if __name__ == "__main__":
    ft.run(main)
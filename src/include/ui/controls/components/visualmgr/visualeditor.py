from copy import deepcopy
from typing import TYPE_CHECKING, Any, Optional
import flet as ft
import bidict

if TYPE_CHECKING:
    from include.ui.controls.components.rulemanager import VisualRuleEditor

from include.util.locale import get_translation

t = get_translation()
_ = t.gettext


class EditSectionEntriesControlBar(ft.Row):
    def __init__(
        self,
        parent_area: "SubRuleGroupEditEntriesArea",
        ref: ft.Ref | None = None,
    ):
        super().__init__(ref=ref)
        self.page: ft.Page
        self.parent_area = parent_area

        self.progress_ring = ft.ProgressRing(visible=False)
        self.name_textfield = ft.TextField(
            expand=True,
            expand_loose=True,
            hint_text=_("Add..."),
            on_submit=self.on_textfield_submit,
        )
        self.submit_button = ft.IconButton(
            icon=ft.Icons.ADD,
            on_click=self.on_add_button_click,
        )

        self.controls = [
            self.name_textfield,
            self.submit_button,
            self.progress_ring,
        ]

    def disable_interactions(self):
        self.name_textfield.disabled = True
        self.submit_button.visible = False
        self.progress_ring.visible = True
        self.update()

    def enable_interactions(self):
        self.name_textfield.disabled = False
        self.submit_button.visible = True
        self.progress_ring.visible = False
        self.update()

    async def on_textfield_submit(self, event: ft.Event[ft.TextField]):
        self.page.run_task(self.action_submit)

    async def on_add_button_click(self, event: ft.Event[ft.IconButton]):
        self.page.run_task(self.action_submit)

    async def action_submit(self):
        current_textfield_value = self.name_textfield.value.strip()
        if not current_textfield_value:
            return  # Ignore empty input

        self.disable_interactions()
        self.parent_area.require.append(current_textfield_value)
        self.parent_area.require_listview.controls.append(
            EntryListTile(self.parent_area, current_textfield_value)
        )
        self.parent_area.require_listview.update()
        self.name_textfield.value = ""
        self.enable_interactions()


class EntryListTile(ft.ListTile):
    def __init__(
        self,
        parent_entries_area: "SubRuleGroupEditEntriesArea",
        entry_name: str,
        ref: ft.Ref | None = None,
    ):
        super().__init__(ref=ref)
        self.page: ft.Page
        self.parent_entries_area = parent_entries_area
        self.entry_name = entry_name

        self.title = ft.Text(self.entry_name)
        self.trailing = ft.IconButton(
            icon=ft.Icons.REMOVE,
            on_click=self.on_remove_clicked,
        )

    async def on_remove_clicked(self, event: ft.Event[ft.IconButton]):
        self.parent_entries_area.require.remove(self.entry_name)
        self.parent_entries_area.require_listview.controls.remove(self)


class SubRuleGroupEditEntriesArea(ft.ExpansionTile):
    def __init__(
        self,
        parent_edit_area: "SubRuleGroupEditArea",
        entry_type: str,  # "groups" | "rights"
        match_mode: str,
        require: list[str],
        ref: ft.Ref | None = None,
    ):
        self.page: ft.Page
        self.parent_edit_area = parent_edit_area
        self.entry_type = entry_type
        self.match_mode = match_mode
        self.require = require

        self.option_names_bidict = bidict.bidict(
            {
                "all": _("All"),
                "any": _("Any"),
            }
        )

        self.mode_dropdown = ft.Dropdown(
            options=[
                ft.DropdownOption(
                    "all",
                    self.option_names_bidict["all"],
                    leading_icon=ft.Icons.SELECT_ALL,
                ),
                ft.DropdownOption(
                    "any",
                    self.option_names_bidict["any"],
                    leading_icon=ft.Icons.FILE_COPY,
                ),
            ],
            label=_("Match Mode"),
            value=self.match_mode,
            on_change=self.on_match_mode_changed,
            align=ft.Alignment.TOP_LEFT,
            dense=True,
            expand=True,
            expand_loose=True,
        )

        self.require_listview = ft.ListView(
            expand=True,
            expand_loose=True,
            spacing=5,
            padding=ft.Padding.only(top=5),
            controls=[EntryListTile(self, name) for name in self.require],
        )

        controls = [
            self.mode_dropdown,
            EditSectionEntriesControlBar(self),
            self.require_listview,
            # EditSectionEntriesControlBar(self),
        ]

        match self.entry_type:
            case "groups":
                title = _("Groups")
            case "rights":
                title = _("Rights")
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
        # This is a temporary workaround for ft.Dropdown not updating value immediately.
        # It seemed that only by using event.data can we always get the updated value.
        self.match_mode = self.option_names_bidict.inverse[event.data]
        # print(f"Match mode changed to {self.match_mode}")

    @property
    def dict_data(self) -> dict[str, Any]:
        return {
            "match": self.match_mode,
            "require": self.require,
        }


class SubRuleGroupEditArea(ft.ExpansionTile):
    def __init__(
        self,
        parent_collection_area: "SubRuleGroupCollectionArea",
        index: int,
        match_mode: str,
        match_groups: dict[str, Any],
        match_rights: dict[str, Any],
        ref: ft.Ref | None = None,
    ):

        self.page: ft.Page
        self.parent_collection_area = parent_collection_area
        self.index = index
        self.match_mode = match_mode
        self.match_groups = deepcopy(match_groups)
        self.match_rights = deepcopy(match_rights)

        match self.match_mode:
            case "all":
                display_match_mode = _("All of the following")
            case "any":
                display_match_mode = _("Any of the following")
            case _:
                raise ValueError(f"Invalid subgroup match mode '{self.match_mode}'")

        controls = []

        if self.match_rights:  # handle rights
            rights_block_match_mode = self.match_rights.get("match", None)
            rights_block_require = self.match_rights.get("require", [])
            assert rights_block_match_mode is not None

            rights_block_expansion_tile = SubRuleGroupEditEntriesArea(
                self,
                "rights",
                rights_block_match_mode,
                rights_block_require,
            )
            controls.append(rights_block_expansion_tile)

        if self.match_groups:  # handle groups
            groups_block_match_mode = self.match_groups.get("match", None)
            groups_block_require = self.match_groups.get("require", [])
            assert groups_block_match_mode is not None

            groups_block_expansion_tile = SubRuleGroupEditEntriesArea(
                self,
                "groups",
                groups_block_match_mode,
                groups_block_require,
            )

            controls.append(groups_block_expansion_tile)

        super().__init__(
            _("Subgroup #{index}").format(
                index=self.index,
            ),
            subtitle=_("Mode: {mode}").format(mode=display_match_mode),
            controls=controls,
            initially_expanded=True,
            ref=ref,
        )

    def did_mount(self):
        super().did_mount()

    @property
    def dict_data(self) -> dict[str, Any]:
        assert self.controls
        data: dict[str, Any] = {"match": self.match_mode}

        for control in self.controls:
            if isinstance(control, SubRuleGroupEditEntriesArea):
                data[control.entry_type] = control.dict_data
        return data


class SubRuleGroupCollectionArea(ft.ExpansionTile):
    def __init__(
        self,
        index: int,
        match_mode: str,
        match_groups: list[dict],
        parent_edit_section: "VisualRuleEditorEditSection",
        ref: ft.Ref | None = None,
    ):
        super().__init__(
            title=_("#{index}").format(
                index=index + 1,
            ),
            subtitle=_("Mode: {mode}").format(mode=match_mode),
            initially_expanded=not index,
            expand=True,
            expand_loose=True,
            align=ft.Alignment.TOP_CENTER,
            ref=ref,
        )
        self.page: ft.Page
        self.parent_edit_section = parent_edit_section
        self.controls = []

        self.index = index
        self.match_mode = match_mode

        for subgroup in match_groups:
            subgroup_match_mode: Optional[str] = subgroup.get("match", None)
            subgroup_rights_block: dict = subgroup.get("rights", {})
            subgroup_groups_block: dict = subgroup.get("groups", {})
            assert subgroup_match_mode is not None

            subgroup_expansion_tile = SubRuleGroupEditArea(
                self,
                match_groups.index(subgroup) + 1,
                subgroup_match_mode,
                subgroup_groups_block,
                subgroup_rights_block,
            )

            self.controls.append(subgroup_expansion_tile)

    @property
    def dict_data(self) -> list[dict[str, Any]]:
        assert self.controls
        data: list[dict[str, Any]] = []

        for control in self.controls:
            if isinstance(control, SubRuleGroupEditArea):
                data.append(control.dict_data)

        return data


class VisualRuleEditorEditSection(ft.Column):
    def __init__(
        self,
        parent_editor: "VisualRuleEditor",
        access_type: str,
        ref: ft.Ref | None = None,
    ):
        super().__init__(ref=ref, expand=True, expand_loose=True)
        self.page: ft.Page
        # self.alignment = ft.MainAxisAlignment.
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.scroll = ft.ScrollMode.AUTO
        self.access_type = access_type  # "read", "write", "move", "manage"

        self.parent_editor = parent_editor
        self.controls = []

    async def load_rules(self):
        # clear existing controls
        self.controls.clear()

        async def parse_sub_rules(
            match_mode: str, match_groups: list[dict], index
        ) -> SubRuleGroupCollectionArea:

            return SubRuleGroupCollectionArea(
                index,
                match_mode,
                match_groups,
                self,
            )

        rules: list[dict] = self.parent_editor.edited_rule_data.get(
            self.access_type, []
        )

        for rule in rules:
            match_mode = rule.get("match", None)
            match_groups = rule.get("match_groups", [])
            assert match_mode is not None

            # get ExpansionTile for this rule
            new_rule_tile = await parse_sub_rules(
                match_mode, match_groups, rules.index(rule)
            )
            self.controls.append(new_rule_tile)

        if not self.controls:
            self.controls.append(
                ft.Text(
                    _("No rules defined for this access type."),
                    text_align=ft.TextAlign.CENTER,
                    align=ft.Alignment.CENTER,
                )
            )

        self.update()

    def did_mount(self):
        super().did_mount()
        self.page.run_task(self.load_rules)

    def will_unmount(self):
        super().will_unmount()
        self.parent_editor.edited_rule_data[self.access_type] = self.dict_data

    @property
    def dict_data(self) -> list[dict[str, Any]]:
        assert self.controls
        data: list[dict[str, Any]] = []

        for control in self.controls:
            if isinstance(control, SubRuleGroupCollectionArea):
                data.append(
                    {
                        "match": control.match_mode,
                        "match_groups": control.dict_data,
                    }
                )

        return data


class VisualRuleEditorNavigationRail(ft.NavigationRail):
    def __init__(self, parent_editor: "VisualRuleEditor", ref: ft.Ref | None = None):
        super().__init__(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            group_alignment=0.0,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.PAGEVIEW_OUTLINED,
                    selected_icon=ft.Icons.PAGEVIEW,
                    label="Read",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.EDIT_OUTLINED),
                    selected_icon=ft.Icon(ft.Icons.EDIT),
                    label="Write",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.DRIVE_FILE_MOVE_OUTLINED,
                    selected_icon=ft.Icon(ft.Icons.DRIVE_FILE_MOVE),
                    label="Move",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.MANAGE_ACCOUNTS_OUTLINED,
                    selected_icon=ft.Icon(ft.Icons.MANAGE_ACCOUNTS),
                    label="Manage",
                ),
            ],
            ref=ref,
        )
        self.parent_editor = parent_editor
        self.on_change = self.handle_navigation_change

    async def handle_navigation_change(self, event: ft.Event[ft.NavigationRail]):
        match self.selected_index:
            case 0:  # Read
                mode = "read"
            case 1:  # Write
                mode = "write"
            case 2:  # Move
                mode = "move"
            case 3:  # Manage
                mode = "manage"
            case _:
                raise ValueError("Invalid navigation index")

        self.parent_editor.current_edit_section_container.content = (
            VisualRuleEditorEditSection(self.parent_editor, mode)
        )
        self.update()

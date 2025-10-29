from typing import TYPE_CHECKING
import flet as ft
from include.util.locale import get_translation

if TYPE_CHECKING:
    from include.ui.controls.components.visualmgr.editor import (
        VisualRuleEditorEditSection,
        SubRuleGroupCollectionArea,
    )

t = get_translation()
_ = t.gettext


class CollectionAreasColumn(ft.Column):
    def __init__(
        self,
        parent_edit_section: "VisualRuleEditorEditSection",
        ref: ft.Ref | None = None,
    ):
        super().__init__(expand=True, expand_loose=True, ref=ref)
        self.page: ft.Page
        self.parent_edit_section = parent_edit_section

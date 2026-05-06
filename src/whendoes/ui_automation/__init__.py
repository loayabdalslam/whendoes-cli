"""UI Automation module for Windows accessibility tree extraction."""

from whendoes.ui_automation.extractor import (
    extract_ui_tree,
    get_window_ui_context,
    find_element_by_id,
    get_element_info,
)
from whendoes.ui_automation.actions import (
    click_element,
    type_text,
    get_element_value,
    invoke_pattern,
    select_item,
)

__all__ = [
    "extract_ui_tree",
    "get_window_ui_context",
    "find_element_by_id",
    "get_element_info",
    "click_element",
    "type_text",
    "get_element_value",
    "invoke_pattern",
    "select_item",
]

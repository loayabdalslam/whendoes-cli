"""Extract UI Automation tree from Windows applications."""

import json
from typing import Optional, Any, Dict, List
from dataclasses import dataclass, asdict

try:
    import uiautomation as auto
except ImportError:
    raise ImportError("uiautomation required: pip install uiautomation")


@dataclass
class UIElement:
    """Represents a UI element from the automation tree."""

    element_id: str
    name: str
    control_type: str
    automation_id: str
    is_enabled: bool
    is_visible: bool
    bounding_rect: Dict[str, int]
    children: List["UIElement"] = None
    patterns: List[str] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []
        if self.patterns is None:
            self.patterns = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.element_id,
            "name": self.name,
            "type": self.control_type,
            "automation_id": self.automation_id,
            "enabled": self.is_enabled,
            "visible": self.is_visible,
            "rect": self.bounding_rect,
            "patterns": self.patterns,
            "children": [child.to_dict() for child in self.children],
        }


def _get_control_type_name(element) -> str:
    """Get human-readable control type name."""
    control_type_map = {
        auto.ControlType.Button: "Button",
        auto.ControlType.Edit: "TextBox",
        auto.ControlType.Text: "Text",
        auto.ControlType.Window: "Window",
        auto.ControlType.Menu: "Menu",
        auto.ControlType.MenuItem: "MenuItem",
        auto.ControlType.ComboBox: "ComboBox",
        auto.ControlType.ListItem: "ListItem",
        auto.ControlType.List: "List",
        auto.ControlType.CheckBox: "CheckBox",
        auto.ControlType.RadioButton: "RadioButton",
        auto.ControlType.Pane: "Pane",
        auto.ControlType.Document: "Document",
        auto.ControlType.Hyperlink: "Hyperlink",
        auto.ControlType.Image: "Image",
        auto.ControlType.Spinner: "Spinner",
        auto.ControlType.Slider: "Slider",
        auto.ControlType.ProgressBar: "ProgressBar",
        auto.ControlType.ScrollBar: "ScrollBar",
        auto.ControlType.Tab: "Tab",
        auto.ControlType.TabItem: "TabItem",
        auto.ControlType.Tree: "Tree",
        auto.ControlType.TreeItem: "TreeItem",
        auto.ControlType.DataGrid: "DataGrid",
        auto.ControlType.DataItem: "DataItem",
        auto.ControlType.Group: "Group",
        auto.ControlType.Thumb: "Thumb",
        auto.ControlType.ToolBar: "ToolBar",
        auto.ControlType.ToolTip: "ToolTip",
        auto.ControlType.Calendar: "Calendar",
        auto.ControlType.Custom: "Custom",
        auto.ControlType.Separator: "Separator",
        auto.ControlType.AppBar: "AppBar",
        auto.ControlType.Header: "Header",
        auto.ControlType.HeaderItem: "HeaderItem",
        auto.ControlType.SemanticZoom: "SemanticZoom",
        auto.ControlType.SplitButton: "SplitButton",
        auto.ControlType.StatusBar: "StatusBar",
    }
    return control_type_map.get(element.ControlType, "Unknown")


def _get_supported_patterns(element) -> List[str]:
    """Get list of supported patterns for an element."""
    patterns = []
    try:
        if element.InvokePattern:
            patterns.append("Invoke")
    except:
        pass
    try:
        if element.SelectionPattern:
            patterns.append("Selection")
    except:
        pass
    try:
        if element.ValuePattern:
            patterns.append("Value")
    except:
        pass
    try:
        if element.TextPattern:
            patterns.append("Text")
    except:
        pass
    try:
        if element.TogglePattern:
            patterns.append("Toggle")
    except:
        pass
    try:
        if element.ExpandCollapsePattern:
            patterns.append("ExpandCollapse")
    except:
        pass
    try:
        if element.ScrollPattern:
            patterns.append("Scroll")
    except:
        pass
    try:
        if element.RangeValuePattern:
            patterns.append("RangeValue")
    except:
        pass
    return patterns


def _extract_element_tree(
    element, max_depth: int = 5, current_depth: int = 0, element_id_counter: dict = None
) -> Optional[UIElement]:
    """Recursively extract UI element tree."""
    if element_id_counter is None:
        element_id_counter = {"count": 0}

    if current_depth > max_depth:
        return None

    try:
        element_id_counter["count"] += 1
        element_id = f"elem_{element_id_counter['count']}"

        name = element.Name or ""
        control_type = _get_control_type_name(element)
        automation_id = element.AutomationId or ""
        is_enabled = element.IsEnabled
        is_visible = element.IsVisible

        # Get bounding rectangle
        try:
            rect = element.BoundingRectangle
            bounding_rect = {
                "left": rect.left,
                "top": rect.top,
                "right": rect.right,
                "bottom": rect.bottom,
                "width": rect.right - rect.left,
                "height": rect.bottom - rect.top,
            }
        except:
            bounding_rect = {"left": 0, "top": 0, "right": 0, "bottom": 0}

        # Get supported patterns
        patterns = _get_supported_patterns(element)

        # Extract children (only interactive elements)
        children = []
        try:
            for child in element.GetChildren():
                child_element = _extract_element_tree(
                    child, max_depth, current_depth + 1, element_id_counter
                )
                if child_element:
                    children.append(child_element)
        except:
            pass

        return UIElement(
            element_id=element_id,
            name=name,
            control_type=control_type,
            automation_id=automation_id,
            is_enabled=is_enabled,
            is_visible=is_visible,
            bounding_rect=bounding_rect,
            children=children,
            patterns=patterns,
        )
    except Exception as e:
        return None


def extract_ui_tree(window_title: str, max_depth: int = 5) -> Optional[UIElement]:
    """Extract UI automation tree from a window.

    Args:
        window_title: Window title (partial match)
        max_depth: Maximum depth to traverse

    Returns:
        UIElement tree or None if window not found
    """
    try:
        # Find window
        window = auto.GetWindowByPartialName(window_title)
        if not window:
            return None

        # Extract tree
        return _extract_element_tree(window, max_depth)
    except Exception as e:
        return None


def get_window_ui_context(window_title: str, max_depth: int = 3) -> str:
    """Get UI context as JSON string for LLM.

    Args:
        window_title: Window title
        max_depth: Maximum depth

    Returns:
        JSON string describing the UI
    """
    tree = extract_ui_tree(window_title, max_depth)
    if not tree:
        return json.dumps({"error": f"Window '{window_title}' not found"})

    # Flatten and compress the tree for LLM
    def flatten_tree(element: UIElement, depth: int = 0) -> List[Dict]:
        """Flatten tree to list of elements."""
        items = []

        # Only include interactive elements
        if element.control_type in [
            "Button",
            "TextBox",
            "MenuItem",
            "ComboBox",
            "CheckBox",
            "RadioButton",
            "Hyperlink",
            "Tab",
            "TabItem",
            "ListItem",
            "Menu",
        ] or element.patterns:
            items.append(
                {
                    "id": element.element_id,
                    "name": element.name,
                    "type": element.control_type,
                    "patterns": element.patterns,
                    "enabled": element.is_enabled,
                    "depth": depth,
                }
            )

        # Add children
        for child in element.children:
            items.extend(flatten_tree(child, depth + 1))

        return items

    elements = flatten_tree(tree)

    context = {
        "window": tree.name,
        "elements": elements,
        "total_elements": len(elements),
    }

    return json.dumps(context, indent=2)


def find_element_by_id(window_title: str, element_id: str) -> Optional[Any]:
    """Find element by ID in window.

    Args:
        window_title: Window title
        element_id: Element ID

    Returns:
        UIAutomation element or None
    """
    try:
        tree = extract_ui_tree(window_title)
        if not tree:
            return None

        def search_tree(element: UIElement) -> Optional[Any]:
            if element.element_id == element_id:
                # Return the actual automation element
                window = auto.GetWindowByPartialName(window_title)
                return _find_automation_element(window, element_id)
            for child in element.children:
                result = search_tree(child)
                if result:
                    return result
            return None

        return search_tree(tree)
    except:
        return None


def _find_automation_element(element, target_id: str, counter: dict = None) -> Optional[Any]:
    """Find automation element by ID."""
    if counter is None:
        counter = {"count": 0}

    counter["count"] += 1
    if f"elem_{counter['count']}" == target_id:
        return element

    try:
        for child in element.GetChildren():
            result = _find_automation_element(child, target_id, counter)
            if result:
                return result
    except:
        pass

    return None


def get_element_info(window_title: str, element_id: str) -> Dict[str, Any]:
    """Get detailed information about an element.

    Args:
        window_title: Window title
        element_id: Element ID

    Returns:
        Dictionary with element information
    """
    tree = extract_ui_tree(window_title)
    if not tree:
        return {"error": "Window not found"}

    def find_in_tree(element: UIElement) -> Optional[UIElement]:
        if element.element_id == element_id:
            return element
        for child in element.children:
            result = find_in_tree(child)
            if result:
                return result
        return None

    element = find_in_tree(tree)
    if not element:
        return {"error": "Element not found"}

    return element.to_dict()

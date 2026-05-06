"""Windows UI Automation - Extract and interact with Accessibility Tree."""

import json
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, asdict

try:
    from pywinauto import Application
    from pywinauto.uia_defines import IFACE_NAME
except ImportError:
    raise ImportError("pywinauto required: pip install pywinauto")


@dataclass
class UIElement:
    """Represents a UI element in the Accessibility Tree."""
    id: str
    name: str
    role: str
    control_type: str
    is_enabled: bool
    is_visible: bool
    value: Optional[str] = None
    children: List['UIElement'] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "control_type": self.control_type,
            "is_enabled": self.is_enabled,
            "is_visible": self.is_visible,
            "value": self.value,
            "children": [child.to_dict() for child in self.children],
        }

    def to_text(self, indent: int = 0) -> str:
        """Convert to readable text format."""
        prefix = "  " * indent
        text = f"{prefix}[{self.id}] {self.role}: {self.name}"
        if self.value:
            text += f" = '{self.value}'"
        if not self.is_enabled:
            text += " (disabled)"
        if not self.is_visible:
            text += " (hidden)"
        text += "\n"

        for child in self.children:
            text += child.to_text(indent + 1)

        return text


class UIAutomationExtractor:
    """Extract Accessibility Tree from Windows applications."""

    def __init__(self, app_name: str = "chrome"):
        """Initialize extractor.

        Args:
            app_name: Application name (chrome, edge, firefox, etc.)
        """
        self.app_name = app_name.lower()
        self.app = None
        self.element_counter = 0

    def connect(self) -> bool:
        """Connect to running application.

        Returns:
            True if connected successfully
        """
        try:
            if self.app_name == "chrome":
                self.app = Application(backend="uia").connect(title_re=".*Chrome.*")
            elif self.app_name == "edge":
                self.app = Application(backend="uia").connect(title_re=".*Edge.*")
            elif self.app_name == "firefox":
                self.app = Application(backend="uia").connect(title_re=".*Firefox.*")
            else:
                self.app = Application(backend="uia").connect(title_re=f".*{self.app_name}.*")
            return True
        except Exception as e:
            print(f"Failed to connect to {self.app_name}: {e}")
            return False

    def extract_tree(self, max_depth: int = 10) -> Optional[UIElement]:
        """Extract Accessibility Tree from application.

        Args:
            max_depth: Maximum depth to traverse

        Returns:
            Root UIElement or None if failed
        """
        if not self.app:
            if not self.connect():
                return None

        try:
            self.element_counter = 0
            root = self.app.top_window()
            return self._extract_element(root, depth=0, max_depth=max_depth)
        except Exception as e:
            print(f"Failed to extract tree: {e}")
            return None

    def _extract_element(self, element, depth: int = 0, max_depth: int = 10) -> Optional[UIElement]:
        """Recursively extract element and children.

        Args:
            element: pywinauto element
            depth: Current depth
            max_depth: Maximum depth to traverse

        Returns:
            UIElement or None
        """
        if depth > max_depth:
            return None

        try:
            self.element_counter += 1
            element_id = f"elem_{self.element_counter}"

            # Get element properties
            name = self._safe_get(element, "name", "")
            control_type = self._safe_get(element, "control_type", "Unknown")
            role = self._get_role(control_type)
            is_enabled = self._safe_get(element, "is_enabled", True)
            is_visible = self._safe_get(element, "is_visible", True)
            value = self._safe_get(element, "value", None)

            # Create element
            ui_element = UIElement(
                id=element_id,
                name=name,
                role=role,
                control_type=control_type,
                is_enabled=is_enabled,
                is_visible=is_visible,
                value=value,
            )

            # Extract children
            try:
                children = element.children()
                for child in children:
                    child_element = self._extract_element(child, depth + 1, max_depth)
                    if child_element:
                        ui_element.children.append(child_element)
            except Exception:
                pass

            return ui_element

        except Exception as e:
            print(f"Error extracting element: {e}")
            return None

    def _safe_get(self, element, attr: str, default: Any = None) -> Any:
        """Safely get element attribute.

        Args:
            element: pywinauto element
            attr: Attribute name
            default: Default value if attribute not found

        Returns:
            Attribute value or default
        """
        try:
            return getattr(element, attr)
        except Exception:
            return default

    def _get_role(self, control_type: str) -> str:
        """Map control type to role.

        Args:
            control_type: Control type string

        Returns:
            Role name
        """
        role_map = {
            "Button": "button",
            "Edit": "textbox",
            "ComboBox": "combobox",
            "ListBox": "listbox",
            "ListItem": "option",
            "CheckBox": "checkbox",
            "RadioButton": "radio",
            "Hyperlink": "link",
            "Text": "text",
            "Document": "document",
            "Window": "window",
            "TabItem": "tab",
            "TabControl": "tablist",
            "Pane": "region",
            "Menu": "menu",
            "MenuItem": "menuitem",
        }
        return role_map.get(control_type, control_type.lower())

    def find_element_by_name(self, name: str, tree: Optional[UIElement] = None) -> Optional[UIElement]:
        """Find element by name in tree.

        Args:
            name: Element name to search for
            tree: Root element (extracts if None)

        Returns:
            UIElement or None
        """
        if tree is None:
            tree = self.extract_tree()
            if not tree:
                return None

        if name.lower() in tree.name.lower():
            return tree

        for child in tree.children:
            result = self.find_element_by_name(name, child)
            if result:
                return result

        return None

    def find_elements_by_role(self, role: str, tree: Optional[UIElement] = None) -> List[UIElement]:
        """Find all elements with specific role.

        Args:
            role: Role to search for
            tree: Root element (extracts if None)

        Returns:
            List of UIElements
        """
        if tree is None:
            tree = self.extract_tree()
            if not tree:
                return []

        results = []

        if tree.role == role:
            results.append(tree)

        for child in tree.children:
            results.extend(self.find_elements_by_role(role, child))

        return results

    def get_tree_json(self, max_depth: int = 10) -> Optional[str]:
        """Get tree as JSON string.

        Args:
            max_depth: Maximum depth to traverse

        Returns:
            JSON string or None
        """
        tree = self.extract_tree(max_depth)
        if not tree:
            return None
        return json.dumps(tree.to_dict(), indent=2)

    def get_tree_text(self, max_depth: int = 10) -> Optional[str]:
        """Get tree as readable text.

        Args:
            max_depth: Maximum depth to traverse

        Returns:
            Text representation or None
        """
        tree = self.extract_tree(max_depth)
        if not tree:
            return None
        return tree.to_text()


class UIAutomationExecutor:
    """Execute actions on UI elements."""

    def __init__(self, app_name: str = "chrome"):
        """Initialize executor.

        Args:
            app_name: Application name
        """
        self.extractor = UIAutomationExtractor(app_name)
        self.element_map = {}

    def click_element(self, element_id: str) -> bool:
        """Click element by ID.

        Args:
            element_id: Element ID

        Returns:
            True if successful
        """
        try:
            if element_id not in self.element_map:
                return False

            element = self.element_map[element_id]
            element.click()
            return True
        except Exception as e:
            print(f"Failed to click element: {e}")
            return False

    def type_text(self, element_id: str, text: str) -> bool:
        """Type text into element.

        Args:
            element_id: Element ID
            text: Text to type

        Returns:
            True if successful
        """
        try:
            if element_id not in self.element_map:
                return False

            element = self.element_map[element_id]
            element.type_keys(text)
            return True
        except Exception as e:
            print(f"Failed to type text: {e}")
            return False

    def get_element_value(self, element_id: str) -> Optional[str]:
        """Get element value.

        Args:
            element_id: Element ID

        Returns:
            Element value or None
        """
        try:
            if element_id not in self.element_map:
                return None

            element = self.element_map[element_id]
            return getattr(element, "value", None)
        except Exception as e:
            print(f"Failed to get element value: {e}")
            return None

    def build_element_map(self, tree: UIElement) -> None:
        """Build map of element IDs to elements.

        Args:
            tree: Root UIElement
        """
        self.element_map[tree.id] = tree

        for child in tree.children:
            self.build_element_map(child)

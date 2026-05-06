"""Accessibility tools for interacting with UI elements."""

from typing import Optional, List, Dict, Any
from whendoes.windows_api.ui_automation import UIAutomationExtractor, UIElement


def read_accessibility_tree(app_name: str = "chrome", max_depth: int = 8) -> str:
    """Read accessibility tree from application.

    Args:
        app_name: Application name (chrome, edge, firefox, etc.)
        max_depth: Maximum depth to traverse

    Returns:
        Text representation of accessibility tree
    """
    try:
        extractor = UIAutomationExtractor(app_name)
        tree = extractor.extract_tree(max_depth)
        if not tree:
            return f"Failed to read accessibility tree from {app_name}"
        return tree.to_text()
    except Exception as e:
        return f"Error reading accessibility tree: {e}"


def find_element_by_name(app_name: str, element_name: str) -> Optional[Dict[str, Any]]:
    """Find element by name in application.

    Args:
        app_name: Application name
        element_name: Element name to search for

    Returns:
        Element info or None
    """
    try:
        extractor = UIAutomationExtractor(app_name)
        tree = extractor.extract_tree()
        if not tree:
            return None

        element = extractor.find_element_by_name(element_name, tree)
        if not element:
            return None

        return {
            "id": element.id,
            "name": element.name,
            "role": element.role,
            "control_type": element.control_type,
            "is_enabled": element.is_enabled,
            "is_visible": element.is_visible,
            "value": element.value,
        }
    except Exception as e:
        return {"error": str(e)}


def find_elements_by_role(app_name: str, role: str) -> List[Dict[str, Any]]:
    """Find all elements with specific role.

    Args:
        app_name: Application name
        role: Element role (button, textbox, link, etc.)

    Returns:
        List of element info
    """
    try:
        extractor = UIAutomationExtractor(app_name)
        tree = extractor.extract_tree()
        if not tree:
            return []

        elements = extractor.find_elements_by_role(role, tree)
        return [
            {
                "id": elem.id,
                "name": elem.name,
                "role": elem.role,
                "control_type": elem.control_type,
                "is_enabled": elem.is_enabled,
                "is_visible": elem.is_visible,
            }
            for elem in elements
        ]
    except Exception as e:
        return [{"error": str(e)}]


def get_element_info(app_name: str, element_id: str) -> Optional[Dict[str, Any]]:
    """Get detailed information about an element.

    Args:
        app_name: Application name
        element_id: Element ID

    Returns:
        Element info or None
    """
    try:
        extractor = UIAutomationExtractor(app_name)
        tree = extractor.extract_tree()
        if not tree:
            return None

        # Find element by ID
        def find_by_id(elem: UIElement, target_id: str) -> Optional[UIElement]:
            if elem.id == target_id:
                return elem
            for child in elem.children:
                result = find_by_id(child, target_id)
                if result:
                    return result
            return None

        element = find_by_id(tree, element_id)
        if not element:
            return None

        return {
            "id": element.id,
            "name": element.name,
            "role": element.role,
            "control_type": element.control_type,
            "is_enabled": element.is_enabled,
            "is_visible": element.is_visible,
            "value": element.value,
            "children_count": len(element.children),
        }
    except Exception as e:
        return {"error": str(e)}


def list_all_buttons(app_name: str = "chrome") -> List[Dict[str, Any]]:
    """List all buttons in application.

    Args:
        app_name: Application name

    Returns:
        List of button info
    """
    return find_elements_by_role(app_name, "button")


def list_all_textboxes(app_name: str = "chrome") -> List[Dict[str, Any]]:
    """List all textboxes in application.

    Args:
        app_name: Application name

    Returns:
        List of textbox info
    """
    return find_elements_by_role(app_name, "textbox")


def list_all_links(app_name: str = "chrome") -> List[Dict[str, Any]]:
    """List all links in application.

    Args:
        app_name: Application name

    Returns:
        List of link info
    """
    return find_elements_by_role(app_name, "link")


def list_all_tabs(app_name: str = "chrome") -> List[Dict[str, Any]]:
    """List all tabs in application.

    Args:
        app_name: Application name

    Returns:
        List of tab info
    """
    return find_elements_by_role(app_name, "tab")


def get_page_title(app_name: str = "chrome") -> str:
    """Get page title from application.

    Args:
        app_name: Application name

    Returns:
        Page title
    """
    try:
        extractor = UIAutomationExtractor(app_name)
        tree = extractor.extract_tree()
        if not tree:
            return "Unknown"
        return tree.name
    except Exception as e:
        return f"Error: {e}"


def get_page_content_summary(app_name: str = "chrome", max_items: int = 10) -> str:
    """Get summary of page content.

    Args:
        app_name: Application name
        max_items: Maximum items to include

    Returns:
        Content summary
    """
    try:
        extractor = UIAutomationExtractor(app_name)
        tree = extractor.extract_tree(max_depth=5)
        if not tree:
            return "No content found"

        # Collect interactive elements
        buttons = extractor.find_elements_by_role("button", tree)
        links = extractor.find_elements_by_role("link", tree)
        textboxes = extractor.find_elements_by_role("textbox", tree)

        summary = f"""Page: {tree.name}

Buttons ({len(buttons)}):
"""
        for btn in buttons[:max_items]:
            summary += f"  - [{btn.id}] {btn.name}\n"

        summary += f"\nLinks ({len(links)}):\n"
        for link in links[:max_items]:
            summary += f"  - [{link.id}] {link.name}\n"

        summary += f"\nTextboxes ({len(textboxes)}):\n"
        for tb in textboxes[:max_items]:
            summary += f"  - [{tb.id}] {tb.name}\n"

        return summary
    except Exception as e:
        return f"Error: {e}"


def search_element(app_name: str, search_term: str) -> List[Dict[str, Any]]:
    """Search for elements containing search term.

    Args:
        app_name: Application name
        search_term: Search term

    Returns:
        List of matching elements
    """
    try:
        extractor = UIAutomationExtractor(app_name)
        tree = extractor.extract_tree()
        if not tree:
            return []

        results = []

        def search_recursive(elem: UIElement) -> None:
            if search_term.lower() in elem.name.lower():
                results.append(
                    {
                        "id": elem.id,
                        "name": elem.name,
                        "role": elem.role,
                        "control_type": elem.control_type,
                    }
                )
            for child in elem.children:
                search_recursive(child)

        search_recursive(tree)
        return results
    except Exception as e:
        return [{"error": str(e)}]


def get_element_path(app_name: str, element_id: str) -> str:
    """Get path to element in hierarchy.

    Args:
        app_name: Application name
        element_id: Element ID

    Returns:
        Element path
    """
    try:
        extractor = UIAutomationExtractor(app_name)
        tree = extractor.extract_tree()
        if not tree:
            return "Not found"

        path = []

        def find_path(elem: UIElement, target_id: str) -> bool:
            path.append(f"[{elem.id}] {elem.name}")
            if elem.id == target_id:
                return True
            for child in elem.children:
                if find_path(child, target_id):
                    return True
            path.pop()
            return False

        if find_path(tree, element_id):
            return " → ".join(path)
        return "Element not found"
    except Exception as e:
        return f"Error: {e}"


def count_elements_by_role(app_name: str) -> Dict[str, int]:
    """Count elements by role.

    Args:
        app_name: Application name

    Returns:
        Dictionary of role counts
    """
    try:
        extractor = UIAutomationExtractor(app_name)
        tree = extractor.extract_tree()
        if not tree:
            return {}

        counts = {}

        def count_recursive(elem: UIElement) -> None:
            role = elem.role
            counts[role] = counts.get(role, 0) + 1
            for child in elem.children:
                count_recursive(child)

        count_recursive(tree)
        return counts
    except Exception as e:
        return {"error": str(e)}


def get_interactive_elements(app_name: str = "chrome") -> Dict[str, List[Dict[str, Any]]]:
    """Get all interactive elements (buttons, links, textboxes, etc.).

    Args:
        app_name: Application name

    Returns:
        Dictionary of interactive elements by type
    """
    try:
        extractor = UIAutomationExtractor(app_name)
        tree = extractor.extract_tree()
        if not tree:
            return {}

        return {
            "buttons": [
                {"id": e.id, "name": e.name}
                for e in extractor.find_elements_by_role("button", tree)
            ],
            "links": [
                {"id": e.id, "name": e.name}
                for e in extractor.find_elements_by_role("link", tree)
            ],
            "textboxes": [
                {"id": e.id, "name": e.name}
                for e in extractor.find_elements_by_role("textbox", tree)
            ],
            "tabs": [
                {"id": e.id, "name": e.name}
                for e in extractor.find_elements_by_role("tab", tree)
            ],
            "checkboxes": [
                {"id": e.id, "name": e.name}
                for e in extractor.find_elements_by_role("checkbox", tree)
            ],
        }
    except Exception as e:
        return {"error": str(e)}


def get_visible_elements(app_name: str = "chrome") -> List[Dict[str, Any]]:
    """Get all visible elements.

    Args:
        app_name: Application name

    Returns:
        List of visible elements
    """
    try:
        extractor = UIAutomationExtractor(app_name)
        tree = extractor.extract_tree()
        if not tree:
            return []

        visible = []

        def collect_visible(elem: UIElement) -> None:
            if elem.is_visible:
                visible.append(
                    {
                        "id": elem.id,
                        "name": elem.name,
                        "role": elem.role,
                        "is_enabled": elem.is_enabled,
                    }
                )
            for child in elem.children:
                collect_visible(child)

        collect_visible(tree)
        return visible
    except Exception as e:
        return [{"error": str(e)}]


def get_enabled_elements(app_name: str = "chrome") -> List[Dict[str, Any]]:
    """Get all enabled elements.

    Args:
        app_name: Application name

    Returns:
        List of enabled elements
    """
    try:
        extractor = UIAutomationExtractor(app_name)
        tree = extractor.extract_tree()
        if not tree:
            return []

        enabled = []

        def collect_enabled(elem: UIElement) -> None:
            if elem.is_enabled:
                enabled.append(
                    {
                        "id": elem.id,
                        "name": elem.name,
                        "role": elem.role,
                        "is_visible": elem.is_visible,
                    }
                )
            for child in elem.children:
                collect_enabled(child)

        collect_enabled(tree)
        return enabled
    except Exception as e:
        return [{"error": str(e)}]

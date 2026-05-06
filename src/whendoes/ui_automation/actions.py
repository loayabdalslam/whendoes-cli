"""UI Automation actions - execute patterns on elements."""

from typing import Optional, Any

try:
    import uiautomation as auto
except ImportError:
    raise ImportError("uiautomation required: pip install uiautomation")


def click_element(window_title: str, element_id: str) -> bool:
    """Click an element.

    Args:
        window_title: Window title
        element_id: Element ID

    Returns:
        True if successful
    """
    try:
        from whendoes.ui_automation.extractor import find_element_by_id

        element = find_element_by_id(window_title, element_id)
        if not element:
            return False

        # Try Invoke pattern first
        try:
            if element.InvokePattern:
                element.Invoke()
                return True
        except:
            pass

        # Fallback to click
        try:
            element.Click()
            return True
        except:
            pass

        return False
    except Exception as e:
        return False


def type_text(window_title: str, element_id: str, text: str) -> bool:
    """Type text into an element.

    Args:
        window_title: Window title
        element_id: Element ID
        text: Text to type

    Returns:
        True if successful
    """
    try:
        from whendoes.ui_automation.extractor import find_element_by_id

        element = find_element_by_id(window_title, element_id)
        if not element:
            return False

        # Try Value pattern
        try:
            if element.ValuePattern:
                element.SetValue(text)
                return True
        except:
            pass

        # Fallback to keyboard input
        try:
            element.Click()
            auto.TypeKeys(text)
            return True
        except:
            pass

        return False
    except Exception as e:
        return False


def get_element_value(window_title: str, element_id: str) -> Optional[str]:
    """Get value from an element.

    Args:
        window_title: Window title
        element_id: Element ID

    Returns:
        Element value or None
    """
    try:
        from whendoes.ui_automation.extractor import find_element_by_id

        element = find_element_by_id(window_title, element_id)
        if not element:
            return None

        # Try Value pattern
        try:
            if element.ValuePattern:
                return element.GetValue()
        except:
            pass

        # Try Text pattern
        try:
            if element.TextPattern:
                return element.GetText()
        except:
            pass

        # Try Name
        try:
            return element.Name
        except:
            pass

        return None
    except Exception as e:
        return None


def invoke_pattern(window_title: str, element_id: str) -> bool:
    """Invoke pattern on an element (for buttons, etc).

    Args:
        window_title: Window title
        element_id: Element ID

    Returns:
        True if successful
    """
    try:
        from whendoes.ui_automation.extractor import find_element_by_id

        element = find_element_by_id(window_title, element_id)
        if not element:
            return False

        if element.InvokePattern:
            element.Invoke()
            return True

        return False
    except Exception as e:
        return False


def select_item(window_title: str, element_id: str) -> bool:
    """Select an item (for lists, comboboxes, etc).

    Args:
        window_title: Window title
        element_id: Element ID

    Returns:
        True if successful
    """
    try:
        from whendoes.ui_automation.extractor import find_element_by_id

        element = find_element_by_id(window_title, element_id)
        if not element:
            return False

        if element.SelectionPattern:
            element.Select()
            return True

        return False
    except Exception as e:
        return False


def toggle_element(window_title: str, element_id: str) -> bool:
    """Toggle an element (for checkboxes, etc).

    Args:
        window_title: Window title
        element_id: Element ID

    Returns:
        True if successful
    """
    try:
        from whendoes.ui_automation.extractor import find_element_by_id

        element = find_element_by_id(window_title, element_id)
        if not element:
            return False

        if element.TogglePattern:
            element.Toggle()
            return True

        return False
    except Exception as e:
        return False


def expand_element(window_title: str, element_id: str) -> bool:
    """Expand an element (for trees, groups, etc).

    Args:
        window_title: Window title
        element_id: Element ID

    Returns:
        True if successful
    """
    try:
        from whendoes.ui_automation.extractor import find_element_by_id

        element = find_element_by_id(window_title, element_id)
        if not element:
            return False

        if element.ExpandCollapsePattern:
            element.Expand()
            return True

        return False
    except Exception as e:
        return False

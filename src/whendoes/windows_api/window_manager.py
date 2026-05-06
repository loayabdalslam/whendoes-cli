"""Windows window management."""

from dataclasses import dataclass
from typing import Optional

try:
    import pygetwindow as gw
    import pyautogui
except ImportError:
    raise ImportError("pygetwindow and pyautogui required: pip install pygetwindow pyautogui")


@dataclass
class Window:
    """Window information."""

    title: str
    hwnd: int
    x: int
    y: int
    width: int
    height: int
    is_active: bool


def list_windows() -> list[Window]:
    """List all open windows.

    Returns:
        List of Window objects
    """
    windows = []
    for win in gw.getAllWindows():
        if win.title.strip():  # Skip windows with empty titles
            windows.append(
                Window(
                    title=win.title,
                    hwnd=win._hWnd,
                    x=win.left,
                    y=win.top,
                    width=win.width,
                    height=win.height,
                    is_active=win.isActive,
                )
            )
    return windows


def get_window_by_title(title: str) -> Optional[Window]:
    """Get window by title.

    Args:
        title: Window title (partial match)

    Returns:
        Window object or None if not found
    """
    for win in gw.getAllWindows():
        if title.lower() in win.title.lower():
            return Window(
                title=win.title,
                hwnd=win._hWnd,
                x=win.left,
                y=win.top,
                width=win.width,
                height=win.height,
                is_active=win.isActive,
            )
    return None


def focus_window(title: str) -> bool:
    """Focus window by title.

    Args:
        title: Window title (partial match)

    Returns:
        True if successful
    """
    try:
        win = gw.getWindowsWithTitle(title)
        if win:
            win[0].activate()
            return True
        return False
    except Exception:
        return False


def close_window(title: str) -> bool:
    """Close window by title.

    Args:
        title: Window title (partial match)

    Returns:
        True if successful
    """
    try:
        win = gw.getWindowsWithTitle(title)
        if win:
            win[0].close()
            return True
        return False
    except Exception:
        return False


def minimize_window(title: str) -> bool:
    """Minimize window by title.

    Args:
        title: Window title (partial match)

    Returns:
        True if successful
    """
    try:
        win = gw.getWindowsWithTitle(title)
        if win:
            win[0].minimize()
            return True
        return False
    except Exception:
        return False


def maximize_window(title: str) -> bool:
    """Maximize window by title.

    Args:
        title: Window title (partial match)

    Returns:
        True if successful
    """
    try:
        win = gw.getWindowsWithTitle(title)
        if win:
            win[0].maximize()
            return True
        return False
    except Exception:
        return False


def resize_window(title: str, width: int, height: int) -> bool:
    """Resize window by title.

    Args:
        title: Window title (partial match)
        width: New width
        height: New height

    Returns:
        True if successful
    """
    try:
        win = gw.getWindowsWithTitle(title)
        if win:
            win[0].resize(width, height)
            return True
        return False
    except Exception:
        return False


def move_window(title: str, x: int, y: int) -> bool:
    """Move window by title.

    Args:
        title: Window title (partial match)
        x: New X position
        y: New Y position

    Returns:
        True if successful
    """
    try:
        win = gw.getWindowsWithTitle(title)
        if win:
            win[0].moveTo(x, y)
            return True
        return False
    except Exception:
        return False

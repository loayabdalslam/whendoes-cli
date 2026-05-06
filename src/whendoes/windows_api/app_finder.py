"""Find installed applications on Windows."""

import os
import winreg
from pathlib import Path
from typing import Optional


def find_app_path(app_name: str) -> Optional[str]:
    """Find installed application path by name.

    Searches:
    1. Program Files
    2. Program Files (x86)
    3. Windows Registry (Uninstall keys)
    4. Common app locations

    Args:
        app_name: Application name (e.g., 'Chrome', 'Notepad', 'Firefox')

    Returns:
        Path to executable or None if not found
    """
    app_name_lower = app_name.lower()

    # Common installation paths
    common_paths = [
        Path("C:/Program Files"),
        Path("C:/Program Files (x86)"),
        Path(os.path.expandvars("%PROGRAMFILES%")),
        Path(os.path.expandvars("%PROGRAMFILES(X86)%")),
        Path(os.path.expandvars("%LOCALAPPDATA%")),
        Path(os.path.expandvars("%APPDATA%")),
    ]

    # Search in common paths
    for base_path in common_paths:
        if not base_path.exists():
            continue

        try:
            for item in base_path.rglob("*"):
                if item.is_file() and item.suffix.lower() == ".exe":
                    if app_name_lower in item.name.lower():
                        return str(item)
        except (PermissionError, OSError):
            continue

    # Search Windows Registry
    exe_path = _search_registry(app_name)
    if exe_path:
        return exe_path

    # Special cases
    special_cases = {
        "chrome": _find_chrome,
        "firefox": _find_firefox,
        "edge": _find_edge,
        "notepad": _find_notepad,
        "vscode": _find_vscode,
        "python": _find_python,
    }

    for key, finder in special_cases.items():
        if key in app_name_lower:
            path = finder()
            if path:
                return path

    return None


def _search_registry(app_name: str) -> Optional[str]:
    """Search Windows Registry for application path.

    Args:
        app_name: Application name

    Returns:
        Path to executable or None
    """
    try:
        reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

        for hive in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
            try:
                with winreg.OpenKey(hive, reg_path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        subkey_name = winreg.EnumKey(key, i)
                        try:
                            with winreg.OpenKey(hive, f"{reg_path}\\{subkey_name}") as subkey:
                                display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]

                                if app_name.lower() in display_name.lower():
                                    try:
                                        install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                        exe_path = Path(install_location) / f"{app_name}.exe"
                                        if exe_path.exists():
                                            return str(exe_path)
                                    except (FileNotFoundError, OSError):
                                        pass
                        except (OSError, WindowsError):
                            continue
            except (OSError, WindowsError):
                continue
    except Exception:
        pass

    return None


def _find_chrome() -> Optional[str]:
    """Find Chrome installation path."""
    paths = [
        Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
        Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
        Path(os.path.expandvars("%LOCALAPPDATA%/Google/Chrome/Application/chrome.exe")),
    ]

    for path in paths:
        if path.exists():
            return str(path)

    return None


def _find_firefox() -> Optional[str]:
    """Find Firefox installation path."""
    paths = [
        Path("C:/Program Files/Mozilla Firefox/firefox.exe"),
        Path("C:/Program Files (x86)/Mozilla Firefox/firefox.exe"),
        Path(os.path.expandvars("%PROGRAMFILES%/Mozilla Firefox/firefox.exe")),
    ]

    for path in paths:
        if path.exists():
            return str(path)

    return None


def _find_edge() -> Optional[str]:
    """Find Microsoft Edge installation path."""
    paths = [
        Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
        Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
        Path(os.path.expandvars("%PROGRAMFILES%/Microsoft/Edge/Application/msedge.exe")),
    ]

    for path in paths:
        if path.exists():
            return str(path)

    return None


def _find_notepad() -> Optional[str]:
    """Find Notepad installation path."""
    paths = [
        Path("C:/Windows/System32/notepad.exe"),
        Path("C:/Windows/notepad.exe"),
    ]

    for path in paths:
        if path.exists():
            return str(path)

    return None


def _find_vscode() -> Optional[str]:
    """Find Visual Studio Code installation path."""
    paths = [
        Path("C:/Program Files/Microsoft VS Code/Code.exe"),
        Path("C:/Program Files (x86)/Microsoft VS Code/Code.exe"),
        Path(os.path.expandvars("%LOCALAPPDATA%/Programs/Microsoft VS Code/Code.exe")),
    ]

    for path in paths:
        if path.exists():
            return str(path)

    return None


def _find_python() -> Optional[str]:
    """Find Python installation path."""
    paths = [
        Path("C:/Python311/python.exe"),
        Path("C:/Python310/python.exe"),
        Path("C:/Python39/python.exe"),
        Path(os.path.expandvars("%LOCALAPPDATA%/Programs/Python/Python311/python.exe")),
    ]

    for path in paths:
        if path.exists():
            return str(path)

    return None

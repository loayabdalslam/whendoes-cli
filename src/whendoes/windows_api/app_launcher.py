"""Windows application launching."""

import subprocess
from typing import Optional

try:
    import psutil
except ImportError:
    raise ImportError("psutil required: pip install psutil")


def launch_app(app_path: str, args: Optional[list[str]] = None) -> bool:
    """Launch an application.

    Args:
        app_path: Path to application executable
        args: Command line arguments

    Returns:
        True if successful
    """
    try:
        cmd = [app_path]
        if args:
            cmd.extend(args)
        subprocess.Popen(cmd)
        return True
    except Exception:
        return False


def launch_app_by_name(app_name: str, args: Optional[list[str]] = None) -> bool:
    """Launch application by name (searches PATH).

    Args:
        app_name: Application name (e.g., 'notepad', 'chrome')
        args: Command line arguments

    Returns:
        True if successful
    """
    try:
        cmd = [app_name]
        if args:
            cmd.extend(args)
        subprocess.Popen(cmd)
        return True
    except Exception:
        return False


def launch_url(url: str) -> bool:
    """Open URL in default browser.

    Args:
        url: URL to open

    Returns:
        True if successful
    """
    try:
        import webbrowser
        webbrowser.open(url)
        return True
    except Exception:
        return False


def launch_file(file_path: str) -> bool:
    """Open file with default application.

    Args:
        file_path: Path to file

    Returns:
        True if successful
    """
    try:
        import os
        os.startfile(file_path)
        return True
    except Exception:
        return False

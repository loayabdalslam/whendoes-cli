"""Windows file operations."""

import os
import shutil
from pathlib import Path
from typing import Optional


def list_files(directory: str) -> list[str]:
    """List files in directory.

    Args:
        directory: Directory path

    Returns:
        List of file paths
    """
    try:
        return [str(p) for p in Path(directory).iterdir()]
    except Exception:
        return []


def file_exists(path: str) -> bool:
    """Check if file exists.

    Args:
        path: File path

    Returns:
        True if file exists
    """
    return Path(path).exists()


def create_file(path: str, content: str = "") -> bool:
    """Create a new file.

    Args:
        path: File path
        content: File content

    Returns:
        True if successful
    """
    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(content)
        return True
    except Exception:
        return False


def delete_file(path: str) -> bool:
    """Delete a file.

    Args:
        path: File path

    Returns:
        True if successful
    """
    try:
        Path(path).unlink()
        return True
    except Exception:
        return False


def copy_file(source: str, destination: str) -> bool:
    """Copy a file.

    Args:
        source: Source file path
        destination: Destination file path

    Returns:
        True if successful
    """
    try:
        Path(destination).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        return True
    except Exception:
        return False


def move_file(source: str, destination: str) -> bool:
    """Move a file.

    Args:
        source: Source file path
        destination: Destination file path

    Returns:
        True if successful
    """
    try:
        Path(destination).parent.mkdir(parents=True, exist_ok=True)
        shutil.move(source, destination)
        return True
    except Exception:
        return False


def read_file(path: str) -> Optional[str]:
    """Read file content.

    Args:
        path: File path

    Returns:
        File content or None if error
    """
    try:
        return Path(path).read_text()
    except Exception:
        return None


def write_file(path: str, content: str) -> bool:
    """Write to file.

    Args:
        path: File path
        content: Content to write

    Returns:
        True if successful
    """
    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(content)
        return True
    except Exception:
        return False


def create_directory(path: str) -> bool:
    """Create a directory.

    Args:
        path: Directory path

    Returns:
        True if successful
    """
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False


def delete_directory(path: str) -> bool:
    """Delete a directory.

    Args:
        path: Directory path

    Returns:
        True if successful
    """
    try:
        shutil.rmtree(path)
        return True
    except Exception:
        return False

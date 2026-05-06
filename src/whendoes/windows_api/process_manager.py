"""Windows process management."""

from dataclasses import dataclass
from typing import Optional

try:
    import psutil
except ImportError:
    raise ImportError("psutil required: pip install psutil")


@dataclass
class Process:
    """Process information."""

    pid: int
    name: str
    exe: str
    status: str
    memory_mb: float


def list_processes() -> list[Process]:
    """List all running processes.

    Returns:
        List of Process objects
    """
    processes = []
    for proc in psutil.process_iter(["pid", "name", "exe", "status"]):
        try:
            mem = proc.memory_info().rss / (1024 * 1024)  # Convert to MB
            processes.append(
                Process(
                    pid=proc.pid,
                    name=proc.name(),
                    exe=proc.exe(),
                    status=proc.status(),
                    memory_mb=mem,
                )
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return processes


def get_process_by_name(name: str) -> Optional[Process]:
    """Get process by name.

    Args:
        name: Process name (partial match)

    Returns:
        Process object or None if not found
    """
    for proc in psutil.process_iter(["pid", "name", "exe", "status"]):
        try:
            if name.lower() in proc.name().lower():
                mem = proc.memory_info().rss / (1024 * 1024)
                return Process(
                    pid=proc.pid,
                    name=proc.name(),
                    exe=proc.exe(),
                    status=proc.status(),
                    memory_mb=mem,
                )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None


def start_process(command: str) -> bool:
    """Start a new process.

    Args:
        command: Command to execute

    Returns:
        True if successful
    """
    try:
        psutil.Popen(command)
        return True
    except Exception:
        return False


def stop_process(pid: int) -> bool:
    """Stop process by PID.

    Args:
        pid: Process ID

    Returns:
        True if successful
    """
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        return True
    except Exception:
        return False


def kill_process(pid: int) -> bool:
    """Kill process by PID (force).

    Args:
        pid: Process ID

    Returns:
        True if successful
    """
    try:
        proc = psutil.Process(pid)
        proc.kill()
        return True
    except Exception:
        return False


def get_process_info(pid: int) -> Optional[Process]:
    """Get process information by PID.

    Args:
        pid: Process ID

    Returns:
        Process object or None if not found
    """
    try:
        proc = psutil.Process(pid)
        mem = proc.memory_info().rss / (1024 * 1024)
        return Process(
            pid=proc.pid,
            name=proc.name(),
            exe=proc.exe(),
            status=proc.status(),
            memory_mb=mem,
        )
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None

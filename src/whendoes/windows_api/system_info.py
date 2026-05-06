"""Windows system information."""

from dataclasses import dataclass

try:
    import psutil
    import platform
except ImportError:
    raise ImportError("psutil required: pip install psutil")


@dataclass
class SystemInfo:
    """System information."""

    os_name: str
    os_version: str
    cpu_count: int
    cpu_percent: float
    memory_total_mb: float
    memory_available_mb: float
    memory_percent: float
    disk_total_mb: float
    disk_free_mb: float
    disk_percent: float


def get_system_info() -> SystemInfo:
    """Get system information.

    Returns:
        SystemInfo object
    """
    cpu_count = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent(interval=1)

    mem = psutil.virtual_memory()
    memory_total_mb = mem.total / (1024 * 1024)
    memory_available_mb = mem.available / (1024 * 1024)
    memory_percent = mem.percent

    disk = psutil.disk_usage("/")
    disk_total_mb = disk.total / (1024 * 1024)
    disk_free_mb = disk.free / (1024 * 1024)
    disk_percent = disk.percent

    return SystemInfo(
        os_name=platform.system(),
        os_version=platform.release(),
        cpu_count=cpu_count,
        cpu_percent=cpu_percent,
        memory_total_mb=memory_total_mb,
        memory_available_mb=memory_available_mb,
        memory_percent=memory_percent,
        disk_total_mb=disk_total_mb,
        disk_free_mb=disk_free_mb,
        disk_percent=disk_percent,
    )


def get_cpu_info() -> dict:
    """Get CPU information.

    Returns:
        Dictionary with CPU info
    """
    return {
        "count": psutil.cpu_count(),
        "percent": psutil.cpu_percent(interval=1),
        "freq": psutil.cpu_freq().current if psutil.cpu_freq() else 0,
    }


def get_memory_info() -> dict:
    """Get memory information.

    Returns:
        Dictionary with memory info
    """
    mem = psutil.virtual_memory()
    return {
        "total_mb": mem.total / (1024 * 1024),
        "available_mb": mem.available / (1024 * 1024),
        "used_mb": mem.used / (1024 * 1024),
        "percent": mem.percent,
    }


def get_disk_info() -> dict:
    """Get disk information.

    Returns:
        Dictionary with disk info
    """
    disk = psutil.disk_usage("/")
    return {
        "total_mb": disk.total / (1024 * 1024),
        "free_mb": disk.free / (1024 * 1024),
        "used_mb": disk.used / (1024 * 1024),
        "percent": disk.percent,
    }

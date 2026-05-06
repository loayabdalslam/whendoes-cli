"""Windows API module."""

from whendoes.windows_api.window_manager import (
    list_windows,
    get_window_by_title,
    focus_window,
    close_window,
    minimize_window,
    maximize_window,
    resize_window,
    move_window,
)
from whendoes.windows_api.process_manager import (
    list_processes,
    get_process_by_name,
    start_process,
    stop_process,
    kill_process,
    get_process_info,
)
from whendoes.windows_api.file_operations import (
    list_files,
    file_exists,
    create_file,
    delete_file,
    copy_file,
    move_file,
    read_file,
    write_file,
    create_directory,
    delete_directory,
)
from whendoes.windows_api.app_launcher import (
    launch_app,
    launch_app_by_name,
    launch_url,
    launch_file,
)
from whendoes.windows_api.system_info import (
    get_system_info,
    get_cpu_info,
    get_memory_info,
    get_disk_info,
)
from whendoes.windows_api.app_finder import (
    find_app_path,
)

__all__ = [
    "list_windows",
    "get_window_by_title",
    "focus_window",
    "close_window",
    "minimize_window",
    "maximize_window",
    "resize_window",
    "move_window",
    "list_processes",
    "get_process_by_name",
    "start_process",
    "stop_process",
    "kill_process",
    "get_process_info",
    "list_files",
    "file_exists",
    "create_file",
    "delete_file",
    "copy_file",
    "move_file",
    "read_file",
    "write_file",
    "create_directory",
    "delete_directory",
    "launch_app",
    "launch_app_by_name",
    "launch_url",
    "launch_file",
    "get_system_info",
    "get_cpu_info",
    "get_memory_info",
    "get_disk_info",
    "find_app_path",
]

"""Tests for Windows API wrappers."""

import pytest
from unittest.mock import patch, MagicMock
from whendoes.windows_api import window_manager, process_manager, file_operations


class TestWindowManager:
    """Tests for window management."""

    @patch("whendoes.windows_api.window_manager.gw.getAllWindows")
    def test_list_windows(self, mock_get_windows):
        """Test listing windows."""
        mock_win = MagicMock()
        mock_win.title = "Test Window"
        mock_win._hWnd = 12345
        mock_win.left = 0
        mock_win.top = 0
        mock_win.width = 800
        mock_win.height = 600
        mock_win.isActive = True

        mock_get_windows.return_value = [mock_win]

        windows = window_manager.list_windows()

        assert len(windows) == 1
        assert windows[0].title == "Test Window"
        assert windows[0].hwnd == 12345

    @patch("whendoes.windows_api.window_manager.gw.getWindowsWithTitle")
    def test_focus_window(self, mock_get_windows):
        """Test focusing window."""
        mock_win = MagicMock()
        mock_get_windows.return_value = [mock_win]

        result = window_manager.focus_window("Test")

        assert result is True
        mock_win.activate.assert_called_once()

    @patch("whendoes.windows_api.window_manager.gw.getWindowsWithTitle")
    def test_close_window(self, mock_get_windows):
        """Test closing window."""
        mock_win = MagicMock()
        mock_get_windows.return_value = [mock_win]

        result = window_manager.close_window("Test")

        assert result is True
        mock_win.close.assert_called_once()


class TestProcessManager:
    """Tests for process management."""

    @patch("whendoes.windows_api.process_manager.psutil.process_iter")
    def test_list_processes(self, mock_process_iter):
        """Test listing processes."""
        mock_proc = MagicMock()
        mock_proc.pid = 1234
        mock_proc.name.return_value = "test.exe"
        mock_proc.exe.return_value = "C:\\test.exe"
        mock_proc.status.return_value = "running"
        mock_proc.memory_info.return_value.rss = 1024 * 1024  # 1 MB

        mock_process_iter.return_value = [mock_proc]

        processes = process_manager.list_processes()

        assert len(processes) == 1
        assert processes[0].name == "test.exe"
        assert processes[0].pid == 1234

    @patch("whendoes.windows_api.process_manager.psutil.Popen")
    def test_start_process(self, mock_popen):
        """Test starting process."""
        result = process_manager.start_process("notepad.exe")

        assert result is True
        mock_popen.assert_called_once_with("notepad.exe")

    @patch("whendoes.windows_api.process_manager.psutil.Process")
    def test_stop_process(self, mock_process):
        """Test stopping process."""
        mock_proc = MagicMock()
        mock_process.return_value = mock_proc

        result = process_manager.stop_process(1234)

        assert result is True
        mock_proc.terminate.assert_called_once()


class TestFileOperations:
    """Tests for file operations."""

    @patch("whendoes.windows_api.file_operations.Path")
    def test_file_exists(self, mock_path):
        """Test checking file existence."""
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance

        result = file_operations.file_exists("test.txt")

        assert result is True

    @patch("whendoes.windows_api.file_operations.Path")
    def test_create_file(self, mock_path):
        """Test creating file."""
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance

        result = file_operations.create_file("test.txt", "content")

        assert result is True
        mock_path_instance.parent.mkdir.assert_called_once()
        mock_path_instance.write_text.assert_called_once_with("content")

    @patch("whendoes.windows_api.file_operations.Path")
    def test_delete_file(self, mock_path):
        """Test deleting file."""
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance

        result = file_operations.delete_file("test.txt")

        assert result is True
        mock_path_instance.unlink.assert_called_once()

    @patch("whendoes.windows_api.file_operations.Path")
    def test_read_file(self, mock_path):
        """Test reading file."""
        mock_path_instance = MagicMock()
        mock_path_instance.read_text.return_value = "content"
        mock_path.return_value = mock_path_instance

        result = file_operations.read_file("test.txt")

        assert result == "content"

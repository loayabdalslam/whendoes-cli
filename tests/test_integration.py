"""Integration test for the complete system."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from whendoes.llm import create_provider
from whendoes.agent import Agent, ToolRegistry
from whendoes.cli.repl import setup_tools
from whendoes.config import get_config


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_provider_creation(self):
        """Test creating all provider types."""
        providers = ["anthropic", "openai", "groq", "gemini", "openrouter", "ollama"]

        for provider_name in providers:
            if provider_name == "ollama":
                # Ollama doesn't need API key
                provider = create_provider(
                    provider_name,
                    base_url="http://localhost:11434",
                )
            else:
                # Others need API key (use dummy for testing)
                provider = create_provider(
                    provider_name,
                    api_key="test-key",
                )

            assert provider is not None
            assert provider.model is not None

    def test_tool_registry_setup(self):
        """Test setting up all tools."""
        tools = setup_tools()

        # Check that all expected tools are registered
        tool_names = [tool.name for tool in tools.get_all_tools()]

        expected_tools = [
            "list_windows",
            "focus_window",
            "close_window",
            "list_processes",
            "start_process",
            "stop_process",
            "create_file",
            "delete_file",
            "read_file",
            "write_file",
            "launch_app_by_name",
            "get_system_info",
        ]

        for tool_name in expected_tools:
            assert tool_name in tool_names, f"Tool {tool_name} not found"

    def test_agent_with_mock_llm(self):
        """Test agent with mocked LLM."""
        from whendoes.llm.base import LLMResponse, ToolCall

        mock_llm = Mock()
        tools = setup_tools()

        # Mock a simple response
        response = LLMResponse(
            content="I've listed the windows",
            tool_calls=[],
            stop_reason="end_turn",
        )
        mock_llm.chat.return_value = response

        agent = Agent(mock_llm, tools)
        result = agent.run("List windows")

        assert "windows" in result.lower()

    def test_config_loading(self):
        """Test configuration loading."""
        config = get_config()

        assert config.llm is not None
        assert config.agent is not None
        assert config.cli is not None
        assert config.llm.provider in [
            "openai",
            "anthropic",
            "groq",
            "gemini",
            "openrouter",
            "ollama",
        ]

    def test_tool_execution_with_mock(self):
        """Test tool execution with mocked Windows API."""
        tools = setup_tools()

        # Get a tool
        list_windows_tool = tools.get_tool("list_windows")
        assert list_windows_tool is not None

        # Mock the Windows API
        with patch("whendoes.windows_api.window_manager.gw.getAllWindows") as mock_get:
            mock_win = MagicMock()
            mock_win.title = "Test Window"
            mock_win._hWnd = 12345
            mock_win.left = 0
            mock_win.top = 0
            mock_win.width = 800
            mock_win.height = 600
            mock_win.isActive = True

            mock_get.return_value = [mock_win]

            # Execute tool
            result = tools.execute_tool("list_windows", {})

            assert isinstance(result, list)
            assert len(result) > 0

    def test_approval_required_tools(self):
        """Test that destructive tools require approval."""
        tools = setup_tools()

        destructive_tools = ["close_window", "stop_process", "kill_process", "delete_file"]

        for tool_name in destructive_tools:
            tool = tools.get_tool(tool_name)
            assert tool is not None
            assert tool.requires_approval is True, f"{tool_name} should require approval"

    def test_safe_tools_no_approval(self):
        """Test that safe tools don't require approval."""
        tools = setup_tools()

        safe_tools = ["list_windows", "list_processes", "read_file", "get_system_info"]

        for tool_name in safe_tools:
            tool = tools.get_tool(tool_name)
            assert tool is not None
            assert tool.requires_approval is False, f"{tool_name} should not require approval"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

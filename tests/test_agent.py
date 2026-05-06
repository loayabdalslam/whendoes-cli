"""Tests for agent system."""

import pytest
from unittest.mock import Mock, MagicMock, patch
from whendoes.agent.agent import Agent
from whendoes.agent.tool_registry import ToolRegistry
from whendoes.llm.base import BaseLLMProvider, Message, LLMResponse, ToolCall


class TestToolRegistry:
    """Tests for tool registry."""

    def test_register_tool(self):
        """Test registering a tool."""
        registry = ToolRegistry()

        def dummy_func(x: int) -> int:
            return x * 2

        registry.register(
            "double",
            "Double a number",
            dummy_func,
            {
                "type": "object",
                "properties": {"x": {"type": "integer"}},
                "required": ["x"],
            },
        )

        assert "double" in registry.tools
        assert registry.tools["double"].name == "double"

    def test_get_tool(self):
        """Test getting a tool."""
        registry = ToolRegistry()

        def dummy_func():
            return 42

        registry.register("answer", "Get the answer", dummy_func, {})

        tool = registry.get_tool("answer")
        assert tool is not None
        assert tool.name == "answer"

    def test_execute_tool(self):
        """Test executing a tool."""
        registry = ToolRegistry()

        def add(a: int, b: int) -> int:
            return a + b

        registry.register(
            "add",
            "Add two numbers",
            add,
            {
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"},
                },
                "required": ["a", "b"],
            },
        )

        result = registry.execute_tool("add", {"a": 2, "b": 3})
        assert result == 5

    def test_get_tools_for_llm(self):
        """Test getting tools in LLM format."""
        registry = ToolRegistry()

        def dummy_func():
            return 42

        registry.register("test", "Test tool", dummy_func, {"type": "object"})

        tools = registry.get_tools_for_llm()
        assert len(tools) == 1
        assert tools[0]["name"] == "test"


class TestAgent:
    """Tests for agent."""

    def test_agent_init(self):
        """Test agent initialization."""
        mock_llm = Mock(spec=BaseLLMProvider)
        registry = ToolRegistry()

        agent = Agent(mock_llm, registry)

        assert agent.llm == mock_llm
        assert agent.tools == registry

    def test_agent_run_simple(self):
        """Test agent run with simple response."""
        mock_llm = Mock(spec=BaseLLMProvider)
        registry = ToolRegistry()

        # Mock LLM response
        response = LLMResponse(
            content="Done!",
            tool_calls=[],
            stop_reason="end_turn",
        )
        mock_llm.chat.return_value = response

        agent = Agent(mock_llm, registry)
        result = agent.run("Hello")

        assert result == "Done!"

    def test_agent_run_with_tool_call(self):
        """Test agent run with tool execution."""
        mock_llm = Mock(spec=BaseLLMProvider)
        registry = ToolRegistry()

        # Register a tool
        def get_answer():
            return 42

        registry.register("answer", "Get answer", get_answer, {})

        # Mock LLM responses
        tool_response = LLMResponse(
            content="",
            tool_calls=[ToolCall(id="1", name="answer", arguments={})],
            stop_reason="tool_use",
        )
        final_response = LLMResponse(
            content="The answer is 42",
            tool_calls=[],
            stop_reason="end_turn",
        )

        mock_llm.chat.side_effect = [tool_response, final_response]

        agent = Agent(mock_llm, registry)
        result = agent.run("What is the answer?")

        assert "42" in result

    def test_agent_max_iterations(self):
        """Test agent respects max iterations."""
        mock_llm = Mock(spec=BaseLLMProvider)
        registry = ToolRegistry()

        # Register a dummy tool
        def dummy_tool():
            return "done"

        registry.register("dummy", "Dummy tool", dummy_tool, {})

        # Mock LLM to always return tool calls
        response = LLMResponse(
            content="",
            tool_calls=[ToolCall(id="1", name="dummy", arguments={})],
            stop_reason="tool_use",
        )
        mock_llm.chat.return_value = response

        agent = Agent(mock_llm, registry, max_iterations=2)
        result = agent.run("Test")

        assert "Maximum iterations" in result

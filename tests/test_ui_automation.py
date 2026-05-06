"""Tests for UI automation system."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from whendoes.ui_automation.extractor import UIElement, _get_control_type_name
from whendoes.agent.smart_ui_agent import SmartUIAgent, setup_ui_tools


class TestUIElement:
    """Tests for UIElement."""

    def test_ui_element_creation(self):
        """Test creating UI element."""
        element = UIElement(
            element_id="elem_1",
            name="Save Button",
            control_type="Button",
            automation_id="btn_save",
            is_enabled=True,
            is_visible=True,
            bounding_rect={"left": 0, "top": 0, "right": 100, "bottom": 50},
            patterns=["Invoke"],
        )

        assert element.element_id == "elem_1"
        assert element.name == "Save Button"
        assert element.control_type == "Button"
        assert "Invoke" in element.patterns

    def test_ui_element_to_dict(self):
        """Test converting element to dict."""
        element = UIElement(
            element_id="elem_1",
            name="Test",
            control_type="Button",
            automation_id="test",
            is_enabled=True,
            is_visible=True,
            bounding_rect={"left": 0, "top": 0, "right": 100, "bottom": 50},
        )

        element_dict = element.to_dict()

        assert element_dict["id"] == "elem_1"
        assert element_dict["name"] == "Test"
        assert element_dict["type"] == "Button"

    def test_ui_element_with_children(self):
        """Test element with children."""
        child = UIElement(
            element_id="elem_2",
            name="Child",
            control_type="Text",
            automation_id="child",
            is_enabled=True,
            is_visible=True,
            bounding_rect={"left": 0, "top": 0, "right": 50, "bottom": 25},
        )

        parent = UIElement(
            element_id="elem_1",
            name="Parent",
            control_type="Pane",
            automation_id="parent",
            is_enabled=True,
            is_visible=True,
            bounding_rect={"left": 0, "top": 0, "right": 100, "bottom": 50},
            children=[child],
        )

        assert len(parent.children) == 1
        assert parent.children[0].name == "Child"


class TestSmartUIAgent:
    """Tests for SmartUIAgent."""

    def test_agent_initialization(self):
        """Test agent initialization."""
        mock_llm = Mock()
        tools = setup_ui_tools()

        agent = SmartUIAgent(mock_llm, tools)

        assert agent.llm == mock_llm
        assert agent.tools == tools
        assert agent.max_iterations == 10

    def test_ui_tools_setup(self):
        """Test UI tools are properly set up."""
        tools = setup_ui_tools()

        # Check that all UI tools are registered
        tool_names = [tool.name for tool in tools.get_all_tools()]

        expected_tools = [
            "click_element",
            "type_text",
            "get_element_value",
            "invoke_pattern",
            "select_item",
            "toggle_element",
            "expand_element",
        ]

        for tool_name in expected_tools:
            assert tool_name in tool_names, f"Tool {tool_name} not found"

    def test_ui_tools_have_correct_parameters(self):
        """Test UI tools have correct parameters."""
        tools = setup_ui_tools()

        # Check click_element tool
        click_tool = tools.get_tool("click_element")
        assert click_tool is not None
        params = click_tool.parameters
        assert "window_title" in params["properties"]
        assert "element_id" in params["properties"]

        # Check type_text tool
        type_tool = tools.get_tool("type_text")
        assert type_tool is not None
        params = type_tool.parameters
        assert "window_title" in params["properties"]
        assert "element_id" in params["properties"]
        assert "text" in params["properties"]

    def test_system_prompt_generation(self):
        """Test system prompt is generated correctly."""
        mock_llm = Mock()
        tools = setup_ui_tools()

        agent = SmartUIAgent(mock_llm, tools)
        prompt = agent._get_ui_system_prompt()

        assert "UI" in prompt or "واجهة" in prompt
        assert "element" in prompt.lower() or "عنصر" in prompt
        assert len(prompt) > 100

    @patch("whendoes.ui_automation.extractor.get_window_ui_context")
    def test_interact_with_window_simple(self, mock_get_context):
        """Test simple window interaction."""
        from whendoes.llm.base import LLMResponse

        mock_llm = Mock()
        tools = setup_ui_tools()

        # Mock UI context
        mock_get_context.return_value = '{"window": "Test", "elements": []}'

        # Mock LLM response
        response = LLMResponse(
            content="Done",
            tool_calls=[],
            stop_reason="end_turn",
        )
        mock_llm.chat.return_value = response

        agent = SmartUIAgent(mock_llm, tools)
        result = agent.interact_with_window("TestApp", "Do something")

        assert result == "Done"
        mock_get_context.assert_called_once()


class TestUIToolsIntegration:
    """Integration tests for UI tools."""

    def test_all_ui_tools_callable(self):
        """Test all UI tools are callable."""
        tools = setup_ui_tools()

        for tool in tools.get_all_tools():
            assert callable(tool.func), f"Tool {tool.name} is not callable"

    def test_ui_tools_have_descriptions(self):
        """Test all UI tools have descriptions."""
        tools = setup_ui_tools()

        for tool in tools.get_all_tools():
            assert tool.description, f"Tool {tool.name} has no description"
            assert len(tool.description) > 0

    def test_ui_tools_have_parameters(self):
        """Test all UI tools have parameter definitions."""
        tools = setup_ui_tools()

        for tool in tools.get_all_tools():
            assert tool.parameters, f"Tool {tool.name} has no parameters"
            assert "type" in tool.parameters
            assert "properties" in tool.parameters


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

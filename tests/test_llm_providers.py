"""Tests for LLM providers."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from whendoes.llm.base import Message, ToolCall, LLMResponse
from whendoes.llm.anthropic_provider import AnthropicProvider
from whendoes.llm.openai_provider import OpenAIProvider
from whendoes.llm.groq_provider import GroqProvider


class TestAnthropicProvider:
    """Tests for Anthropic provider."""

    @patch("whendoes.llm.anthropic_provider.Anthropic")
    def test_init(self, mock_anthropic):
        """Test provider initialization."""
        provider = AnthropicProvider(api_key="test-key", model="claude-3-sonnet")
        assert provider.api_key == "test-key"
        assert provider.model == "claude-3-sonnet"

    @patch("whendoes.llm.anthropic_provider.Anthropic")
    def test_chat_simple(self, mock_anthropic):
        """Test simple chat without tools."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        # Mock response
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Hello!")]
        mock_response.stop_reason = "end_turn"
        mock_client.messages.create.return_value = mock_response

        provider = AnthropicProvider(api_key="test-key")
        messages = [Message(role="user", content="Hello")]

        response = provider.chat(messages)

        assert response.content == "Hello!"
        assert response.stop_reason == "end_turn"
        assert len(response.tool_calls) == 0

    @patch("whendoes.llm.anthropic_provider.Anthropic")
    def test_chat_with_tools(self, mock_anthropic):
        """Test chat with tool calls."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        # Mock response with tool call
        mock_tool_use = MagicMock()
        mock_tool_use.type = "tool_use"
        mock_tool_use.id = "tool-1"
        mock_tool_use.name = "list_windows"
        mock_tool_use.input = {}

        mock_text = MagicMock()
        mock_text.text = "Calling tool"

        mock_response = MagicMock()
        mock_response.content = [mock_text, mock_tool_use]
        mock_response.stop_reason = "tool_use"
        mock_client.messages.create.return_value = mock_response

        provider = AnthropicProvider(api_key="test-key")
        messages = [Message(role="user", content="List windows")]
        tools = [{"name": "list_windows", "description": "List windows"}]

        response = provider.chat(messages, tools=tools)

        assert len(response.tool_calls) == 1
        assert response.tool_calls[0].name == "list_windows"


class TestOpenAIProvider:
    """Tests for OpenAI provider."""

    @patch("whendoes.llm.openai_provider.OpenAI")
    def test_init(self, mock_openai):
        """Test provider initialization."""
        provider = OpenAIProvider(api_key="test-key", model="gpt-4")
        assert provider.api_key == "test-key"
        assert provider.model == "gpt-4"

    @patch("whendoes.llm.openai_provider.OpenAI")
    def test_chat_simple(self, mock_openai):
        """Test simple chat."""
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        # Mock response
        mock_choice = MagicMock()
        mock_choice.message.content = "Hello!"
        mock_choice.message.tool_calls = None
        mock_choice.finish_reason = "stop"

        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response

        provider = OpenAIProvider(api_key="test-key")
        messages = [Message(role="user", content="Hello")]

        response = provider.chat(messages)

        assert response.content == "Hello!"


class TestGroqProvider:
    """Tests for Groq provider."""

    @patch("whendoes.llm.groq_provider.Groq")
    def test_init(self, mock_groq):
        """Test provider initialization."""
        provider = GroqProvider(api_key="test-key")
        assert provider.api_key == "test-key"
        assert provider.model == "mixtral-8x7b-32768"

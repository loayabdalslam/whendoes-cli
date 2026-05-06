"""Base LLM provider interface."""

from abc import ABC, abstractmethod
from typing import Any, Optional
from dataclasses import dataclass


@dataclass
class Message:
    """Chat message."""

    role: str  # "user" or "assistant"
    content: str
    tool_call_id: Optional[str] = None  # For tool messages


@dataclass
class ToolCall:
    """Tool call from LLM."""

    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class LLMResponse:
    """Response from LLM."""

    content: str
    tool_calls: list[ToolCall]
    stop_reason: str  # "end_turn", "tool_use", etc.


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "default",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        base_url: Optional[str] = None,
    ):
        """Initialize LLM provider.

        Args:
            api_key: API key for the provider
            model: Model name
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            base_url: Base URL for API (optional)
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.base_url = base_url

    @abstractmethod
    def chat(
        self,
        messages: list[Message],
        tools: Optional[list[dict[str, Any]]] = None,
        system: Optional[str] = None,
    ) -> LLMResponse:
        """Send chat message to LLM.

        Args:
            messages: List of messages
            tools: List of available tools (OpenAI format)
            system: System prompt

        Returns:
            LLMResponse with content and tool calls
        """
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """Validate provider configuration.

        Returns:
            True if configuration is valid
        """
        pass

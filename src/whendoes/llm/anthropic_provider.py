"""Anthropic provider implementation."""

import json
from typing import Any, Optional
from whendoes.llm.base import BaseLLMProvider, Message, LLMResponse, ToolCall

try:
    from anthropic import Anthropic
except ImportError:
    raise ImportError("anthropic package required: pip install anthropic")


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude provider."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-5-sonnet-20241022",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs,
    ):
        """Initialize Anthropic provider."""
        super().__init__(api_key, model, temperature, max_tokens)
        self.client = Anthropic(api_key=api_key)

    def chat(
        self,
        messages: list[Message],
        tools: Optional[list[dict[str, Any]]] = None,
        system: Optional[str] = None,
    ) -> LLMResponse:
        """Send chat message to Claude."""
        # Convert messages to Anthropic format
        anthropic_messages = []
        for msg in messages:
            if msg.role == "tool":
                # Tool messages need tool_use_id
                anthropic_messages.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": msg.tool_call_id,
                                "content": msg.content,
                            }
                        ],
                    }
                )
            else:
                # Regular messages
                anthropic_messages.append(
                    {
                        "role": msg.role,
                        "content": msg.content,
                    }
                )

        # Prepare request
        kwargs = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": anthropic_messages,
        }

        if system:
            kwargs["system"] = system

        if tools:
            kwargs["tools"] = tools

        # Call API
        response = self.client.messages.create(**kwargs)

        # Parse response
        content = ""
        tool_calls = []

        for block in response.content:
            if hasattr(block, "text"):
                content = block.text
            elif block.type == "tool_use":
                tool_calls.append(
                    ToolCall(
                        id=block.id,
                        name=block.name,
                        arguments=block.input,
                    )
                )

        return LLMResponse(
            content=content,
            tool_calls=tool_calls,
            stop_reason=response.stop_reason,
        )

    def validate_config(self) -> bool:
        """Validate Anthropic configuration."""
        if not self.api_key:
            return False
        try:
            self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": "test"}],
            )
            return True
        except Exception:
            return False

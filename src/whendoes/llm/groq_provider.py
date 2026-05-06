"""Groq provider implementation."""

import json
from typing import Any, Optional
from whendoes.llm.base import BaseLLMProvider, Message, LLMResponse, ToolCall

try:
    from groq import Groq
except ImportError:
    raise ImportError("groq package required: pip install groq")


class GroqProvider(BaseLLMProvider):
    """Groq API provider."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "mixtral-8x7b-32768",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs,
    ):
        """Initialize Groq provider."""
        super().__init__(api_key, model, temperature, max_tokens)
        self.client = Groq(api_key=api_key)

    def chat(
        self,
        messages: list[Message],
        tools: Optional[list[dict[str, Any]]] = None,
        system: Optional[str] = None,
    ) -> LLMResponse:
        """Send chat message to Groq."""
        # Convert messages to Groq format
        groq_messages = []
        for msg in messages:
            if msg.role == "tool":
                # Tool messages need tool_call_id
                groq_messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": msg.tool_call_id,
                        "content": msg.content,
                    }
                )
            else:
                # Regular messages
                groq_messages.append(
                    {
                        "role": msg.role,
                        "content": msg.content,
                    }
                )

        # Add system message if provided
        if system:
            groq_messages.insert(0, {"role": "system", "content": system})

        # Prepare request
        kwargs = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": groq_messages,
        }

        if tools:
            kwargs["tools"] = [{"type": "function", "function": tool} for tool in tools]

        # Call API
        response = self.client.chat.completions.create(**kwargs)

        # Parse response
        content = ""
        tool_calls = []

        for choice in response.choices:
            if choice.message.content:
                content = choice.message.content

            if hasattr(choice.message, "tool_calls") and choice.message.tool_calls:
                for tool_call in choice.message.tool_calls:
                    tool_calls.append(
                        ToolCall(
                            id=tool_call.id,
                            name=tool_call.function.name,
                            arguments=json.loads(tool_call.function.arguments),
                        )
                    )

        return LLMResponse(
            content=content,
            tool_calls=tool_calls,
            stop_reason=response.choices[0].finish_reason or "end_turn",
        )

    def validate_config(self) -> bool:
        """Validate Groq configuration."""
        if not self.api_key:
            return False
        try:
            self.client.chat.completions.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": "test"}],
            )
            return True
        except Exception:
            return False

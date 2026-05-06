"""OpenAI provider implementation."""

import json
from typing import Any, Optional
from whendoes.llm.base import BaseLLMProvider, Message, LLMResponse, ToolCall

try:
    from openai import OpenAI
except ImportError:
    raise ImportError("openai package required: pip install openai")


class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT provider."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4-turbo",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs,
    ):
        """Initialize OpenAI provider."""
        super().__init__(api_key, model, temperature, max_tokens)
        self.client = OpenAI(api_key=api_key)

    def chat(
        self,
        messages: list[Message],
        tools: Optional[list[dict[str, Any]]] = None,
        system: Optional[str] = None,
    ) -> LLMResponse:
        """Send chat message to OpenAI."""
        # Convert messages to OpenAI format
        openai_messages = []
        for msg in messages:
            if msg.role == "tool":
                # Tool messages need tool_call_id
                openai_messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": msg.tool_call_id,
                        "content": msg.content,
                    }
                )
            else:
                # Regular messages
                openai_messages.append(
                    {
                        "role": msg.role,
                        "content": msg.content,
                    }
                )

        # Add system message if provided
        if system:
            openai_messages.insert(0, {"role": "system", "content": system})

        # Prepare request
        kwargs = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": openai_messages,
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

            if choice.message.tool_calls:
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
        """Validate OpenAI configuration."""
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

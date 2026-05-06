"""Ollama provider implementation."""

import json
from typing import Any, Optional
from whendoes.llm.base import BaseLLMProvider, Message, LLMResponse, ToolCall

try:
    import requests
except ImportError:
    raise ImportError("requests package required: pip install requests")


class OllamaProvider(BaseLLMProvider):
    """Ollama local LLM provider."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "llama2",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        base_url: str = "http://localhost:11434",
        **kwargs,
    ):
        """Initialize Ollama provider."""
        super().__init__(api_key, model, temperature, max_tokens, base_url)
        self.base_url = base_url.rstrip("/")

    def chat(
        self,
        messages: list[Message],
        tools: Optional[list[dict[str, Any]]] = None,
        system: Optional[str] = None,
    ) -> LLMResponse:
        """Send chat message to Ollama."""
        # Convert messages to Ollama format
        ollama_messages = [
            {"role": msg.role, "content": msg.content} for msg in messages
        ]

        # Prepare request
        payload = {
            "model": self.model,
            "messages": ollama_messages,
            "temperature": self.temperature,
            "stream": False,
        }

        if system:
            payload["system"] = system

        # Call API
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=300,
            )
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            raise RuntimeError(f"Ollama API error: {e}")

        # Parse response
        content = data.get("message", {}).get("content", "")
        tool_calls = []

        # Ollama doesn't natively support tool calling, so we parse from content
        # This is a simplified implementation
        if tools and "```json" in content:
            try:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                if json_end > json_start:
                    tool_data = json.loads(content[json_start:json_end])
                    if "tool_calls" in tool_data:
                        for tc in tool_data["tool_calls"]:
                            tool_calls.append(
                                ToolCall(
                                    id=tc.get("id", ""),
                                    name=tc.get("name", ""),
                                    arguments=tc.get("arguments", {}),
                                )
                            )
            except json.JSONDecodeError:
                pass

        return LLMResponse(
            content=content,
            tool_calls=tool_calls,
            stop_reason="end_turn",
        )

    def validate_config(self) -> bool:
        """Validate Ollama configuration."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

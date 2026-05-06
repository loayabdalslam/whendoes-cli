"""Google Gemini provider implementation."""

import json
from typing import Any, Optional
from whendoes.llm.base import BaseLLMProvider, Message, LLMResponse, ToolCall

try:
    import google.generativeai as genai
except ImportError:
    raise ImportError("google-generativeai package required: pip install google-generativeai")


class GeminiProvider(BaseLLMProvider):
    """Google Gemini provider."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-1.5-pro",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs,
    ):
        """Initialize Gemini provider."""
        super().__init__(api_key, model, temperature, max_tokens)
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(model)

    def chat(
        self,
        messages: list[Message],
        tools: Optional[list[dict[str, Any]]] = None,
        system: Optional[str] = None,
    ) -> LLMResponse:
        """Send chat message to Gemini."""
        # Convert messages to Gemini format
        gemini_messages = []
        for msg in messages:
            gemini_messages.append({"role": msg.role, "parts": [msg.content]})

        # Prepare system instruction
        system_instruction = system or ""

        # Prepare tools if provided
        tool_config = None
        if tools:
            tool_config = genai.types.Tool(
                function_declarations=[
                    genai.types.FunctionDeclaration(
                        name=tool["name"],
                        description=tool.get("description", ""),
                        parameters=genai.types.Schema(
                            type=genai.types.Type.OBJECT,
                            properties={
                                k: genai.types.Schema(
                                    type=genai.types.Type.STRING,
                                    description=v.get("description", ""),
                                )
                                for k, v in tool.get("parameters", {})
                                .get("properties", {})
                                .items()
                            },
                            required=tool.get("parameters", {}).get("required", []),
                        ),
                    )
                    for tool in tools
                ]
            )

        # Call API
        response = self.client.generate_content(
            gemini_messages,
            generation_config=genai.types.GenerationConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
            ),
            tools=[tool_config] if tool_config else None,
            system_instruction=system_instruction,
        )

        # Parse response
        content = ""
        tool_calls = []

        if response.text:
            content = response.text

        # Handle function calls if present
        if hasattr(response, "candidates") and response.candidates:
            for candidate in response.candidates:
                if hasattr(candidate.content, "parts"):
                    for part in candidate.content.parts:
                        if hasattr(part, "function_call"):
                            tool_calls.append(
                                ToolCall(
                                    id=part.function_call.name,
                                    name=part.function_call.name,
                                    arguments=dict(part.function_call.args),
                                )
                            )

        return LLMResponse(
            content=content,
            tool_calls=tool_calls,
            stop_reason="end_turn",
        )

    def validate_config(self) -> bool:
        """Validate Gemini configuration."""
        if not self.api_key:
            return False
        try:
            self.client.generate_content("test")
            return True
        except Exception:
            return False

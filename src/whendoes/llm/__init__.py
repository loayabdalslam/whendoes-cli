"""LLM provider factory."""

from typing import Optional
from whendoes.llm.base import BaseLLMProvider
from whendoes.llm.anthropic_provider import AnthropicProvider
from whendoes.llm.openai_provider import OpenAIProvider
from whendoes.llm.groq_provider import GroqProvider
from whendoes.llm.gemini_provider import GeminiProvider
from whendoes.llm.openrouter_provider import OpenRouterProvider
from whendoes.llm.ollama_provider import OllamaProvider


def create_provider(
    provider_name: str,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    base_url: Optional[str] = None,
) -> BaseLLMProvider:
    """Create LLM provider instance.

    Args:
        provider_name: Provider name (openai, anthropic, groq, gemini, openrouter, ollama)
        api_key: API key for the provider
        model: Model name
        temperature: Temperature for generation
        max_tokens: Maximum tokens to generate
        base_url: Base URL for API (optional)

    Returns:
        LLM provider instance

    Raises:
        ValueError: If provider name is not recognized
    """
    provider_map = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "groq": GroqProvider,
        "gemini": GeminiProvider,
        "openrouter": OpenRouterProvider,
        "ollama": OllamaProvider,
    }

    if provider_name not in provider_map:
        raise ValueError(
            f"Unknown provider: {provider_name}. "
            f"Available: {', '.join(provider_map.keys())}"
        )

    provider_class = provider_map[provider_name]

    kwargs = {
        "api_key": api_key,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    if model:
        kwargs["model"] = model

    if base_url:
        kwargs["base_url"] = base_url

    return provider_class(**kwargs)

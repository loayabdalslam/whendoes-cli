"""Tests for configuration."""

import pytest
from whendoes.config import LLMConfig, AgentConfig, CLIConfig, Config, get_config


class TestLLMConfig:
    """Tests for LLM configuration."""

    def test_default_config(self):
        """Test default LLM config."""
        config = LLMConfig()
        assert config.provider == "anthropic"
        assert config.temperature == 0.7
        assert config.max_tokens == 2048

    def test_custom_config(self):
        """Test custom LLM config."""
        config = LLMConfig(
            provider="openai",
            model="gpt-4",
            temperature=0.5,
            max_tokens=4096,
        )
        assert config.provider == "openai"
        assert config.model == "gpt-4"
        assert config.temperature == 0.5
        assert config.max_tokens == 4096


class TestAgentConfig:
    """Tests for agent configuration."""

    def test_default_config(self):
        """Test default agent config."""
        config = AgentConfig()
        assert config.max_iterations == 10
        assert config.require_approval is True
        assert config.verbose is False


class TestCLIConfig:
    """Tests for CLI configuration."""

    def test_default_config(self):
        """Test default CLI config."""
        config = CLIConfig()
        assert config.debug is False
        assert config.max_history == 1000


class TestMainConfig:
    """Tests for main configuration."""

    def test_config_structure(self):
        """Test main config structure."""
        config = Config()
        assert isinstance(config.llm, LLMConfig)
        assert isinstance(config.agent, AgentConfig)
        assert isinstance(config.cli, CLIConfig)

import os
from pathlib import Path
from typing import Literal, Optional
from pydantic import BaseModel, Field, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv, find_dotenv

# Load .env file - search in current working directory first, then in package root
cwd_env = Path.cwd() / ".env"
if cwd_env.exists():
    load_dotenv(cwd_env)
else:
    # Fallback to package root
    package_env = Path(__file__).parent.parent.parent.parent / ".env"
    if package_env.exists():
        load_dotenv(package_env)
    else:
        # Last resort - use find_dotenv
        load_dotenv(find_dotenv())


class LLMConfig(BaseModel):
    """LLM provider configuration."""
    provider: str
    model: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2048


class AgentConfig(BaseModel):
    """Agent configuration."""
    max_iterations: int = 10
    timeout: int = 300
    require_approval: bool = True
    verbose: bool = False


class CLIConfig(BaseModel):
    """CLI configuration."""
    debug: bool = False
    history_file: str = ".whendoes_history"
    max_history: int = 1000


class Config(BaseSettings):
    """Main configuration - Flat for environment variable mapping."""

    # LLM Settings
    llm_provider: str = Field(
        default="groq",
        validation_alias=AliasChoices("LLM_PROVIDER", "llm_provider"),
    )
    llm_model: str = Field(
        default="qwen/qwen3-32b",
        validation_alias=AliasChoices("LLM_MODEL", "llm_model"),
    )
    llm_api_key: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("LLM_API_KEY", "llm_api_key", "GROQ_API_KEY", "ANTHROPIC_API_KEY", "OPENAI_API_KEY"),
    )
    llm_base_url: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("LLM_BASE_URL", "llm_base_url"),
    )
    llm_temperature: float = Field(
        default=0.7,
        validation_alias=AliasChoices("LLM_TEMPERATURE", "llm_temperature"),
    )
    llm_max_tokens: int = Field(
        default=2048,
        validation_alias=AliasChoices("LLM_MAX_TOKENS", "llm_max_tokens"),
    )

    # Agent Settings
    agent_max_iterations: int = Field(
        default=10,
        validation_alias=AliasChoices("AGENT_MAX_ITERATIONS", "agent_max_iterations"),
    )
    agent_timeout: int = Field(
        default=300,
        validation_alias=AliasChoices("AGENT_TIMEOUT", "agent_timeout"),
    )
    agent_require_approval: bool = Field(
        default=True,
        validation_alias=AliasChoices("AGENT_REQUIRE_APPROVAL", "agent_require_approval"),
    )
    agent_verbose: bool = Field(
        default=False,
        validation_alias=AliasChoices("AGENT_VERBOSE", "agent_verbose"),
    )

    # CLI Settings
    cli_debug: bool = Field(
        default=False,
        validation_alias=AliasChoices("CLI_DEBUG", "cli_debug"),
    )
    cli_history_file: str = Field(
        default=".whendoes_history",
        validation_alias=AliasChoices("CLI_HISTORY_FILE", "cli_history_file"),
    )
    cli_max_history: int = Field(
        default=1000,
        validation_alias=AliasChoices("CLI_MAX_HISTORY", "cli_max_history"),
    )

    model_config = SettingsConfigDict(
        env_file=str(Path.cwd() / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def llm(self) -> LLMConfig:
        return LLMConfig(
            provider=self.llm_provider,
            model=self.llm_model,
            api_key=self.llm_api_key,
            base_url=self.llm_base_url,
            temperature=self.llm_temperature,
            max_tokens=self.llm_max_tokens,
        )

    @property
    def agent(self) -> AgentConfig:
        return AgentConfig(
            max_iterations=self.agent_max_iterations,
            timeout=self.agent_timeout,
            require_approval=self.agent_require_approval,
            verbose=self.agent_verbose,
        )

    @property
    def cli(self) -> CLIConfig:
        return CLIConfig(
            debug=self.cli_debug,
            history_file=self.cli_history_file,
            max_history=self.cli_max_history,
        )


def get_config() -> Config:
    """Get configuration instance."""
    return Config()

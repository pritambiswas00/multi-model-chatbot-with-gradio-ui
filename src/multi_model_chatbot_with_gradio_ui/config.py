"""Application configuration loaded from the environment."""
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Application configuration loaded from environment variables or ``.env``.

    Attributes:
        anthropic_api_key: Anthropic API key, read from ``ANTHROPIC_API_KEY``
            (case-insensitive). Must start with ``sk-ant``; a missing or
            malformed value raises a ``ValidationError`` on instantiation.
    """
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")
    anthropic_api_key: str = Field(description="API key for Anthropic", pattern="^sk-ant.*$")
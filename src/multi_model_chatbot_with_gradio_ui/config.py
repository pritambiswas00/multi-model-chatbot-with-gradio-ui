from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Application configuration loaded from environment variables."""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")
    anthropic_api_key: str = Field(description="API key for Anthropic", pattern="^sk-ant.*$")
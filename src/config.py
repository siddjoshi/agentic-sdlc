"""Application configuration loaded from environment variables via pydantic-settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Central configuration for the learning platform.

    All values are read from environment variables.
    Required variables must be set before the application starts.
    """

    # API authentication
    api_key: str = Field(..., description="Expected value for X-API-Key header")

    # GitHub Models API
    github_models_api_key: str = Field(..., description="Auth token for GitHub Models API")
    github_models_endpoint: str = Field(..., description="Base URL for GitHub Models API")
    github_models_model: str = Field(default="gpt-4o", description="Model name for chat completions")

    # AI request tuning
    ai_request_timeout: int = Field(default=30, description="Timeout in seconds for AI API requests")
    ai_max_retries: int = Field(default=3, description="Max retry attempts for transient failures")
    ai_initial_backoff: float = Field(default=1.0, description="Initial backoff delay in seconds")
    ai_max_backoff: float = Field(default=30.0, description="Maximum backoff delay in seconds")
    ai_backoff_jitter: int = Field(default=500, description="Jitter range in ms (±)")
    lesson_max_tokens: int = Field(default=2000, description="Max tokens for lesson generation")
    quiz_max_tokens: int = Field(default=1500, description="Max tokens for quiz generation")

    # Prompt templates
    prompts_dir: str = Field(default="prompts", description="Path to prompt templates directory")

    # Database
    database_url: str = Field(default="data/learning_platform.db", description="SQLite database file path")

    # Application
    cors_origins: str = Field(default="http://localhost:8000", description="Comma-separated CORS origins")
    log_level: str = Field(default="INFO", description="Logging level")
    app_version: str = Field(default="1.0.0", description="Application version")

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    """Return a cached singleton Settings instance."""
    return Settings()

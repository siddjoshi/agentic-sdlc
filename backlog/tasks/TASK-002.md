# Task: Implement Configuration with Pydantic Settings

| Field        | Value                |
|--------------|----------------------|
| **Task ID**  | TASK-002             |
| **Story**    | STORY-001            |
| **Status**   | To Do                |
| **Assignee** | develop-agent        |
| **Estimate** | 1h                   |

## Description

Create a `Settings` class using Pydantic Settings that loads all configuration from environment variables. This centralizes config access and ensures the API key is never hardcoded.

## Implementation Details

**Files to create/modify:**
- `src/config.py` — Settings class with all env vars

**Approach:**
Use `pydantic_settings.BaseSettings` to define a Settings class with these fields:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Authentication
    api_key: str  # For X-API-Key header validation

    # GitHub Models API
    github_models_api_key: str  # GITHUB_MODELS_API_KEY
    github_models_endpoint: str  # GITHUB_MODELS_ENDPOINT
    github_models_model: str = "gpt-4o"

    # AI Configuration
    ai_request_timeout: int = 30
    ai_max_retries: int = 3
    ai_initial_backoff: float = 1.0
    ai_max_backoff: float = 30.0
    ai_backoff_jitter: int = 500
    lesson_max_tokens: int = 2000
    quiz_max_tokens: int = 1500
    prompts_dir: str = "prompts"

    # Database
    database_url: str = "data/learning_platform.db"

    # App
    app_version: str = "1.0.0"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
```

Create a module-level `get_settings()` function with `@lru_cache` for singleton access.

## API Changes

N/A

## Data Model Changes

N/A

## Acceptance Criteria

- [ ] Settings class loads all required env vars
- [ ] Missing required env vars raise a clear validation error at startup
- [ ] Default values work for optional settings
- [ ] `get_settings()` returns a cached singleton instance

## Test Requirements

- **Unit tests:** Test Settings with mock env vars; test defaults; test missing required vars raise error
- **Integration tests:** N/A
- **Edge cases:** Missing GITHUB_MODELS_API_KEY raises clear error

## Parent References

| Ref Type | ID               |
|----------|------------------|
| Story    | STORY-001        |
| Epic     | EPIC-004         |
| BRD      | BRD-NFR-003      |

## Definition of Done

- [ ] Code written and follows project conventions
- [ ] All tests passing (`pytest`)
- [ ] No linting errors
- [ ] PR opened and reviewed
- [ ] Acceptance criteria verified

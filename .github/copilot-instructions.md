# Copilot Instructions — Agentic SDLC Learning Platform

## Project Overview

AI-powered learning platform for GitHub training (Actions, Copilot, Advanced Security).
The platform uses GitHub Models for AI content generation and FastAPI for the backend.
The SDLC is driven by 6 custom Copilot agents that chain together to produce
requirements, design, implementation, testing, and deployment artifacts.

## Tech Stack & Conventions

- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Data Models**: Pydantic v2
- **Testing**: pytest
- **AI Backend**: GitHub Models API (GPT-4o)
- **Project Structure**:
  - `src/` — application source code
  - `tests/` — test suite
  - `docs/` — SDLC artifacts (requirements/, design/, testing/)
  - `templates/` — SDLC document templates
  - `backlog/` — work items (epics/, stories/, tasks/)

## Coding Standards

- Use type hints on all function signatures and variables where non-obvious.
- Define request/response schemas as Pydantic models (never raw dicts).
- Use `async def` for I/O-bound endpoints; sync is fine for pure computation.
- Raise `fastapi.HTTPException` with appropriate status codes for error handling.
- Load configuration from environment variables — never hardcode secrets.
- Add docstrings to all public functions and classes.
- Keep functions small and single-purpose.

## Agent Workflow Rules

- SDLC document templates live in `templates/` — always start from a template.
- Generated artifacts go under `docs/`:
  - `docs/requirements/` — BRD, functional specs
  - `docs/design/` — architecture, API design, data models
  - `docs/testing/` — test plans, test cases
- Backlog items go under `backlog/`:
  - `backlog/epics/` — high-level features
  - `backlog/stories/` — user stories
  - `backlog/tasks/` — implementation tasks
- Every artifact **must** trace back to a BRD requirement ID (`BRD-xxx`).
- Update `docs/change-log.md` when making key decisions or significant changes.

## GitHub Models Integration

- **Auth**: Use environment variable `GITHUB_MODELS_API_KEY`.
- **Endpoint**: Configured via environment variable `GITHUB_MODELS_ENDPOINT`.
- **Preferred model**: GPT-4o for content generation tasks.
- Always handle rate limits with exponential backoff.
- Wrap API calls in try/except and return meaningful error responses.
- Never log or expose API keys in output or error messages.

## Do / Avoid

### Do

- Use templates from `templates/` for all SDLC documents.
- Maintain requirement ID traceability (`BRD-xxx`) across all artifacts.
- Write tests for every new endpoint and service function.
- Keep dependencies minimal and justified.

### Avoid

- Hardcoding API keys, secrets, or environment-specific values.
- Adding complexity beyond MVP scope — keep it simple.
- Introducing frameworks or libraries not needed for the MVP.
- Committing generated credentials or `.env` files.
- Skipping error handling on external API calls.

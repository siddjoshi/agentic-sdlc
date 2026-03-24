# Story: Project Scaffolding & Configuration

| Field        | Value                |
|--------------|----------------------|
| **Story ID** | STORY-001            |
| **Epic**     | EPIC-004             |
| **Status**   | Draft                |
| **Assignee** | develop-agent        |
| **Estimate** | M                    |
| **Priority** | P0                   |

## User Story

**As a** developer,
**I want** a well-structured FastAPI project with configuration management,
**so that** all other features can be built on a solid, consistent foundation.

## Acceptance Criteria

1. **Given** the project directory,
   **When** I run `uvicorn src.main:app`,
   **Then** the FastAPI application starts on port 8000 without errors.

2. **Given** environment variables are set,
   **When** the app starts,
   **Then** configuration is loaded from env vars via a Pydantic Settings class.

3. **Given** the project structure,
   **When** I inspect the src/ directory,
   **Then** I see separate packages for routes, services, models, middleware, database, repositories, and ai.

## BRD & Design References

| BRD ID        | HLD/LLD Component                    |
|---------------|--------------------------------------|
| BRD-NFR-010   | COMP-001 — modular codebase          |
| BRD-NFR-003   | Config — env var management          |

## Tasks Breakdown

| Task ID    | Description                                      | Estimate |
|------------|--------------------------------------------------|----------|
| TASK-001   | Create project structure and requirements.txt     | 2h       |
| TASK-002   | Implement config.py with Pydantic Settings        | 1h       |
| TASK-003   | Create FastAPI app factory in main.py             | 2h       |

## UI/UX Notes

N/A — API only.

## Technical Notes

- **Stack:** Python / FastAPI / Uvicorn
- **Key considerations:** Use `create_app()` factory pattern with async lifespan context manager; config must read from env vars only
- **Configuration:** GITHUB_MODELS_API_KEY, GITHUB_MODELS_ENDPOINT, API_KEY, DATABASE_URL

## Dependencies

- None — this is the foundational story

## Definition of Done

- [ ] Code implements all acceptance criteria
- [ ] Unit and integration tests written and passing
- [ ] API documentation updated (if applicable)
- [ ] Code reviewed and approved
- [ ] No regressions in existing tests

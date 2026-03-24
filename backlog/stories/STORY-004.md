# Story: Error Handling & Request Logging

| Field        | Value                |
|--------------|----------------------|
| **Story ID** | STORY-004            |
| **Epic**     | EPIC-004             |
| **Status**   | Draft                |
| **Assignee** | develop-agent        |
| **Estimate** | M                    |
| **Priority** | P0                   |

## User Story

**As a** developer,
**I want** consistent error responses and request logging across all endpoints,
**so that** I can debug issues quickly and users receive clear, structured error messages.

## Acceptance Criteria

1. **Given** invalid input (e.g., non-integer course ID),
   **When** the request is processed,
   **Then** the server returns HTTP 422 with field-level error details.

2. **Given** a resource is not found (e.g., course ID 999),
   **When** the request is processed,
   **Then** the server returns HTTP 404 with {"error": {"code": "..._NOT_FOUND", "message": "..."}}.

3. **Given** any API request,
   **When** it is processed,
   **Then** method, path, status code, and response time are logged at INFO level.

4. **Given** a custom exception (e.g., AIServiceUnavailableError),
   **When** it is raised in a route handler,
   **Then** it is caught by an exception handler and returns the appropriate HTTP status and error body.

## BRD & Design References

| BRD ID        | HLD/LLD Component                       |
|---------------|-----------------------------------------|
| BRD-FR-012    | COMP-001 — input validation             |
| BRD-NFR-007   | COMP-001 — request logging              |
| BRD-NFR-009   | COMP-001 — Pydantic validation          |

## Tasks Breakdown

| Task ID    | Description                                          | Estimate |
|------------|------------------------------------------------------|----------|
| TASK-006   | Implement custom exceptions and exception handlers   | 2h       |
| TASK-007   | Implement request logging middleware                 | 1h       |

## UI/UX Notes

N/A — API only.

## Technical Notes

- **Stack:** Python / FastAPI exception handlers / logging
- **Key considerations:** Use FastAPI `@app.exception_handler()` for custom exceptions; use ASGI middleware for request logging with `time.time()` for latency measurement; never log API keys
- **Configuration:** Log level via LOG_LEVEL env var

## Dependencies

- STORY-001 (project scaffolding)

## Definition of Done

- [ ] Code implements all acceptance criteria
- [ ] Unit and integration tests written and passing
- [ ] API documentation updated (if applicable)
- [ ] Code reviewed and approved
- [ ] No regressions in existing tests

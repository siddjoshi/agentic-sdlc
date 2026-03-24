# Story: API Key Authentication Middleware

| Field        | Value                |
|--------------|----------------------|
| **Story ID** | STORY-002            |
| **Epic**     | EPIC-004             |
| **Status**   | Draft                |
| **Assignee** | develop-agent        |
| **Estimate** | S                    |
| **Priority** | P0                   |

## User Story

**As a** platform admin,
**I want** all API endpoints (except health) to require a valid API key,
**so that** unauthorized access to training data and AI features is prevented.

## Acceptance Criteria

1. **Given** a request without an X-API-Key header,
   **When** it hits any endpoint except /api/v1/health,
   **Then** the server returns HTTP 401 with {"error": {"code": "UNAUTHORIZED", "message": "Missing or invalid API key..."}}.

2. **Given** a request with an invalid X-API-Key header,
   **When** it hits a protected endpoint,
   **Then** the server returns HTTP 401.

3. **Given** a request to GET /api/v1/health,
   **When** no X-API-Key header is provided,
   **Then** the server returns HTTP 200 (health is exempt).

4. **Given** a request with a valid X-API-Key header,
   **When** it hits any protected endpoint,
   **Then** the request is forwarded to the route handler normally.

## BRD & Design References

| BRD ID        | HLD/LLD Component                                |
|---------------|--------------------------------------------------|
| BRD-FR-013    | COMP-001 — API key auth middleware               |
| BRD-NFR-004   | All endpoints except health require valid key    |
| BRD-NFR-003   | API key from env var, never logged               |

## Tasks Breakdown

| Task ID    | Description                                       | Estimate |
|------------|---------------------------------------------------|----------|
| TASK-004   | Implement API key authentication middleware        | 2h       |

## UI/UX Notes

N/A — API only.

## Technical Notes

- **Stack:** Python / FastAPI middleware
- **Key considerations:** Middleware checks `X-API-Key` header against `API_KEY` env var; health endpoint path excluded
- **Configuration:** API_KEY environment variable

## Dependencies

- STORY-001 (project scaffolding and config)

## Definition of Done

- [ ] Code implements all acceptance criteria
- [ ] Unit and integration tests written and passing
- [ ] API documentation updated (if applicable)
- [ ] Code reviewed and approved
- [ ] No regressions in existing tests

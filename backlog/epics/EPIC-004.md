# Epic: API Layer & Infrastructure Setup

| Field       | Value                |
|-------------|----------------------|
| **Epic ID** | EPIC-004             |
| **Status**  | Draft                |
| **Owner**   | epic-and-tasks-agent |
| **Created** | 2026-03-24           |
| **Target**  | Sprint 1             |

## Goal / Objective

Set up the FastAPI application skeleton with project configuration, dependency injection, API key authentication middleware, health check endpoint, structured error handling, request logging, and input validation — forming the foundation all other epics build upon.

## Business Value

The infrastructure layer ensures the platform is secure, observable, and well-structured from day one. API key authentication protects endpoints, structured logging enables troubleshooting, and the health check enables operational monitoring.

## BRD Requirements Mapped

| BRD ID       | Description                                               |
|--------------|-----------------------------------------------------------|
| BRD-FR-009   | GET /api/v1/health — system health check                  |
| BRD-FR-012   | Input validation with HTTP 422 for invalid input          |
| BRD-FR-013   | API key authentication via X-API-Key header               |
| BRD-NFR-003  | API key read from env var, never logged or exposed        |
| BRD-NFR-004  | All endpoints (except health) require valid API key       |
| BRD-NFR-007  | Log all API requests with method, path, status, time      |
| BRD-NFR-009  | Pydantic validation on all user-facing input              |
| BRD-NFR-010  | Modular codebase with separate routes/services/models     |

## Features

| Feature ID | Name                              | Priority (P0/P1/P2) | Status  |
|------------|-----------------------------------|----------------------|---------|
| FEAT-014   | Project Scaffolding & Config      | P0                   | Planned |
| FEAT-015   | API Key Auth Middleware           | P0                   | Planned |
| FEAT-016   | Health Check Endpoint             | P0                   | Planned |
| FEAT-017   | Error Handling & Validation       | P0                   | Planned |
| FEAT-018   | Request Logging Middleware        | P1                   | Planned |

## Acceptance Criteria

1. FastAPI application starts with `uvicorn src.main:app` and serves endpoints on port 8000
2. GET /api/v1/health returns {"status": "healthy", "version": "1.0.0", "database": "connected"} without auth
3. All endpoints except health return HTTP 401 when X-API-Key is missing or invalid
4. Invalid input returns HTTP 422 with descriptive field-level errors
5. All requests are logged with method, path, status code, and response time at INFO level
6. Configuration is loaded from environment variables via a Settings class
7. Project follows modular structure: routes/, services/, models/, middleware/, database/, repositories/

## Dependencies & Risks

**Dependencies:**
- Python 3.11+ with FastAPI, Uvicorn, Pydantic, aiosqlite packages
- Environment variables: API_KEY, GITHUB_MODELS_API_KEY, GITHUB_MODELS_ENDPOINT

**Risks:**
- Middleware ordering affects request processing — auth must run before route handlers
- Incorrect CORS configuration may block frontend requests

## Out of Scope

- OAuth / SSO / multi-factor authentication
- Cloud deployment configuration
- CI/CD pipeline setup
- Frontend static file serving (minimal, included as part of app factory)

## Definition of Done

- [ ] All stories in this epic are Done
- [ ] Acceptance criteria verified
- [ ] API endpoints documented
- [ ] No critical or high-severity bugs open
- [ ] Demo-ready for stakeholder review

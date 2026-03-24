# Task: Implement API Key Authentication Middleware

| Field        | Value                |
|--------------|----------------------|
| **Task ID**  | TASK-004             |
| **Story**    | STORY-002            |
| **Status**   | To Do                |
| **Assignee** | develop-agent        |
| **Estimate** | 2h                   |

## Description

Create ASGI middleware that validates the `X-API-Key` header on all requests except the health check endpoint. Invalid or missing keys return HTTP 401 with a structured error response.

## Implementation Details

**Files to create/modify:**
- `src/middleware/auth.py` — API key authentication middleware
- `src/main.py` — Register middleware in create_app()

**Approach:**
```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

class APIKeyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, api_key: str):
        super().__init__(app)
        self.api_key = api_key

    async def dispatch(self, request: Request, call_next):
        # Skip auth for health endpoint
        if request.url.path == "/api/v1/health":
            return await call_next(request)

        # Check X-API-Key header
        provided_key = request.headers.get("X-API-Key")
        if not provided_key or provided_key != self.api_key:
            return JSONResponse(
                status_code=401,
                content={"error": {"code": "UNAUTHORIZED", "message": "Missing or invalid API key. Provide a valid key in the X-API-Key header."}}
            )
        return await call_next(request)
```

Register in main.py: `app.add_middleware(APIKeyMiddleware, api_key=settings.api_key)`

## API Changes

N/A — this is cross-cutting middleware.

## Data Model Changes

N/A

## Acceptance Criteria

- [ ] Requests without X-API-Key header return 401 on protected endpoints
- [ ] Requests with invalid X-API-Key return 401
- [ ] Requests with valid X-API-Key are forwarded to route handlers
- [ ] GET /api/v1/health is exempt from authentication
- [ ] The 401 response body follows the ErrorResponse format
- [ ] The API key value is never logged

## Test Requirements

- **Unit tests:** Test middleware with mock request/response; test exempt path; test valid/invalid keys
- **Integration tests:** Test protected endpoints return 401 without key; test health returns 200 without key
- **Edge cases:** Empty X-API-Key header; extra whitespace in key

## Parent References

| Ref Type | ID               |
|----------|------------------|
| Story    | STORY-002        |
| Epic     | EPIC-004         |
| BRD      | BRD-FR-013, BRD-NFR-004 |

## Definition of Done

- [ ] Code written and follows project conventions
- [ ] All tests passing (`pytest`)
- [ ] No linting errors
- [ ] PR opened and reviewed
- [ ] Acceptance criteria verified

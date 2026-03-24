# Task: Implement Request Logging Middleware

| Field        | Value                |
|--------------|----------------------|
| **Task ID**  | TASK-007             |
| **Story**    | STORY-004            |
| **Status**   | To Do                |
| **Assignee** | develop-agent        |
| **Estimate** | 1h                   |

## Description

Create ASGI middleware that logs every API request with HTTP method, path, response status code, and response time in milliseconds at INFO level. Ensure API keys are never included in log output.

## Implementation Details

**Files to create/modify:**
- `src/middleware/logging.py` — Request logging middleware
- `src/main.py` — Register logging middleware in create_app()

**Approach:**
```python
import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("api")

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        duration_ms = (time.time() - start) * 1000
        logger.info(
            "%s %s %d %.1fms",
            request.method, request.url.path, response.status_code, duration_ms
        )
        return response
```

Configure logging in main.py or a setup function:
```python
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
```

## API Changes

N/A

## Data Model Changes

N/A

## Acceptance Criteria

- [ ] Every request is logged with method, path, status code, and duration
- [ ] Log output is at INFO level
- [ ] API key values are never present in log output
- [ ] Log format includes timestamp

## Test Requirements

- **Unit tests:** Test middleware logs correct format; verify no API key in logs
- **Integration tests:** Send requests and verify log entries appear
- **Edge cases:** Requests that raise exceptions still get logged

## Parent References

| Ref Type | ID               |
|----------|------------------|
| Story    | STORY-004        |
| Epic     | EPIC-004         |
| BRD      | BRD-NFR-007      |

## Definition of Done

- [ ] Code written and follows project conventions
- [ ] All tests passing (`pytest`)
- [ ] No linting errors
- [ ] PR opened and reviewed
- [ ] Acceptance criteria verified

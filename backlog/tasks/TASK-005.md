# Task: Implement Health Check Endpoint

| Field        | Value                |
|--------------|----------------------|
| **Task ID**  | TASK-005             |
| **Story**    | STORY-003            |
| **Status**   | To Do                |
| **Assignee** | develop-agent        |
| **Estimate** | 1h                   |

## Description

Create the health check route that returns the API status, version, and database connectivity status. This endpoint is exempt from authentication.

## Implementation Details

**Files to create/modify:**
- `src/routes/health.py` — Health check route handler
- `src/models/responses.py` — HealthResponse Pydantic model

**Approach:**
```python
from fastapi import APIRouter, Depends
from src.dependencies import get_db

router = APIRouter(prefix="/api/v1", tags=["health"])

@router.get("/health", response_model=HealthResponse)
async def health_check(db=Depends(get_db)):
    try:
        await db.execute("SELECT 1")
        db_status = "connected"
        status = "healthy"
    except Exception:
        db_status = "disconnected"
        status = "degraded"

    return HealthResponse(status=status, version=settings.app_version, database=db_status)
```

The `HealthResponse` model:
```python
class HealthResponse(BaseModel):
    status: str  # "healthy" or "degraded"
    version: str
    database: str  # "connected" or "disconnected"
```

## API Changes

| Endpoint         | Method | Description        |
|------------------|--------|--------------------|
| `/api/v1/health` | GET    | System health check|

**Response body:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected"
}
```

## Data Model Changes

N/A

## Acceptance Criteria

- [ ] GET /api/v1/health returns 200 with HealthResponse when DB is connected
- [ ] Returns {"status": "degraded", "database": "disconnected"} when DB fails
- [ ] No authentication required for this endpoint
- [ ] Response time < 2 seconds

## Test Requirements

- **Unit tests:** Test health check with mocked DB connection; test degraded path with DB error
- **Integration tests:** Test full endpoint returns 200 with expected fields
- **Edge cases:** Database file missing; database locked

## Parent References

| Ref Type | ID               |
|----------|------------------|
| Story    | STORY-003        |
| Epic     | EPIC-004         |
| BRD      | BRD-FR-009       |

## Definition of Done

- [ ] Code written and follows project conventions
- [ ] All tests passing (`pytest`)
- [ ] No linting errors
- [ ] PR opened and reviewed
- [ ] Acceptance criteria verified

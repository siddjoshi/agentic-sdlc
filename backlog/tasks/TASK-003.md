# Task: Create FastAPI App Factory in main.py

| Field        | Value                |
|--------------|----------------------|
| **Task ID**  | TASK-003             |
| **Story**    | STORY-001            |
| **Status**   | To Do                |
| **Assignee** | develop-agent        |
| **Estimate** | 2h                   |

## Description

Implement the FastAPI application factory (`create_app()`) with async lifespan context manager for database initialization and cleanup, CORS configuration, and router registration.

## Implementation Details

**Files to create/modify:**
- `src/main.py` — App factory, lifespan, CORS, router registration
- `src/dependencies.py` — FastAPI Depends() providers for DB and services

**Approach:**
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize DB, seed data
    db_manager = DatabaseManager(settings.database_url)
    await db_manager.initialize()
    app.state.db_manager = db_manager
    yield
    # Shutdown: close DB connections
    await db_manager.close()

def create_app() -> FastAPI:
    app = FastAPI(title="AI Learning Platform", version="1.0.0", lifespan=lifespan)
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    # Register routers (courses, lessons, quizzes, progress, health)
    # Add auth middleware
    return app

app = create_app()
```

The `dependencies.py` file should provide:
- `get_db()` — yields async DB connection from app.state.db_manager
- `get_content_service()` — returns configured ContentService instance

## API Changes

N/A — this creates the app shell that routes are registered into.

## Data Model Changes

N/A

## Acceptance Criteria

- [ ] `uvicorn src.main:app` starts without errors
- [ ] Lifespan initializes DB on startup and cleans up on shutdown
- [ ] CORS is configured to allow all origins for local dev
- [ ] All route modules are registered as routers under /api/v1
- [ ] `get_db()` dependency provides async DB connection per request

## Test Requirements

- **Unit tests:** Test create_app() returns FastAPI instance; test lifespan initializes DB
- **Integration tests:** Test app starts and serves requests via TestClient
- **Edge cases:** Missing DB file is auto-created; missing env vars fail at startup

## Parent References

| Ref Type | ID               |
|----------|------------------|
| Story    | STORY-001        |
| Epic     | EPIC-004         |
| BRD      | BRD-NFR-010      |

## Definition of Done

- [ ] Code written and follows project conventions
- [ ] All tests passing (`pytest`)
- [ ] No linting errors
- [ ] PR opened and reviewed
- [ ] Acceptance criteria verified

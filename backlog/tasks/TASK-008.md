# Task: Implement DatabaseManager with Schema Creation

| Field        | Value                |
|--------------|----------------------|
| **Task ID**  | TASK-008             |
| **Story**    | STORY-005            |
| **Status**   | To Do                |
| **Assignee** | develop-agent        |
| **Estimate** | 3h                   |

## Description

Implement the `DatabaseManager` class that manages async SQLite connections, creates all database tables on initialization, enables WAL mode, and creates required indexes. This is the core data infrastructure that all other components depend on.

## Implementation Details

**Files to create/modify:**
- `src/database/connection.py` — DatabaseManager class
- `src/database/models.py` — Pydantic models mirroring database entities

**Approach:**

DatabaseManager class:
```python
import aiosqlite
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._connection = None

    async def initialize(self):
        """Create tables, enable WAL mode, seed data."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        conn = await aiosqlite.connect(self.db_path)
        await conn.execute("PRAGMA journal_mode=WAL")
        # Create all 5 tables per data-layer LLD schema
        await conn.executescript(SCHEMA_SQL)
        # Create indexes
        await conn.executescript(INDEX_SQL)
        await conn.commit()
        self._connection = conn
        # Seed data (separate task)
        await seed_database(conn)

    async def get_connection(self):
        """Return the async database connection."""
        return self._connection

    async def close(self):
        if self._connection:
            await self._connection.close()
```

Schema SQL should match exactly the data-layer LLD:
- courses (id, title, description, topic, level, created_at)
- lessons (id, course_id, title, level, "order", objectives, created_at)
- quizzes (id, lesson_id, questions_json, generated_at)
- quiz_attempts (id, quiz_id, user_id, score, total, percentage, answers_json, attempted_at)
- user_progress (id, user_id, lesson_id, completed_at)

Plus 6 indexes per the LLD.

Database entity models in `src/database/models.py`:
```python
class CourseRow(BaseModel):
    id: int; title: str; description: str; topic: str; level: str; created_at: datetime

class LessonRow(BaseModel):
    id: int; course_id: int; title: str; level: str; order: int; objectives: str; created_at: datetime

class QuizRow(BaseModel):
    id: int; lesson_id: int; questions_json: str; generated_at: datetime

class QuizAttemptRow(BaseModel):
    id: int; quiz_id: int; user_id: str; score: int; total: int; percentage: float; answers_json: str; attempted_at: datetime

class UserProgressRow(BaseModel):
    id: int; user_id: str; lesson_id: int; completed_at: datetime
```

## API Changes

N/A

## Data Model Changes

- **Tables:** courses, lessons, quizzes, quiz_attempts, user_progress (all 5 created)
- **Indexes:** 6 indexes on foreign keys and common query columns

## Acceptance Criteria

- [ ] DatabaseManager creates all 5 tables with correct schema on initialize()
- [ ] WAL mode is enabled after initialization
- [ ] All 6 indexes are created
- [ ] Tables use IF NOT EXISTS for idempotent startup
- [ ] Database file is created at configured path with parent directories
- [ ] Pydantic models mirror all database entity fields

## Test Requirements

- **Unit tests:** Test schema creation with in-memory SQLite; verify table existence; verify WAL mode; verify index existence
- **Integration tests:** Test full initialize() → verify tables and indexes
- **Edge cases:** Re-initialization doesn't drop existing data; missing data/ directory auto-created

## Parent References

| Ref Type | ID               |
|----------|------------------|
| Story    | STORY-005        |
| Epic     | EPIC-001         |
| BRD      | BRD-NFR-006, BRD-FR-010 |

## Definition of Done

- [ ] Code written and follows project conventions
- [ ] All tests passing (`pytest`)
- [ ] No linting errors
- [ ] PR opened and reviewed
- [ ] Acceptance criteria verified

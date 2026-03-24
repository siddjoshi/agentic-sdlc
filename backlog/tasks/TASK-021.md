# Task: Implement ProgressRepository and Lesson Completion Endpoint

| Field        | Value                |
|--------------|----------------------|
| **Task ID**  | TASK-021             |
| **Story**    | STORY-012            |
| **Status**   | To Do                |
| **Assignee** | develop-agent        |
| **Estimate** | 2h                   |

## Description

Create the `ProgressRepository` class with `mark_complete()` method and the route handler for `POST /api/v1/progress/{user_id}/complete` that marks a lesson as completed for a user.

## Implementation Details

**Files to create/modify:**
- `src/repositories/progress_repository.py` — ProgressRepository class
- `src/routes/progress.py` — Lesson completion and progress route handlers
- `src/models/requests.py` — LessonCompleteRequest model
- `src/models/responses.py` — ProgressUpdateResponse model

**Approach:**

ProgressRepository:
```python
import aiosqlite
from datetime import datetime

class ProgressRepository:
    def __init__(self, db: aiosqlite.Connection):
        self.db = db

    async def mark_complete(self, user_id: str, lesson_id: int) -> datetime:
        """Mark a lesson as completed. Idempotent via INSERT OR IGNORE.

        Returns the completed_at timestamp.
        """
        await self.db.execute(
            "INSERT OR IGNORE INTO user_progress (user_id, lesson_id) VALUES (?, ?)",
            (user_id, lesson_id)
        )
        await self.db.commit()

        # Fetch the completion record
        cursor = await self.db.execute(
            "SELECT completed_at FROM user_progress WHERE user_id = ? AND lesson_id = ?",
            (user_id, lesson_id)
        )
        row = await cursor.fetchone()
        return row[0]
```

Route handler:
```python
from fastapi import APIRouter, Depends
from src.dependencies import get_db
from src.repositories.progress_repository import ProgressRepository
from src.repositories.course_repository import CourseRepository
from src.exceptions import LessonNotFoundError

router = APIRouter(prefix="/api/v1", tags=["progress"])

@router.post("/progress/{user_id}/complete", response_model=ProgressUpdateResponse)
async def mark_lesson_complete(
    user_id: str,
    body: LessonCompleteRequest,
    db=Depends(get_db),
):
    # Validate lesson exists
    course_repo = CourseRepository(db)
    lesson = await course_repo.get_lesson(body.lesson_id)
    if not lesson:
        raise LessonNotFoundError(body.lesson_id)

    progress_repo = ProgressRepository(db)
    completed_at = await progress_repo.mark_complete(user_id, body.lesson_id)

    return ProgressUpdateResponse(
        user_id=user_id,
        lesson_id=body.lesson_id,
        status="completed",
        updated_at=completed_at,
    )
```

## API Changes

| Endpoint                                  | Method | Description               |
|-------------------------------------------|--------|---------------------------|
| `/api/v1/progress/{user_id}/complete`     | POST   | Mark lesson as completed  |

**Request body:**
```json
{
  "lesson_id": 1
}
```

**Response body:**
```json
{
  "user_id": "user-42",
  "lesson_id": 1,
  "status": "completed",
  "updated_at": "2026-03-24T11:00:00Z"
}
```

## Data Model Changes

N/A — uses existing user_progress table.

## Acceptance Criteria

- [ ] POST /api/v1/progress/{user_id}/complete marks lesson completed
- [ ] Duplicate completions are idempotent (INSERT OR IGNORE)
- [ ] Invalid lesson_id returns HTTP 404
- [ ] Response includes user_id, lesson_id, status, and updated_at
- [ ] Completion persists across application restarts

## Test Requirements

- **Unit tests:** Test mark_complete() with valid lesson; test idempotency (call twice); test invalid lesson
- **Integration tests:** Full HTTP test: complete lesson → verify in DB
- **Edge cases:** Complete same lesson twice; lesson_id 0; very long user_id

## Parent References

| Ref Type | ID               |
|----------|------------------|
| Story    | STORY-012        |
| Epic     | EPIC-003         |
| BRD      | BRD-FR-008       |

## Definition of Done

- [ ] Code written and follows project conventions
- [ ] All tests passing (`pytest`)
- [ ] No linting errors
- [ ] PR opened and reviewed
- [ ] Acceptance criteria verified

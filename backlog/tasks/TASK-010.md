# Task: Implement CourseRepository with CRUD Methods

| Field        | Value                |
|--------------|----------------------|
| **Task ID**  | TASK-010             |
| **Story**    | STORY-007            |
| **Status**   | To Do                |
| **Assignee** | develop-agent        |
| **Estimate** | 2h                   |

## Description

Create the `CourseRepository` class with methods for listing courses with pagination, getting a single course with its lessons, listing lessons for a course, and getting a single lesson by ID. This follows the repository pattern from the data-layer LLD.

## Implementation Details

**Files to create/modify:**
- `src/repositories/course_repository.py` — CourseRepository class

**Approach:**
```python
import aiosqlite
import json

class CourseRepository:
    def __init__(self, db: aiosqlite.Connection):
        self.db = db

    async def list_courses(self, limit: int = 20, offset: int = 0) -> tuple[list[dict], int]:
        """List courses with pagination. Returns (courses, total_count)."""
        cursor = await self.db.execute(
            "SELECT id, title, description, topic, level, created_at FROM courses ORDER BY id LIMIT ? OFFSET ?",
            (limit, offset)
        )
        rows = await cursor.fetchall()
        # Get total count
        count_cursor = await self.db.execute("SELECT COUNT(*) FROM courses")
        total = (await count_cursor.fetchone())[0]
        # Get lesson count per course
        # ...
        return courses, total

    async def get_course(self, course_id: int) -> dict | None:
        """Get course by ID with lesson list."""
        # SELECT course, then SELECT lessons WHERE course_id = ?

    async def list_lessons(self, course_id: int, limit: int = 20, offset: int = 0) -> tuple[list[dict], int]:
        """List lessons for a course, ordered by sequence."""
        # Verify course exists first, raise CourseNotFoundError if not

    async def get_lesson(self, lesson_id: int) -> dict | None:
        """Get a single lesson by ID."""
        # Returns lesson metadata including objectives JSON
```

Use `db.row_factory = aiosqlite.Row` for dict-like row access. All methods should return data matching the Pydantic models from the LLD.

## API Changes

N/A — repository is consumed by route handlers.

## Data Model Changes

N/A

## Acceptance Criteria

- [ ] list_courses() returns paginated results with total count
- [ ] get_course() returns course details with nested lessons list
- [ ] get_course() returns None for non-existent course ID
- [ ] list_lessons() returns ordered lessons for a valid course
- [ ] list_lessons() raises CourseNotFoundError for invalid course
- [ ] get_lesson() returns lesson with objectives field

## Test Requirements

- **Unit tests:** Test each method with seeded in-memory DB; test pagination; test not-found cases
- **Integration tests:** Test repository against real seeded database
- **Edge cases:** Empty results; offset beyond total count; course with 0 lessons

## Parent References

| Ref Type | ID               |
|----------|------------------|
| Story    | STORY-007        |
| Epic     | EPIC-001         |
| BRD      | BRD-FR-001, BRD-FR-002, BRD-FR-003 |

## Definition of Done

- [ ] Code written and follows project conventions
- [ ] All tests passing (`pytest`)
- [ ] No linting errors
- [ ] PR opened and reviewed
- [ ] Acceptance criteria verified

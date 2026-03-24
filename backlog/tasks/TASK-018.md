# Task: Implement QuizRepository and Quiz Route Handler

| Field        | Value                |
|--------------|----------------------|
| **Task ID**  | TASK-018             |
| **Story**    | STORY-009            |
| **Status**   | To Do                |
| **Assignee** | develop-agent        |
| **Estimate** | 2h                   |

## Description

Create the `QuizRepository` for quiz CRUD operations and the route handler for `POST /api/v1/lessons/{id}/quiz` that generates a quiz for a given lesson.

## Implementation Details

**Files to create/modify:**
- `src/repositories/quiz_repository.py` — QuizRepository class
- `src/routes/lessons.py` — Add quiz generation route handler

**Approach:**

QuizRepository:
```python
import aiosqlite
import json

class QuizRepository:
    def __init__(self, db: aiosqlite.Connection):
        self.db = db

    async def create_quiz(self, lesson_id: int, questions_json: str) -> int:
        """Insert a quiz record and return the quiz_id."""
        cursor = await self.db.execute(
            "INSERT INTO quizzes (lesson_id, questions_json) VALUES (?, ?)",
            (lesson_id, questions_json)
        )
        await self.db.commit()
        return cursor.lastrowid

    async def get_quiz(self, quiz_id: int) -> dict | None:
        """Get a quiz by ID."""
        cursor = await self.db.execute(
            "SELECT id, lesson_id, questions_json, generated_at FROM quizzes WHERE id = ?",
            (quiz_id,)
        )
        row = await cursor.fetchone()
        if not row:
            return None
        return {"id": row[0], "lesson_id": row[1], "questions_json": row[2], "generated_at": row[3]}
```

Quiz route handler in `src/routes/lessons.py`:
```python
@router.post("/lessons/{lesson_id}/quiz", response_model=QuizResponse)
async def generate_quiz(
    lesson_id: int,
    db=Depends(get_db),
    content_service=Depends(get_content_service),
):
    repo = CourseRepository(db)
    lesson = await repo.get_lesson(lesson_id)
    if not lesson:
        raise LessonNotFoundError(lesson_id)

    course = await repo.get_course(lesson["course_id"])
    result = await content_service.generate_quiz(
        lesson_id=lesson_id, topic=course["topic"], level=lesson["level"], db=db
    )
    return result
```

## API Changes

| Endpoint                    | Method | Description               |
|-----------------------------|--------|---------------------------|
| `/api/v1/lessons/{id}/quiz` | POST   | Generate a quiz for lesson|

**Response body:**
```json
{
  "quiz_id": 12,
  "lesson_id": 5,
  "topic": "github-actions",
  "level": "beginner",
  "questions": [{"question": "...", "options": [...], "correct_answer": "...", "explanation": "..."}],
  "generated_at": "2026-03-24T10:31:00Z"
}
```

## Data Model Changes

N/A — uses existing quizzes table.

## Acceptance Criteria

- [ ] QuizRepository.create_quiz() persists quiz and returns quiz_id
- [ ] QuizRepository.get_quiz() retrieves quiz by ID or returns None
- [ ] POST /api/v1/lessons/{id}/quiz returns generated and validated quiz
- [ ] Quiz is persisted in DB before returning to client
- [ ] Invalid lesson_id returns HTTP 404

## Test Requirements

- **Unit tests:** Test QuizRepository CRUD with in-memory DB; test route handler with mocks
- **Integration tests:** Full HTTP test with mocked AI and seeded DB
- **Edge cases:** Lesson exists but AI fails; quiz persistence failure

## Parent References

| Ref Type | ID               |
|----------|------------------|
| Story    | STORY-009        |
| Epic     | EPIC-002         |
| BRD      | BRD-FR-005, BRD-AI-002 |

## Definition of Done

- [ ] Code written and follows project conventions
- [ ] All tests passing (`pytest`)
- [ ] No linting errors
- [ ] PR opened and reviewed
- [ ] Acceptance criteria verified

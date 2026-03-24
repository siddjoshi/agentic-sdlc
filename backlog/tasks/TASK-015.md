# Task: Implement Lesson Content Route Handler

| Field        | Value                |
|--------------|----------------------|
| **Task ID**  | TASK-015             |
| **Story**    | STORY-008            |
| **Status**   | To Do                |
| **Assignee** | develop-agent        |
| **Estimate** | 2h                   |

## Description

Create the FastAPI route handler for `POST /api/v1/lessons/{id}/content` that looks up the lesson metadata from the database, invokes the ContentService to generate AI content, and returns the result.

## Implementation Details

**Files to create/modify:**
- `src/routes/lessons.py` — Lesson content and quiz route handlers
- `src/models/responses.py` — LessonContentResponse model (add if not present)

**Approach:**
```python
from fastapi import APIRouter, Depends
from src.dependencies import get_db, get_content_service
from src.repositories.course_repository import CourseRepository
from src.exceptions import LessonNotFoundError

router = APIRouter(prefix="/api/v1", tags=["lessons"])

@router.post("/lessons/{lesson_id}/content", response_model=LessonContentResponse)
async def generate_lesson_content(
    lesson_id: int,
    db=Depends(get_db),
    content_service=Depends(get_content_service),
):
    # 1. Look up lesson metadata
    repo = CourseRepository(db)
    lesson = await repo.get_lesson(lesson_id)
    if not lesson:
        raise LessonNotFoundError(lesson_id)

    # 2. Parse objectives from JSON string
    import json
    objectives = json.loads(lesson["objectives"])

    # 3. Get the course to determine topic
    # lesson has course_id — look up course to get topic field
    course = await repo.get_course(lesson["course_id"])
    topic = course["topic"]

    # 4. Generate content via AI
    result = await content_service.generate_lesson_content(
        lesson_id=lesson_id,
        topic=topic,
        level=lesson["level"],
        objectives=objectives,
    )
    return result
```

Update `src/dependencies.py` to provide `get_content_service()`:
```python
def get_content_service(request: Request) -> ContentService:
    return request.app.state.content_service
```

Initialize ContentService in lifespan (main.py).

## API Changes

| Endpoint                       | Method | Description                     |
|--------------------------------|--------|---------------------------------|
| `/api/v1/lessons/{id}/content` | POST   | Generate AI lesson content      |

**Response body:**
```json
{
  "lesson_id": 5,
  "topic": "github-actions",
  "level": "beginner",
  "content_markdown": "# Introduction to GitHub Actions...",
  "generated_at": "2026-03-24T10:30:00Z"
}
```

## Data Model Changes

N/A

## Acceptance Criteria

- [ ] POST /api/v1/lessons/{id}/content returns AI-generated Markdown content
- [ ] Lesson metadata (topic, level, objectives) is loaded from DB for prompt construction
- [ ] Invalid lesson ID returns HTTP 404
- [ ] AI service errors propagate as HTTP 503
- [ ] Response matches LessonContentResponse schema

## Test Requirements

- **Unit tests:** Test route with mocked dependencies; test 404 for missing lesson
- **Integration tests:** Full HTTP test with mocked AI and seeded DB
- **Edge cases:** Lesson with empty objectives; non-integer lesson_id returns 422

## Parent References

| Ref Type | ID               |
|----------|------------------|
| Story    | STORY-008        |
| Epic     | EPIC-002         |
| BRD      | BRD-FR-004, BRD-FR-015 |

## Definition of Done

- [ ] Code written and follows project conventions
- [ ] All tests passing (`pytest`)
- [ ] No linting errors
- [ ] PR opened and reviewed
- [ ] Acceptance criteria verified

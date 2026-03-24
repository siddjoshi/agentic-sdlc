# Task: Implement Course Catalog Route Handlers

| Field        | Value                |
|--------------|----------------------|
| **Task ID**  | TASK-011             |
| **Story**    | STORY-007            |
| **Status**   | To Do                |
| **Assignee** | develop-agent        |
| **Estimate** | 3h                   |

## Description

Create FastAPI route handlers for the course catalog endpoints: list courses, get course detail, and list lessons. These handlers use the CourseRepository via dependency injection and return Pydantic response models.

## Implementation Details

**Files to create/modify:**
- `src/routes/courses.py` — Course and lesson list route handlers
- `src/models/responses.py` — CourseResponse, CourseListResponse, LessonSummary, CourseDetailResponse, LessonListResponse models

**Approach:**
```python
from fastapi import APIRouter, Depends, Query
from src.dependencies import get_db
from src.repositories.course_repository import CourseRepository

router = APIRouter(prefix="/api/v1", tags=["courses"])

@router.get("/courses", response_model=CourseListResponse)
async def list_courses(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db=Depends(get_db)
):
    repo = CourseRepository(db)
    courses, total = await repo.list_courses(limit, offset)
    return CourseListResponse(courses=courses, total=total, limit=limit, offset=offset)

@router.get("/courses/{course_id}", response_model=CourseDetailResponse)
async def get_course(course_id: int, db=Depends(get_db)):
    repo = CourseRepository(db)
    course = await repo.get_course(course_id)
    if not course:
        raise CourseNotFoundError(course_id)
    return course

@router.get("/courses/{course_id}/lessons", response_model=LessonListResponse)
async def list_lessons(
    course_id: int,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db=Depends(get_db)
):
    repo = CourseRepository(db)
    lessons, total = await repo.list_lessons(course_id, limit, offset)
    return LessonListResponse(lessons=lessons, total=total, limit=limit, offset=offset)
```

Response models per api-layer LLD section 3.2.

## API Changes

| Endpoint                        | Method | Description                         |
|---------------------------------|--------|-------------------------------------|
| `/api/v1/courses`               | GET    | List all courses with pagination    |
| `/api/v1/courses/{id}`          | GET    | Get course details with lessons     |
| `/api/v1/courses/{id}/lessons`  | GET    | List lessons for a course           |

**Response body (courses list):**
```json
{
  "courses": [{"id": 1, "title": "...", "description": "...", "level": "beginner", "total_lessons": 5}],
  "total": 6,
  "limit": 20,
  "offset": 0
}
```

## Data Model Changes

N/A

## Acceptance Criteria

- [ ] GET /api/v1/courses returns paginated course list with total_lessons count
- [ ] GET /api/v1/courses/{id} returns course details with nested lessons array
- [ ] GET /api/v1/courses/{id} returns 404 for non-existent course
- [ ] GET /api/v1/courses/{id}/lessons returns ordered lesson list
- [ ] Pagination works with limit and offset query parameters
- [ ] Default pagination: limit=20, offset=0

## Test Requirements

- **Unit tests:** Test route handlers with mocked repository
- **Integration tests:** Test full HTTP flow with seeded test DB via TestClient
- **Edge cases:** Non-integer course_id returns 422; limit=0 returns 422; empty courses list

## Parent References

| Ref Type | ID               |
|----------|------------------|
| Story    | STORY-007        |
| Epic     | EPIC-001         |
| BRD      | BRD-FR-001, BRD-FR-002, BRD-FR-003, BRD-FR-014 |

## Definition of Done

- [ ] Code written and follows project conventions
- [ ] All tests passing (`pytest`)
- [ ] No linting errors
- [ ] PR opened and reviewed
- [ ] Acceptance criteria verified

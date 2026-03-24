# Task: Implement Progress Aggregation Query and Endpoint

| Field        | Value                |
|--------------|----------------------|
| **Task ID**  | TASK-022             |
| **Story**    | STORY-013            |
| **Status**   | To Do                |
| **Assignee** | develop-agent        |
| **Estimate** | 3h                   |

## Description

Add the `get_progress()` and `get_quiz_scores()` methods to ProgressRepository and create the route handler for `GET /api/v1/progress/{user_id}` that returns per-course progress across all courses.

## Implementation Details

**Files to create/modify:**
- `src/repositories/progress_repository.py` — Add get_progress() and get_quiz_scores()
- `src/routes/progress.py` — Add progress retrieval route handler
- `src/models/responses.py` — CourseProgress, ProgressResponse models

**Approach:**

ProgressRepository additions:
```python
async def get_progress(self, user_id: str) -> list[dict]:
    """Get per-course progress for a user.

    Returns all courses with completed_lessons, total_lessons, and completion_percentage.
    """
    cursor = await self.db.execute("""
        SELECT
            c.id as course_id,
            c.title as course_title,
            COUNT(DISTINCT up.lesson_id) as completed_lessons,
            COUNT(DISTINCT l.id) as total_lessons,
            ROUND(
                CASE WHEN COUNT(DISTINCT l.id) = 0 THEN 0
                ELSE COUNT(DISTINCT up.lesson_id) * 100.0 / COUNT(DISTINCT l.id)
                END, 1
            ) as completion_percentage
        FROM courses c
        JOIN lessons l ON l.course_id = c.id
        LEFT JOIN user_progress up ON up.lesson_id = l.id AND up.user_id = ?
        GROUP BY c.id, c.title
        ORDER BY c.id
    """, (user_id,))
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]

async def get_quiz_scores(self, user_id: str, course_id: int) -> list[float]:
    """Get quiz scores for a user in a specific course."""
    cursor = await self.db.execute("""
        SELECT qa.percentage
        FROM quiz_attempts qa
        JOIN quizzes q ON q.id = qa.quiz_id
        JOIN lessons l ON l.id = q.lesson_id
        WHERE qa.user_id = ? AND l.course_id = ?
        ORDER BY qa.attempted_at
    """, (user_id, course_id))
    rows = await cursor.fetchall()
    return [row[0] for row in rows]
```

Route handler:
```python
@router.get("/progress/{user_id}", response_model=ProgressResponse)
async def get_progress(
    user_id: str,
    db=Depends(get_db),
):
    progress_repo = ProgressRepository(db)
    course_progress = await progress_repo.get_progress(user_id)

    # Enrich with quiz scores per course
    courses = []
    for cp in course_progress:
        quiz_scores = await progress_repo.get_quiz_scores(user_id, cp["course_id"])
        courses.append(CourseProgress(
            course_id=cp["course_id"],
            course_title=cp["course_title"],
            completed_lessons=cp["completed_lessons"],
            total_lessons=cp["total_lessons"],
            quiz_scores=quiz_scores,
            completion_percentage=cp["completion_percentage"],
        ))

    return ProgressResponse(user_id=user_id, courses=courses)
```

Response models:
```python
class CourseProgress(BaseModel):
    course_id: int
    course_title: str
    completed_lessons: int
    total_lessons: int
    quiz_scores: list[float]
    completion_percentage: float

class ProgressResponse(BaseModel):
    user_id: str
    courses: list[CourseProgress]
```

## API Changes

| Endpoint                        | Method | Description                     |
|---------------------------------|--------|---------------------------------|
| `/api/v1/progress/{user_id}`    | GET    | Get user progress across courses|

**Response body:**
```json
{
  "user_id": "user-42",
  "courses": [
    {
      "course_id": 1,
      "course_title": "GitHub Actions — Beginner",
      "completed_lessons": 3,
      "total_lessons": 5,
      "quiz_scores": [80.0, 100.0],
      "completion_percentage": 60.0
    }
  ]
}
```

## Data Model Changes

N/A — uses existing tables with aggregation queries.

## Acceptance Criteria

- [ ] GET /api/v1/progress/{user_id} returns all courses with progress data
- [ ] Completed lessons count matches actual completions
- [ ] Total lessons count matches seeded lesson count per course
- [ ] Completion percentage is calculated correctly (rounded to 1 decimal)
- [ ] Quiz scores array contains all quiz attempt percentages for that course
- [ ] User with no progress sees all courses with 0 completed and 0% completion
- [ ] Response time < 2 seconds

## Test Requirements

- **Unit tests:** Test get_progress() with no completions; with partial completions; with quiz scores
- **Integration tests:** Full flow: seed DB → complete lessons → take quiz → check progress
- **Edge cases:** User with no activity; user with all lessons complete; course with 0 lessons

## Parent References

| Ref Type | ID               |
|----------|------------------|
| Story    | STORY-013        |
| Epic     | EPIC-003         |
| BRD      | BRD-FR-007       |

## Definition of Done

- [ ] Code written and follows project conventions
- [ ] All tests passing (`pytest`)
- [ ] No linting errors
- [ ] PR opened and reviewed
- [ ] Acceptance criteria verified

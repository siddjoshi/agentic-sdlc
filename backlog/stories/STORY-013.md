# Story: Progress Dashboard API

| Field        | Value                |
|--------------|----------------------|
| **Story ID** | STORY-013            |
| **Epic**     | EPIC-003             |
| **Status**   | Draft                |
| **Assignee** | develop-agent        |
| **Estimate** | M                    |
| **Priority** | P0                   |

## User Story

**As a** learner,
**I want** to view my progress across all courses,
**so that** I can see how many lessons I've completed, my quiz scores, and my overall completion percentage.

## Acceptance Criteria

1. **Given** a user with some progress,
   **When** I call GET /api/v1/progress/{user_id},
   **Then** I receive per-course progress including completed_lessons, total_lessons, quiz_scores, and completion_percentage.

2. **Given** a user with no progress,
   **When** I call GET /api/v1/progress/{user_id},
   **Then** I receive all courses with 0 completed_lessons and 0.0 completion_percentage.

3. **Given** a user has completed 3 of 5 lessons in a course,
   **When** I check their progress,
   **Then** completion_percentage is 60.0.

4. **Given** a user has taken 2 quizzes with scores 80% and 100%,
   **When** I check their progress,
   **Then** quiz_scores contains [80.0, 100.0].

## BRD & Design References

| BRD ID        | HLD/LLD Component                            |
|---------------|----------------------------------------------|
| BRD-FR-007    | COMP-001/004 — GET /api/v1/progress/{user_id}|

## Tasks Breakdown

| Task ID    | Description                                         | Estimate |
|------------|-----------------------------------------------------|----------|
| TASK-022   | Implement progress aggregation query and endpoint    | 3h       |

## UI/UX Notes

N/A — API only.

## Technical Notes

- **Stack:** Python / FastAPI / aiosqlite
- **Key considerations:** Use aggregation query joining courses, lessons, user_progress, and quiz_attempts; compute completion_percentage as (completed/total)*100 rounded to 1 decimal; return all courses even if user has no progress
- **Configuration:** None specific

## Dependencies

- STORY-012 (lesson completion tracking)
- STORY-011 (quiz scoring for quiz_scores data)
- STORY-005 (database schema)

## Definition of Done

- [ ] Code implements all acceptance criteria
- [ ] Unit and integration tests written and passing
- [ ] API documentation updated (if applicable)
- [ ] Code reviewed and approved
- [ ] No regressions in existing tests

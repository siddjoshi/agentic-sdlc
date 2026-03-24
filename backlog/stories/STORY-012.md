# Story: Lesson Completion Tracking

| Field        | Value                |
|--------------|----------------------|
| **Story ID** | STORY-012            |
| **Epic**     | EPIC-003             |
| **Status**   | Draft                |
| **Assignee** | develop-agent        |
| **Estimate** | S                    |
| **Priority** | P0                   |

## User Story

**As a** learner,
**I want** to mark lessons as completed,
**so that** my progress is saved and I can track which lessons I've finished.

## Acceptance Criteria

1. **Given** a valid user_id and lesson_id,
   **When** I call POST /api/v1/progress/{user_id}/complete with {"lesson_id": 1},
   **Then** I receive HTTP 200 with {"user_id": "...", "lesson_id": 1, "status": "completed", "updated_at": "..."}.

2. **Given** the same lesson is completed again,
   **When** I submit the same completion,
   **Then** the request is idempotent — no duplicate record is created, and I still receive HTTP 200.

3. **Given** an invalid lesson_id,
   **When** I submit a completion,
   **Then** I receive HTTP 404.

4. **Given** a lesson has been marked complete,
   **When** I check GET /api/v1/progress/{user_id},
   **Then** the completed lesson is reflected in the progress count.

## BRD & Design References

| BRD ID        | HLD/LLD Component                                     |
|---------------|--------------------------------------------------------|
| BRD-FR-008    | COMP-001/004 — POST /api/v1/progress/{user_id}/complete|
| BRD-NFR-006   | Data Layer — proper transaction management             |

## Tasks Breakdown

| Task ID    | Description                                           | Estimate |
|------------|-------------------------------------------------------|----------|
| TASK-021   | Implement ProgressRepository and completion endpoint   | 2h       |

## UI/UX Notes

N/A — API only.

## Technical Notes

- **Stack:** Python / FastAPI / aiosqlite
- **Key considerations:** Use INSERT OR IGNORE for idempotency on UNIQUE(user_id, lesson_id); validate lesson_id exists before inserting; return the completed_at timestamp
- **Configuration:** None specific

## Dependencies

- STORY-005 (database schema with user_progress table)
- STORY-006 (seed data for lesson records to validate against)

## Definition of Done

- [ ] Code implements all acceptance criteria
- [ ] Unit and integration tests written and passing
- [ ] API documentation updated (if applicable)
- [ ] Code reviewed and approved
- [ ] No regressions in existing tests

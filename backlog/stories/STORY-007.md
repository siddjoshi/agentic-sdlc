# Story: Course Catalog API Endpoints

| Field        | Value                |
|--------------|----------------------|
| **Story ID** | STORY-007            |
| **Epic**     | EPIC-001             |
| **Status**   | Draft                |
| **Assignee** | develop-agent        |
| **Estimate** | M                    |
| **Priority** | P0                   |

## User Story

**As a** learner,
**I want** to browse available courses and view their lesson outlines via the API,
**so that** I can choose which GitHub topic and skill level to study.

## Acceptance Criteria

1. **Given** courses exist in the database,
   **When** I call GET /api/v1/courses,
   **Then** I receive a paginated JSON list with id, title, description, level, and total_lessons for each course.

2. **Given** a valid course ID,
   **When** I call GET /api/v1/courses/{id},
   **Then** I receive course details with a nested lessons array (id, title, level, order).

3. **Given** an invalid course ID,
   **When** I call GET /api/v1/courses/{id},
   **Then** I receive HTTP 404 with a structured error response.

4. **Given** courses exist,
   **When** I call GET /api/v1/courses?limit=2&offset=0,
   **Then** I receive exactly 2 courses and a total count.

5. **Given** a valid course ID,
   **When** I call GET /api/v1/courses/{id}/lessons,
   **Then** I receive a paginated, ordered list of lessons for that course.

## BRD & Design References

| BRD ID        | HLD/LLD Component                              |
|---------------|-------------------------------------------------|
| BRD-FR-001    | COMP-001/003 — GET /api/v1/courses              |
| BRD-FR-002    | COMP-001/003 — GET /api/v1/courses/{id}         |
| BRD-FR-003    | COMP-001/003 — GET /api/v1/courses/{id}/lessons |
| BRD-FR-014    | COMP-001 — pagination with limit/offset         |
| BRD-NFR-001   | Response < 2 seconds                            |

## Tasks Breakdown

| Task ID    | Description                                       | Estimate |
|------------|---------------------------------------------------|----------|
| TASK-010   | Implement CourseRepository with CRUD methods       | 2h       |
| TASK-011   | Implement course catalog route handlers            | 3h       |

## UI/UX Notes

N/A — API only.

## Technical Notes

- **Stack:** Python / FastAPI / aiosqlite
- **Key considerations:** Use repository pattern per LLD; inject DB connection via FastAPI Depends(); pagination defaults: limit=20, offset=0
- **Configuration:** None specific

## Dependencies

- STORY-005 (database schema)
- STORY-006 (seed data)
- STORY-001 (project scaffolding)

## Definition of Done

- [ ] Code implements all acceptance criteria
- [ ] Unit and integration tests written and passing
- [ ] API documentation updated (if applicable)
- [ ] Code reviewed and approved
- [ ] No regressions in existing tests

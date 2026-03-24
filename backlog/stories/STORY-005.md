# Story: Database Initialization & Schema

| Field        | Value                |
|--------------|----------------------|
| **Story ID** | STORY-005            |
| **Epic**     | EPIC-001             |
| **Status**   | Draft                |
| **Assignee** | develop-agent        |
| **Estimate** | M                    |
| **Priority** | P0                   |

## User Story

**As a** developer,
**I want** the database schema to be automatically created and the database initialized on application startup,
**so that** the platform is ready to serve data without manual setup steps.

## Acceptance Criteria

1. **Given** the application starts for the first time,
   **When** the lifespan context manager runs,
   **Then** all 5 tables (courses, lessons, quizzes, quiz_attempts, user_progress) are created with correct schema.

2. **Given** the database already exists with tables,
   **When** the application restarts,
   **Then** existing data is preserved (CREATE TABLE IF NOT EXISTS).

3. **Given** the database is initialized,
   **When** I check the journal mode,
   **Then** WAL mode is enabled.

4. **Given** the database is initialized,
   **When** I check indexes,
   **Then** all 6 performance indexes exist.

## BRD & Design References

| BRD ID        | HLD/LLD Component                            |
|---------------|----------------------------------------------|
| BRD-NFR-006   | Data Layer — WAL mode, transaction management|
| BRD-FR-010    | Data Layer — database initialization         |

## Tasks Breakdown

| Task ID    | Description                                       | Estimate |
|------------|---------------------------------------------------|----------|
| TASK-008   | Implement DatabaseManager with schema creation    | 3h       |

## UI/UX Notes

N/A — Backend infrastructure.

## Technical Notes

- **Stack:** Python / aiosqlite
- **Key considerations:** Use `aiosqlite` for async access; enable WAL mode via PRAGMA; create tables idempotently; DatabaseManager class per data-layer LLD
- **Configuration:** DATABASE_URL env var (default: data/learning_platform.db)

## Dependencies

- STORY-001 (project scaffolding for config and lifespan)

## Definition of Done

- [ ] Code implements all acceptance criteria
- [ ] Unit and integration tests written and passing
- [ ] API documentation updated (if applicable)
- [ ] Code reviewed and approved
- [ ] No regressions in existing tests

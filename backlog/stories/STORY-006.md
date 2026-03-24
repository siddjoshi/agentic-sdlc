# Story: Course & Lesson Seed Data

| Field        | Value                |
|--------------|----------------------|
| **Story ID** | STORY-006            |
| **Epic**     | EPIC-001             |
| **Status**   | Draft                |
| **Assignee** | develop-agent        |
| **Estimate** | M                    |
| **Priority** | P0                   |

## User Story

**As a** learner,
**I want** the platform to have pre-loaded courses and lessons for GitHub Actions, Copilot, and Advanced Security,
**so that** I can immediately browse and start learning when the platform starts.

## Acceptance Criteria

1. **Given** the application starts,
   **When** seed data runs,
   **Then** 6 courses exist (2 per topic: beginner + intermediate).

2. **Given** the seed data has run,
   **When** I count all lessons,
   **Then** there are at least 30 lessons across all courses.

3. **Given** a course exists,
   **When** I list its lessons,
   **Then** each lesson has a title, level, order, and JSON objectives array.

4. **Given** the seed data has already been inserted,
   **When** the app restarts,
   **Then** no duplicate courses or lessons are created (INSERT OR IGNORE).

## BRD & Design References

| BRD ID        | HLD/LLD Component                    |
|---------------|--------------------------------------|
| BRD-FR-010    | COMP-003 / Data Layer — seed data    |

## Tasks Breakdown

| Task ID    | Description                                 | Estimate |
|------------|---------------------------------------------|----------|
| TASK-009   | Implement seed data for all 6 courses       | 3h       |

## UI/UX Notes

N/A — Backend data seeding.

## Technical Notes

- **Stack:** Python / aiosqlite
- **Key considerations:** Each course needs 5-8 lessons with learning objectives as JSON arrays; use INSERT OR IGNORE for idempotency; call seed_database() from DatabaseManager.initialize()
- **Configuration:** None — seed data is hardcoded in src/database/seed.py

## Dependencies

- STORY-005 (database schema must exist first)

## Definition of Done

- [ ] Code implements all acceptance criteria
- [ ] Unit and integration tests written and passing
- [ ] API documentation updated (if applicable)
- [ ] Code reviewed and approved
- [ ] No regressions in existing tests

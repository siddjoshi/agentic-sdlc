# Epic: Course Catalog & Content Management

| Field       | Value                |
|-------------|----------------------|
| **Epic ID** | EPIC-001             |
| **Status**  | Draft                |
| **Owner**   | epic-and-tasks-agent |
| **Created** | 2026-03-24           |
| **Target**  | Sprint 1             |

## Goal / Objective

Deliver a fully functional course catalog with seeded data for 3 GitHub training topics (Actions, Copilot, Advanced Security) at 2 skill levels each, browsable via REST API endpoints with pagination.

## Business Value

Provides the foundational content structure that all other features (AI generation, quizzes, progress tracking) depend on. Without a seeded catalog, learners cannot discover or navigate available training material.

## BRD Requirements Mapped

| BRD ID       | Description                                          |
|--------------|------------------------------------------------------|
| BRD-FR-001   | GET /api/v1/courses — list all courses               |
| BRD-FR-002   | GET /api/v1/courses/{id} — course details + lessons  |
| BRD-FR-003   | GET /api/v1/courses/{id}/lessons — list lessons      |
| BRD-FR-010   | Seed database with course/lesson metadata at startup |
| BRD-FR-014   | Pagination support on list endpoints                 |
| BRD-NFR-001  | Non-AI endpoints respond < 2 seconds                 |
| BRD-NFR-010  | Modular codebase structure                           |

## Features

| Feature ID | Name                      | Priority (P0/P1/P2) | Status  |
|------------|---------------------------|----------------------|---------|
| FEAT-001   | Database Schema & Init    | P0                   | Planned |
| FEAT-002   | Course Seed Data          | P0                   | Planned |
| FEAT-003   | Course Catalog API        | P0                   | Planned |
| FEAT-004   | Lesson List API           | P0                   | Planned |
| FEAT-005   | Pagination Support        | P1                   | Planned |

## Acceptance Criteria

1. Application startup creates all required SQLite tables and seeds 6 courses with 30+ lessons
2. GET /api/v1/courses returns all courses with id, title, description, level fields
3. GET /api/v1/courses/{id} returns course details with nested lesson outline
4. GET /api/v1/courses/{id}/lessons returns ordered lesson list for a course
5. All list endpoints support limit/offset pagination with total count
6. Invalid course IDs return HTTP 404 with structured error response

## Dependencies & Risks

**Dependencies:**
- Python 3.11+ runtime
- FastAPI, aiosqlite packages
- SQLite database file location (data/learning_platform.db)

**Risks:**
- Seed data must be comprehensive enough to support 30+ lessons across all topics

## Out of Scope

- AI content generation (EPIC-002)
- Quiz generation or scoring
- User progress tracking
- Frontend UI

## Definition of Done

- [ ] All stories in this epic are Done
- [ ] Acceptance criteria verified
- [ ] API endpoints documented
- [ ] No critical or high-severity bugs open
- [ ] Demo-ready for stakeholder review

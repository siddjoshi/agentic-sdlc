# Epic: Learning Experience & Progress Tracking

| Field       | Value                |
|-------------|----------------------|
| **Epic ID** | EPIC-003             |
| **Status**  | Draft                |
| **Owner**   | epic-and-tasks-agent |
| **Created** | 2026-03-24           |
| **Target**  | Sprint 1             |

## Goal / Objective

Enable learners to submit quiz answers for scoring with per-question feedback, mark lessons as completed, and view their progress across all courses — with persistent storage in SQLite.

## Business Value

Progress tracking and quiz scoring close the learning loop — learners can measure their skill acquisition, identify knowledge gaps, and track completion across all training topics. This is essential for demonstrating measurable skill assessment (BO-3).

## BRD Requirements Mapped

| BRD ID       | Description                                              |
|--------------|----------------------------------------------------------|
| BRD-FR-006   | POST /api/v1/quiz/{quiz_id}/submit — score quiz answers  |
| BRD-FR-007   | GET /api/v1/progress/{user_id} — user progress           |
| BRD-FR-008   | POST /api/v1/progress/{user_id}/complete — mark complete |
| BRD-FR-011   | Persist quiz scores in SQLite                            |
| BRD-NFR-006  | SQLite WAL mode and proper transaction management        |
| BRD-NFR-012  | Atomic persistence for quiz scores and progress          |

## Features

| Feature ID | Name                          | Priority (P0/P1/P2) | Status  |
|------------|-------------------------------|----------------------|---------|
| FEAT-011   | Quiz Submission & Scoring     | P0                   | Planned |
| FEAT-012   | Lesson Completion Tracking    | P0                   | Planned |
| FEAT-013   | Progress Dashboard API        | P0                   | Planned |

## Acceptance Criteria

1. POST /api/v1/quiz/{quiz_id}/submit returns score, total, percentage, and per-question feedback
2. Quiz scores persist in SQLite and are retrievable via the progress endpoint
3. POST /api/v1/progress/{user_id}/complete marks a lesson as completed (idempotent)
4. GET /api/v1/progress/{user_id} returns per-course progress with completed_lessons, total_lessons, quiz_scores, and completion_percentage
5. Duplicate lesson completions do not create duplicate records
6. Quiz attempt storage is atomic — partial writes are rolled back

## Dependencies & Risks

**Dependencies:**
- EPIC-001 (course/lesson tables must exist)
- EPIC-002 (quizzes table and quiz records must exist for scoring)

**Risks:**
- Concurrent writes to SQLite from multiple requests (mitigated by WAL mode)
- Quiz answer count mismatch with question count requires validation

## Out of Scope

- Training Manager progress monitoring (UC-007, deferred to post-MVP)
- Leaderboards or comparative analytics
- Certificate generation

## Definition of Done

- [ ] All stories in this epic are Done
- [ ] Acceptance criteria verified
- [ ] API endpoints documented
- [ ] No critical or high-severity bugs open
- [ ] Demo-ready for stakeholder review

# Story: Quiz Submission & Scoring

| Field        | Value                |
|--------------|----------------------|
| **Story ID** | STORY-011            |
| **Epic**     | EPIC-003             |
| **Status**   | Draft                |
| **Assignee** | develop-agent        |
| **Estimate** | M                    |
| **Priority** | P0                   |

## User Story

**As a** learner,
**I want** to submit my quiz answers and receive a score with per-question feedback,
**so that** I understand which answers were correct and learn from my mistakes.

## Acceptance Criteria

1. **Given** a valid quiz_id and answers array,
   **When** I call POST /api/v1/quiz/{quiz_id}/submit with {"user_id": "user-42", "answers": [...]},
   **Then** I receive score, total, percentage, and a results array with correct (bool) and explanation per question.

2. **Given** an invalid quiz_id,
   **When** I submit answers,
   **Then** I receive HTTP 404.

3. **Given** a valid quiz submission,
   **When** the score is computed,
   **Then** the attempt is persisted in quiz_attempts table atomically.

4. **Given** a submission where the answer count doesn't match question count,
   **When** the request is validated,
   **Then** I receive HTTP 422 with a descriptive error.

5. **Given** a previous quiz submission,
   **When** I check GET /api/v1/progress/{user_id},
   **Then** the quiz score appears in the progress response.

## BRD & Design References

| BRD ID        | HLD/LLD Component                               |
|---------------|--------------------------------------------------|
| BRD-FR-006    | COMP-001/004 — POST /api/v1/quiz/{quiz_id}/submit|
| BRD-FR-011    | COMP-004 — persist quiz scores in SQLite         |
| BRD-NFR-012   | Data Layer — atomic quiz attempt persistence     |

## Tasks Breakdown

| Task ID    | Description                                       | Estimate |
|------------|---------------------------------------------------|----------|
| TASK-020   | Implement quiz scoring logic and submission route  | 3h       |

## UI/UX Notes

N/A — API only.

## Technical Notes

- **Stack:** Python / FastAPI / aiosqlite
- **Key considerations:** Fetch quiz from DB, compare answers positionally, compute score/percentage, persist with BEGIN TRANSACTION/COMMIT, return per-question feedback with explanations from stored quiz data
- **Configuration:** None specific

## Dependencies

- STORY-009 (quizzes must be generated and stored in DB)
- STORY-005 (database schema)

## Definition of Done

- [ ] Code implements all acceptance criteria
- [ ] Unit and integration tests written and passing
- [ ] API documentation updated (if applicable)
- [ ] Code reviewed and approved
- [ ] No regressions in existing tests

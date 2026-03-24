# Story: AI Quiz Generation

| Field        | Value                |
|--------------|----------------------|
| **Story ID** | STORY-009            |
| **Epic**     | EPIC-002             |
| **Status**   | Draft                |
| **Assignee** | develop-agent        |
| **Estimate** | L                    |
| **Priority** | P0                   |

## User Story

**As a** learner,
**I want** to generate a quiz for any lesson,
**so that** I can test my understanding with multiple-choice questions and receive explanations.

## Acceptance Criteria

1. **Given** a valid lesson ID,
   **When** I call POST /api/v1/lessons/{id}/quiz,
   **Then** I receive a quiz with 3-5 questions, each with question text, 4 options, correct_answer, and explanation.

2. **Given** a generated quiz,
   **When** I inspect the response,
   **Then** each question has exactly 4 options and the correct_answer is one of those options.

3. **Given** the AI returns malformed JSON,
   **When** schema validation fails,
   **Then** the system retries up to 2 times before returning HTTP 502.

4. **Given** a generated quiz,
   **When** it is returned to the client,
   **Then** it is also persisted in the quizzes table with a quiz_id.

5. **Given** an invalid lesson ID,
   **When** I call POST /api/v1/lessons/{id}/quiz,
   **Then** I receive HTTP 404 with a structured error.

## BRD & Design References

| BRD ID        | HLD/LLD Component                               |
|---------------|--------------------------------------------------|
| BRD-FR-005    | COMP-002 — POST /api/v1/lessons/{id}/quiz        |
| BRD-AI-002    | Content Service — quiz JSON generation           |
| BRD-AI-003    | Content Service — validate against schema        |
| BRD-AI-008    | Content Service — 4 options, 1 correct answer    |

## Tasks Breakdown

| Task ID    | Description                                           | Estimate |
|------------|-------------------------------------------------------|----------|
| TASK-016   | Implement quiz prompt template and validation schemas  | 2h       |
| TASK-017   | Implement ContentService.generate_quiz()               | 3h       |
| TASK-018   | Implement QuizRepository and quiz route handler        | 2h       |

## UI/UX Notes

N/A — API only.

## Technical Notes

- **Stack:** Python / FastAPI / httpx / GitHub Models API (GPT-4o)
- **Key considerations:** Quiz JSON must be validated with Pydantic before returning; retry up to 2 times on malformed responses; persist quiz in DB before returning; max_tokens=1500
- **Configuration:** QUIZ_MAX_TOKENS, PROMPTS_DIR

## Dependencies

- STORY-008 (GitHubModelsClient and PromptManager must exist)
- STORY-005 (database schema for quizzes table)

## Definition of Done

- [ ] Code implements all acceptance criteria
- [ ] Unit and integration tests written and passing
- [ ] API documentation updated (if applicable)
- [ ] Code reviewed and approved
- [ ] No regressions in existing tests

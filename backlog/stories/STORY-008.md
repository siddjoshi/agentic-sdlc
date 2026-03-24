# Story: AI Lesson Content Generation

| Field        | Value                |
|--------------|----------------------|
| **Story ID** | STORY-008            |
| **Epic**     | EPIC-002             |
| **Status**   | Draft                |
| **Assignee** | develop-agent        |
| **Estimate** | L                    |
| **Priority** | P0                   |

## User Story

**As a** learner,
**I want** to generate AI-powered lesson content for any lesson,
**so that** I receive up-to-date explanations and code examples tailored to my skill level.

## Acceptance Criteria

1. **Given** a valid lesson ID,
   **When** I call POST /api/v1/lessons/{id}/content,
   **Then** I receive Markdown-formatted content with 2-3 explanatory paragraphs and at least one code example.

2. **Given** a GitHub Actions lesson,
   **When** content is generated,
   **Then** the response contains YAML code blocks.

3. **Given** a GitHub Copilot lesson,
   **When** content is generated,
   **Then** the response contains Python or JavaScript code blocks.

4. **Given** an invalid lesson ID,
   **When** I call POST /api/v1/lessons/{id}/content,
   **Then** I receive HTTP 404 with a structured error.

5. **Given** the GitHub Models API is unavailable,
   **When** I call the content endpoint,
   **Then** I receive HTTP 503 with error_code, message, and retry_after.

## BRD & Design References

| BRD ID        | HLD/LLD Component                              |
|---------------|-------------------------------------------------|
| BRD-FR-004    | COMP-002 — POST /api/v1/lessons/{id}/content    |
| BRD-FR-015    | COMP-002 — Markdown with code blocks            |
| BRD-AI-001    | Content Service — structured prompt with topic   |
| BRD-AI-005    | Content Service — file-based prompt templates    |
| BRD-AI-007    | Content Service — topic-appropriate code         |
| BRD-AI-010    | Content Service — topic/level in every prompt    |

## Tasks Breakdown

| Task ID    | Description                                         | Estimate |
|------------|-----------------------------------------------------|----------|
| TASK-012   | Implement GitHubModelsClient (async HTTP wrapper)    | 3h       |
| TASK-013   | Implement PromptManager and prompt template files    | 2h       |
| TASK-014   | Implement ContentService.generate_lesson_content()   | 2h       |
| TASK-015   | Implement lesson content route handler               | 2h       |

## UI/UX Notes

N/A — API only.

## Technical Notes

- **Stack:** Python / FastAPI / httpx / GitHub Models API (GPT-4o)
- **Key considerations:** Prompt templates in prompts/ directory with {topic}, {level}, {objectives} placeholders; max_tokens=2000; 30s timeout; content must be Markdown
- **Configuration:** GITHUB_MODELS_API_KEY, GITHUB_MODELS_ENDPOINT, GITHUB_MODELS_MODEL, AI_REQUEST_TIMEOUT, LESSON_MAX_TOKENS

## Dependencies

- STORY-001 (project scaffolding)
- STORY-005 (database for lesson metadata lookup)
- STORY-006 (seed data for lesson records)

## Definition of Done

- [ ] Code implements all acceptance criteria
- [ ] Unit and integration tests written and passing
- [ ] API documentation updated (if applicable)
- [ ] Code reviewed and approved
- [ ] No regressions in existing tests

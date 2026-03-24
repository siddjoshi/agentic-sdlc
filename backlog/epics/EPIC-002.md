# Epic: AI Content Generation (GitHub Models Integration)

| Field       | Value                |
|-------------|----------------------|
| **Epic ID** | EPIC-002             |
| **Status**  | Draft                |
| **Owner**   | epic-and-tasks-agent |
| **Created** | 2026-03-24           |
| **Target**  | Sprint 1             |

## Goal / Objective

Integrate the GitHub Models API (GPT-4o) to dynamically generate lesson content and quizzes, with prompt template management, response validation, retry logic, and structured error handling.

## Business Value

AI-generated content is the platform's core differentiator — it enables on-demand, adaptive training material that stays current with GitHub's evolving tools, eliminating the need for manually authored courseware.

## BRD Requirements Mapped

| BRD ID       | Description                                                  |
|--------------|--------------------------------------------------------------|
| BRD-FR-004   | POST /api/v1/lessons/{id}/content — AI lesson generation     |
| BRD-FR-005   | POST /api/v1/lessons/{id}/quiz — AI quiz generation          |
| BRD-FR-015   | Lesson content as Markdown with code blocks                  |
| BRD-AI-001   | Structured prompts with topic, level, objectives to GPT-4o   |
| BRD-AI-002   | Quiz generation returning JSON array of questions            |
| BRD-AI-003   | Validate AI quiz responses against JSON schema               |
| BRD-AI-004   | Exponential backoff with jitter for rate limits              |
| BRD-AI-005   | Prompt templates as version-controlled files in prompts/     |
| BRD-AI-006   | HTTP 503 with structured error when AI unavailable           |
| BRD-AI-007   | Topic-appropriate code examples in generated content         |
| BRD-AI-008   | Each quiz question has exactly 4 options, 1 correct answer   |
| BRD-AI-009   | 30-second request timeout for AI API calls                   |
| BRD-AI-010   | Include topic and level in every AI prompt                   |
| BRD-NFR-002  | AI endpoints respond < 10 seconds                            |
| BRD-NFR-005  | Graceful handling of GitHub Models API failures              |
| BRD-NFR-008  | Log AI API call details at DEBUG level                       |

## Features

| Feature ID | Name                          | Priority (P0/P1/P2) | Status  |
|------------|-------------------------------|----------------------|---------|
| FEAT-006   | GitHub Models API Client      | P0                   | Planned |
| FEAT-007   | Prompt Template Management    | P0                   | Planned |
| FEAT-008   | Lesson Content Generation     | P0                   | Planned |
| FEAT-009   | Quiz Generation & Validation  | P0                   | Planned |
| FEAT-010   | Retry & Error Handling        | P0                   | Planned |

## Acceptance Criteria

1. POST /api/v1/lessons/{id}/content returns Markdown content with topic-appropriate code examples
2. POST /api/v1/lessons/{id}/quiz returns 3-5 valid multiple-choice questions with explanations
3. All AI responses are validated against Pydantic schemas before being returned to clients
4. Rate limit (429) responses trigger exponential backoff with jitter (up to 3 retries)
5. AI unavailability returns HTTP 503 with error_code, message, and retry_after fields
6. Prompt templates are loaded from prompts/ directory, not hardcoded in source

## Dependencies & Risks

**Dependencies:**
- EPIC-001 (course catalog must exist to look up lesson metadata for prompts)
- GitHub Models API access with valid GITHUB_MODELS_API_KEY
- httpx package for async HTTP calls

**Risks:**
- GitHub Models API rate limits may throttle generation during demos
- AI-generated quiz JSON may be malformed, requiring retry logic
- 30-second timeout may not be sufficient for complex content generation

## Out of Scope

- Content caching or offline fallback
- Alternative LLM providers
- Per-topic prompt template overrides (future iteration)

## Definition of Done

- [ ] All stories in this epic are Done
- [ ] Acceptance criteria verified
- [ ] API endpoints documented
- [ ] No critical or high-severity bugs open
- [ ] Demo-ready for stakeholder review

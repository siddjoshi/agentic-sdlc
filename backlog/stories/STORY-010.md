# Story: AI Retry & Error Handling

| Field        | Value                |
|--------------|----------------------|
| **Story ID** | STORY-010            |
| **Epic**     | EPIC-002             |
| **Status**   | Draft                |
| **Assignee** | develop-agent        |
| **Estimate** | M                    |
| **Priority** | P0                   |

## User Story

**As a** learner,
**I want** the platform to handle AI API failures gracefully with retries,
**so that** transient errors don't prevent me from generating content and I receive clear error messages when the service is unavailable.

## Acceptance Criteria

1. **Given** the GitHub Models API returns HTTP 429 (rate limit),
   **When** the client detects this,
   **Then** it retries with exponential backoff (1s, 2s, 4s) with ±500ms jitter, up to 3 retries.

2. **Given** the GitHub Models API returns HTTP 5xx,
   **When** all retries are exhausted,
   **Then** an HTTP 503 is returned with {"error": {"code": "AI_SERVICE_UNAVAILABLE", "message": "...", "retry_after": 30}}.

3. **Given** the API request exceeds 30 seconds,
   **When** the timeout fires,
   **Then** the request is treated as a 5xx error and follows the same error path.

4. **Given** a network connectivity failure,
   **When** the client cannot reach the GitHub Models API,
   **Then** an HTTP 503 is returned with a descriptive message.

5. **Given** any AI API interaction,
   **When** it completes,
   **Then** model, token count, and latency are logged at DEBUG level.

## BRD & Design References

| BRD ID        | HLD/LLD Component                              |
|---------------|-------------------------------------------------|
| BRD-AI-004    | Content Service — exponential backoff           |
| BRD-AI-006    | Content Service — 503 structured error          |
| BRD-AI-009    | Content Service — 30s timeout                   |
| BRD-NFR-005   | Graceful failure handling                       |
| BRD-NFR-008   | DEBUG-level AI call logging                     |

## Tasks Breakdown

| Task ID    | Description                                              | Estimate |
|------------|----------------------------------------------------------|----------|
| TASK-019   | Add retry logic with exponential backoff to AI client    | 3h       |

## UI/UX Notes

N/A — API only.

## Technical Notes

- **Stack:** Python / httpx
- **Key considerations:** Retry logic built into GitHubModelsClient.generate(); exponential backoff formula: delay = min(initial * 2^attempt, max_backoff) + random(-jitter, +jitter); never log API key values
- **Configuration:** AI_MAX_RETRIES, AI_INITIAL_BACKOFF, AI_MAX_BACKOFF, AI_BACKOFF_JITTER, AI_REQUEST_TIMEOUT

## Dependencies

- STORY-008 (GitHubModelsClient implementation)

## Definition of Done

- [ ] Code implements all acceptance criteria
- [ ] Unit and integration tests written and passing
- [ ] API documentation updated (if applicable)
- [ ] Code reviewed and approved
- [ ] No regressions in existing tests

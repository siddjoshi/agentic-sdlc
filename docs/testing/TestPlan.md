# Test Plan — AI-Powered Learning Platform

| Field         | Value                              |
|---------------|------------------------------------|
| **Version**   | 1.0                                |
| **Date**      | 2026-03-24                         |
| **Author**    | automation-test-agent              |
| **BRD Ref**   | BRD-LP-001                         |
| **Status**    | Complete                           |

---

## 1. Test Scope & Objectives

### 1.1 Scope

This test plan covers the MVP of the AI-powered learning platform built with Python, FastAPI, and the GitHub Models API. The MVP delivers personalised training content for three topics:

- GitHub Actions
- GitHub Copilot
- GitHub Advanced Security

**In scope:**
- FastAPI REST endpoints (course listing, lesson content generation, quiz generation, quiz submission, progress tracking, health check)
- Integration with GitHub Models API for content generation (mocked)
- Input validation and error handling
- API key authentication middleware
- Core business logic and data models
- Repository layer database operations
- AI response validation and retry logic

**Out of scope:**
- UI/frontend testing
- Load/performance testing
- End-to-end testing against live GitHub Models API
- Security penetration testing

### 1.2 Objectives

- Verify all 9 API endpoints return correct responses for valid and invalid inputs
- Confirm GitHub Models API integration produces expected learning content (via mocked responses)
- Validate business rules for the three MVP training topics
- Ensure error handling returns appropriate HTTP status codes and messages
- Achieve minimum code coverage target of 80%

---

## 2. Test Strategy

### 2.1 Unit Testing

| Aspect          | Detail                                                        |
|-----------------|---------------------------------------------------------------|
| **Scope**       | Individual functions, models, utility helpers, AI schemas      |
| **Framework**   | pytest                                                        |
| **Approach**    | Mock external dependencies (GitHub Models API, DB); test business logic in isolation |
| **Coverage**    | Target 80% line coverage                                      |

### 2.2 Integration Testing

| Aspect          | Detail                                                        |
|-----------------|---------------------------------------------------------------|
| **Scope**       | Interaction between modules — routes → services → repositories |
| **Framework**   | pytest + httpx (async)                                        |
| **Approach**    | Use FastAPI `AsyncClient`; mock only external AI API          |

### 2.3 API Testing

| Aspect          | Detail                                                        |
|-----------------|---------------------------------------------------------------|
| **Scope**       | All REST endpoints — happy path, edge cases, error responses  |
| **Framework**   | pytest + httpx                                                |
| **Approach**    | Validate status codes, response schemas, headers, auth flows  |

### 2.4 Content Generation Testing

| Aspect          | Detail                                                        |
|-----------------|---------------------------------------------------------------|
| **Scope**       | AI client, prompt building, quiz validation, retry logic       |
| **Framework**   | pytest + respx (mock httpx)                                   |
| **Approach**    | Mock GitHub Models API responses; test prompt construction, response parsing, error handling |

---

## 3. Test Environment

### 3.1 Local Development Setup

| Component               | Detail                                     |
|-------------------------|--------------------------------------------|
| **Python version**      | 3.11+                                      |
| **Virtual environment** | venv                                       |
| **Application server**  | Uvicorn (FastAPI)                          |
| **Database**            | SQLite (in-memory for tests via `:memory:`) |
| **External APIs**       | GitHub Models API (mocked with respx/unittest.mock) |

### 3.2 Dependencies

```
pytest
httpx
pytest-asyncio
pytest-cov
respx
```

### 3.3 Environment Variables

| Variable                    | Purpose                              | Test Value      |
|-----------------------------|--------------------------------------|-----------------|
| `API_KEY`                   | X-API-Key authentication             | `test-api-key`  |
| `GITHUB_MODELS_API_KEY`     | GitHub Models bearer token (mocked)  | `test-gh-key`   |
| `GITHUB_MODELS_ENDPOINT`    | GitHub Models base URL               | `https://models.test.ai/inference` |

---

## 4. Test Cases

| TC ID   | Description                                           | Type        | Input                              | Expected Output                                    | BRD/Story Ref | Status    |
|---------|-------------------------------------------------------|-------------|------------------------------------|----------------------------------------------------|----------------|-----------|
| TC-001  | Health check returns healthy status                   | API         | `GET /api/v1/health`               | 200 OK; `{status: "healthy", database: "connected"}` | BRD-FR-009, TASK-005 | Implemented |
| TC-002  | Health check accessible without auth                  | API         | `GET /api/v1/health` (no API key)  | 200 OK                                              | BRD-FR-013, TASK-004 | Implemented |
| TC-003  | List all courses                                      | API         | `GET /api/v1/courses`              | 200 OK; JSON array with 6 courses                   | BRD-FR-001, TASK-011 | Implemented |
| TC-004  | List courses with pagination                          | API         | `GET /api/v1/courses?limit=2&offset=0` | 200 OK; 2 courses returned, total=6             | BRD-FR-014, TASK-011 | Implemented |
| TC-005  | Get course details by valid ID                        | API         | `GET /api/v1/courses/1`            | 200 OK; course with lessons array                   | BRD-FR-002, TASK-011 | Implemented |
| TC-006  | Get course with non-existent ID returns 404           | API         | `GET /api/v1/courses/999`          | 404; error response                                 | BRD-FR-002, TASK-006 | Implemented |
| TC-007  | List lessons for a course                             | API         | `GET /api/v1/courses/1/lessons`    | 200 OK; ordered lessons                             | BRD-FR-003, TASK-011 | Implemented |
| TC-008  | List lessons for non-existent course returns 404      | API         | `GET /api/v1/courses/999/lessons`  | 404; error response                                 | BRD-FR-003, TASK-011 | Implemented |
| TC-009  | Generate lesson content (AI mocked)                   | Integration | `POST /api/v1/lessons/1/content`   | 200 OK; Markdown content                            | BRD-FR-004, TASK-015 | Implemented |
| TC-010  | Generate lesson for non-existent lesson returns 404   | API         | `POST /api/v1/lessons/999/content` | 404; error response                                 | BRD-FR-004, TASK-015 | Implemented |
| TC-011  | Generate quiz (AI mocked)                             | Integration | `POST /api/v1/lessons/1/quiz`      | 200 OK; quiz with 3-5 questions                     | BRD-FR-005, TASK-018 | Implemented |
| TC-012  | Submit quiz with correct answers                      | API         | `POST /api/v1/quiz/{id}/submit`    | 200 OK; score, results                              | BRD-FR-006, TASK-020 | Implemented |
| TC-013  | Submit quiz with wrong answer count returns 422       | API         | `POST /api/v1/quiz/{id}/submit`    | 422; validation error                               | BRD-FR-006, TASK-020 | Implemented |
| TC-014  | Submit quiz for non-existent quiz returns 404         | API         | `POST /api/v1/quiz/999/submit`     | 404; error response                                 | BRD-FR-006, TASK-020 | Implemented |
| TC-015  | Get user progress                                     | API         | `GET /api/v1/progress/user-1`      | 200 OK; courses with progress data                  | BRD-FR-007, TASK-022 | Implemented |
| TC-016  | Mark lesson complete                                  | API         | `POST /api/v1/progress/user-1/complete` | 200 OK; completion confirmed                   | BRD-FR-008, TASK-021 | Implemented |
| TC-017  | Mark lesson complete is idempotent                    | API         | `POST` twice with same data        | Both return 200; progress shows 1 completion        | BRD-FR-008, TASK-021 | Implemented |
| TC-018  | Mark non-existent lesson complete returns 404         | API         | `POST /api/v1/progress/user-1/complete` | 404; error response                            | BRD-FR-008, TASK-021 | Implemented |
| TC-019  | Unauthenticated request returns 401                   | API         | Request without X-API-Key          | 401 Unauthorized                                    | BRD-FR-013, TASK-004 | Implemented |
| TC-020  | Invalid API key returns 401                           | API         | Request with wrong X-API-Key       | 401 Unauthorized                                    | BRD-FR-013, TASK-004 | Implemented |
| TC-021  | Quiz validation: exactly 4 options                    | Unit        | QuizQuestion with 3 options        | Validation error                                    | BRD-AI-008, TASK-016 | Implemented |
| TC-022  | Quiz validation: correct_answer in options            | Unit        | correct_answer not in options      | Validation error                                    | BRD-AI-008, TASK-016 | Implemented |
| TC-023  | Quiz validation: 3-5 questions enforced               | Unit        | Quiz with 2 or 6 questions         | Validation error                                    | BRD-AI-003, TASK-016 | Implemented |
| TC-024  | AI client handles 429 with retry                      | Unit        | Mocked 429 response                | AIRateLimitError after retries                      | BRD-AI-004, TASK-019 | Implemented |
| TC-025  | AI client handles 5xx with retry                      | Unit        | Mocked 500 response                | AIServiceUnavailableError after retries             | BRD-AI-006, TASK-019 | Implemented |
| TC-026  | AI client handles timeout with retry                  | Unit        | Mocked timeout                     | AIServiceUnavailableError after retries             | BRD-AI-009, TASK-019 | Implemented |
| TC-027  | Prompt manager builds lesson prompt                   | Unit        | Topic, level, objectives           | Correct message list with placeholders filled       | BRD-AI-005, TASK-013 | Implemented |
| TC-028  | Prompt manager builds quiz prompt                     | Unit        | Topic, level, num_questions        | Correct message list                                | BRD-AI-005, TASK-013 | Implemented |
| TC-029  | Content service generates lesson content              | Unit        | Mocked AI client                   | Dict matching LessonContentResponse                 | BRD-FR-004, TASK-014 | Implemented |
| TC-030  | Content service retries quiz on validation failure    | Unit        | Mocked invalid then valid AI resp  | Quiz returned after retry                           | BRD-AI-003, TASK-017 | Implemented |
| TC-031  | Request/response model validation                     | Unit        | Various Pydantic models            | Correct validation behavior                         | BRD-NFR-009, TASK-006 | Implemented |
| TC-032  | Database models mirror table schemas                  | Unit        | CourseRow, LessonRow, etc.         | Valid model creation                                | BRD-NFR-010, TASK-008 | Implemented |

---

## 5. Test Data Requirements

| Data Category          | Description                                               | Source           |
|------------------------|-----------------------------------------------------------|------------------|
| Training topics        | Seed data for 6 courses (3 topics × 2 levels)            | Database seed (conftest.py) |
| User accounts          | Test user IDs (`test-user-1`, `test-user-2`)              | Fixtures         |
| API responses          | Mocked GitHub Models API responses                        | conftest.py mock fixtures |
| Invalid inputs         | Missing fields, wrong types, boundary values              | Parameterised fixtures |
| Quiz data              | Pre-seeded quiz with known questions for scoring tests    | conftest.py      |

---

## 6. Entry / Exit Criteria

### 6.1 Entry Criteria

- [x] Application builds and starts without errors
- [x] Test environment provisioned with required dependencies
- [x] Test data and fixtures are available
- [x] All external API mocks are configured and verified

### 6.2 Exit Criteria

- [x] All critical and high-priority test cases pass
- [x] Code coverage ≥ 80%
- [x] No open Severity 1 or Severity 2 defects
- [x] API contract tests pass for all 9 endpoints
- [x] All 32 test cases implemented and passing

---

## 7. Defect Management

### 7.1 Severity Levels

| Severity | Definition                                                     | Example                                    |
|----------|----------------------------------------------------------------|--------------------------------------------|
| **S1 — Critical** | System crash, data loss, security vulnerability        | API returns 500 on all requests            |
| **S2 — High**     | Major feature broken, no workaround                   | Content generation fails for a topic       |
| **S3 — Medium**   | Feature impaired but workaround exists                | Progress not saved on first attempt        |
| **S4 — Low**      | Minor issue, cosmetic, or edge case                   | Inconsistent error message wording         |

### 7.2 Defect Workflow

```
New → Triaged → In Progress → Fixed → Verified → Closed
                                   ↘ Won't Fix
```

- Defects tracked in: GitHub Issues with `bug` label
- Retest owner: automation-test-agent

---

## 8. Tools & Frameworks

| Tool / Framework | Purpose                                          |
|------------------|--------------------------------------------------|
| **pytest**       | Test runner and assertion framework              |
| **httpx**        | Async HTTP client for API testing                |
| **pytest-asyncio** | Async test support for FastAPI                 |
| **pytest-cov**   | Code coverage reporting                          |
| **respx**        | Mock httpx requests (GitHub Models API stubs)    |
| **unittest.mock** | Additional mocking for service/repository layer |

---

## 9. Traceability Matrix

| BRD Requirement          | Story/Task              | Test Cases                        | Status    |
|--------------------------|-------------------------|-----------------------------------|-----------|
| BRD-FR-001: Course listing | STORY-007 / TASK-011  | TC-003, TC-004                    | Implemented |
| BRD-FR-002: Course details | STORY-007 / TASK-011  | TC-005, TC-006                    | Implemented |
| BRD-FR-003: Lesson listing | STORY-007 / TASK-011  | TC-007, TC-008                    | Implemented |
| BRD-FR-004: Lesson content gen | STORY-008 / TASK-015 | TC-009, TC-010                  | Implemented |
| BRD-FR-005: Quiz generation | STORY-009 / TASK-018  | TC-011                            | Implemented |
| BRD-FR-006: Quiz submission | STORY-010 / TASK-020  | TC-012, TC-013, TC-014            | Implemented |
| BRD-FR-007: Progress tracking | STORY-013 / TASK-022 | TC-015                           | Implemented |
| BRD-FR-008: Lesson completion | STORY-012 / TASK-021 | TC-016, TC-017, TC-018           | Implemented |
| BRD-FR-009: Health check | STORY-003 / TASK-005    | TC-001, TC-002                    | Implemented |
| BRD-FR-013: Authentication | STORY-002 / TASK-004   | TC-002, TC-019, TC-020            | Implemented |
| BRD-FR-014: Pagination   | STORY-007 / TASK-011    | TC-004                            | Implemented |
| BRD-AI-003: Quiz validation | STORY-009 / TASK-016  | TC-021, TC-022, TC-023            | Implemented |
| BRD-AI-004: Retry/backoff | STORY-008 / TASK-019   | TC-024, TC-025, TC-026            | Implemented |
| BRD-AI-005: Prompt templates | STORY-008 / TASK-013  | TC-027, TC-028                    | Implemented |
| BRD-NFR-009: Input validation | TASK-006              | TC-031                            | Implemented |

---

## 10. Risks & Assumptions

### 10.1 Risks

| Risk                                              | Impact | Likelihood | Mitigation                                       |
|---------------------------------------------------|--------|------------|--------------------------------------------------|
| GitHub Models API rate limits during testing       | High   | Medium     | Use mocked/recorded responses in all tests       |
| Non-deterministic AI responses complicate assertions | Medium | High     | Assert on structure/schema rather than exact content |
| Test environment drift from production config      | Medium | Low        | Use environment variable overrides in conftest.py |
| SQLite in-memory DB behavior differs from file DB  | Low    | Low        | Use same schema and seed data as production       |

### 10.2 Assumptions

- GitHub Models API remains backward-compatible during MVP development
- Three MVP topics (Actions, Copilot, Advanced Security) are finalised
- pytest and httpx are the agreed-upon testing stack
- SQLite in-memory database is sufficient for test isolation
- All tests run with mocked external API calls (no network required)

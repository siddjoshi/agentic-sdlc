# Business Requirements Document (BRD)

| Field       | Value                                                        |
|-------------|--------------------------------------------------------------|
| **Title**   | AI-Powered Learning Platform for GitHub Technologies         |
| **Version** | 1.0                                                          |
| **Date**    | 2026-03-24                                                   |
| **Author**  | requirement-agent                                            |
| **Status**  | Draft                                                        |

---

## 1. Executive Summary

### 1.1 Project Overview

The AI-Powered Learning Platform is an interactive training application that helps organizations upskill developers on three core GitHub technologies: **GitHub Actions**, **GitHub Copilot**, and **GitHub Advanced Security**. The platform leverages the **GitHub Models API (GPT-4o)** to dynamically generate lesson content, runnable code examples, and knowledge-assessment quizzes. Built with a **Python + FastAPI** backend and a lightweight HTML/JS frontend, the MVP targets local development environments, enabling rapid iteration and validation before any cloud deployment.

The core problem being solved is the lack of adaptive, AI-driven training content for GitHub's developer tooling. Traditional static documentation and slide decks fail to keep pace with rapidly evolving features. This platform generates fresh, context-aware learning material on demand, personalised to the learner's current level.

### 1.2 Business Objectives

- **BO-1**: Accelerate developer onboarding for GitHub Actions, Copilot, and Advanced Security by providing AI-generated, interactive training content.
- **BO-2**: Reduce training content creation effort by 80% compared to manually authored courseware through automated lesson and quiz generation.
- **BO-3**: Enable measurable skill assessment via auto-generated quizzes with immediate, AI-powered explanations of correct and incorrect answers.
- **BO-4**: Deliver a working MVP suitable for local demonstration and stakeholder validation within a single development sprint.

### 1.3 Success Metrics / KPIs

| Metric ID | Metric                                  | Target                  | Measurement Method                                      |
|-----------|-----------------------------------------|-------------------------|---------------------------------------------------------|
| KPI-001   | Lesson content generation success rate  | >= 95% of requests      | Ratio of successful AI responses to total requests      |
| KPI-002   | Quiz generation validity                | 100% well-formed JSON   | Automated schema validation on every quiz response      |
| KPI-003   | API response time (non-AI endpoints)    | < 2 seconds             | Automated latency measurement on health/catalog calls   |
| KPI-004   | API response time (AI generation)       | < 10 seconds            | Automated latency measurement on content/quiz endpoints |
| KPI-005   | Course catalog completeness             | 3 courses, 30+ lessons  | Manual audit of seed data                               |
| KPI-006   | Progress tracking accuracy              | 100% data consistency   | Unit tests verifying completion and score persistence   |

---

## 2. Background & Context

GitHub is the world's largest software development platform, and its ecosystem of developer tools -- Actions for CI/CD, Copilot for AI-assisted coding, and Advanced Security for vulnerability management -- is rapidly expanding. Organizations adopting these tools face a persistent training gap: official documentation is extensive but static, and third-party courses quickly become outdated.

AI-powered content generation offers a solution. By combining curated learning objectives with the generative capabilities of large language models, the platform can produce up-to-date explanations, realistic code examples, and adaptive assessments on demand. The GitHub Models API provides a convenient, GitHub-native inference endpoint, eliminating the need for separate AI infrastructure.

This MVP validates the core hypothesis: that AI-generated training content, structured around a progressive curriculum, can deliver an effective and engaging learning experience for developers at varying skill levels.

---

## 3. Stakeholders

| Name                | Role                    | Interest                                                        | Influence |
|---------------------|-------------------------|-----------------------------------------------------------------|-----------|
| Engineering Lead    | Technical Decision Maker| Architecture integrity, API design quality, code maintainability| High      |
| Product Owner       | Business Sponsor        | Feature completeness, MVP scope alignment, demo readiness       | High      |
| Learner (Developer) | Primary End User        | Quality of content, quiz relevance, progress visibility         | High      |
| Training Manager    | Secondary End User      | Course catalog overview, learner progress monitoring            | Medium    |
| Platform Admin      | Operations User         | System health, configuration management, API key security       | Medium    |
| QA / Test Engineer  | Quality Assurance       | Testability of requirements, acceptance criteria clarity         | Medium    |

---

## 4. Scope

### 4.1 In-Scope

- FastAPI REST API with all MVP endpoints (course catalog, lesson generation, quiz generation, progress tracking, health check)
- AI-powered lesson content generation via GitHub Models API (GPT-4o)
- AI-powered quiz generation with multiple-choice questions, correct answers, and explanations
- Three training courses: GitHub Actions, GitHub Copilot, GitHub Advanced Security
- Two skill levels per course: Beginner and Intermediate (5-8 lessons per level)
- SQLite-based persistence for user progress and quiz scores
- Simple API key authentication for endpoint access
- Health check endpoint for operational monitoring
- Basic error handling with graceful degradation when the AI API is unavailable
- Local development environment only

### 4.2 Out-of-Scope

- Cloud deployment (AWS, Azure, GCP) and production infrastructure
- OAuth / SSO / multi-factor authentication
- Multi-tenancy and organization-level isolation
- Advanced content caching or CDN integration
- Real-time collaborative features
- Mobile-native applications
- Admin UI for course authoring or curriculum management
- Integration with external LMS platforms (e.g., Moodle, Canvas)
- Billing or subscription management
- Internationalisation / multi-language support

### 4.3 Assumptions

- A-1: Developers running the platform locally have a valid GitHub account with access to the GitHub Models API.
- A-2: The `GITHUB_MODELS_API_KEY` environment variable is provisioned before application startup.
- A-3: GPT-4o is available via the GitHub Models API with sufficient rate limits for development and demo usage.
- A-4: Users interact with the API via a browser-based frontend or API client (e.g., curl, Postman); no CLI interface is required.
- A-5: SQLite is adequate for MVP data volumes (single user or small team).

### 4.4 Constraints

- C-1: All AI inference must use the GitHub Models API exclusively; no alternative LLM providers.
- C-2: The backend must be implemented in Python using the FastAPI framework.
- C-3: Data persistence must use SQLite (no external database services).
- C-4: The API key must never be hardcoded in source code; it must be read from the `GITHUB_MODELS_API_KEY` environment variable.
- C-5: The platform is designed for local development only; no load balancing or horizontal scaling.

### 4.5 Dependencies

- D-1: GitHub Models API availability and rate limits (external service dependency).
- D-2: Python 3.10+ runtime environment on the developer's machine.
- D-3: Network connectivity for API calls to the GitHub Models endpoint.
- D-4: FastAPI and Uvicorn packages available via PyPI.

---

## 5. Use Cases

| Use Case ID | Name                              | Description                                                                                                             | Priority    | Actors              |
|-------------|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------|-------------|----------------------|
| UC-001      | Browse Course Catalog             | A Learner views the list of available courses (Actions, Copilot, Security) and selects one to see its lesson outline.   | Must-Have   | Learner              |
| UC-002      | Generate and View Lesson Content  | A Learner requests AI-generated lesson content for a specific lesson, receiving explanations and code examples.         | Must-Have   | Learner              |
| UC-003      | Take a Quiz                       | A Learner generates a quiz for a completed lesson, answering multiple-choice questions and receiving a score with explanations. | Must-Have   | Learner              |
| UC-004      | Submit Quiz Answers               | A Learner submits quiz answers and receives their score, correct answers, and AI-generated explanations for each question. | Must-Have   | Learner              |
| UC-005      | Track Learning Progress           | A Learner views their progress across all courses, including completed lessons and quiz scores.                          | Must-Have   | Learner              |
| UC-006      | Mark Lesson Completed             | A Learner marks a lesson as completed, updating their progress record.                                                  | Must-Have   | Learner              |
| UC-007      | Monitor Learner Progress          | A Training Manager retrieves progress data for a specific user to assess their learning status.                          | Should-Have | Training Manager     |
| UC-008      | Check System Health               | A Platform Admin calls the health endpoint to verify the API is running and dependencies are reachable.                  | Must-Have   | Platform Admin       |
| UC-009      | Handle AI API Unavailability      | The system gracefully degrades when the GitHub Models API is unavailable, returning informative error messages or fallback content. | Must-Have   | System               |

---

## 6. Functional Requirements

| Req ID      | Description                                                                                                                                       | Priority    | Acceptance Criteria                                                                                                                                      |
|-------------|---------------------------------------------------------------------------------------------------------------------------------------------------|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| BRD-FR-001  | The system shall expose `GET /api/v1/courses` returning a JSON array of all available courses with `id`, `title`, `description`, and `level` fields. | Must-Have   | A GET request returns HTTP 200 with a JSON array containing exactly 3 courses (Actions, Copilot, Security). Each object includes `id`, `title`, `description`, and `level`. |
| BRD-FR-002  | The system shall expose `GET /api/v1/courses/{id}` returning course details including the lesson outline for the specified course.                | Must-Have   | A GET request with a valid course ID returns HTTP 200 with course metadata and a `lessons` array. An invalid ID returns HTTP 404 with an error message.   |
| BRD-FR-003  | The system shall expose `GET /api/v1/courses/{id}/lessons` returning a JSON array of lessons for the specified course, ordered by sequence.       | Must-Have   | A GET request returns HTTP 200 with an ordered list of lessons containing `id`, `title`, `level`, and `order`. An invalid course ID returns HTTP 404.     |
| BRD-FR-004  | The system shall expose `POST /api/v1/lessons/{id}/content` that generates AI-powered lesson content via the GitHub Models API.                   | Must-Have   | A POST request returns HTTP 200 with Markdown-formatted content containing 2-3 explanatory paragraphs and at least one code example. Response time < 10s. |
| BRD-FR-005  | The system shall expose `POST /api/v1/lessons/{id}/quiz` that generates a multiple-choice quiz via the GitHub Models API.                         | Must-Have   | A POST request returns HTTP 200 with a JSON object containing an array of 3-5 questions, each with `question`, `options[]` (4 choices), `correct_answer`, and `explanation`. |
| BRD-FR-006  | The system shall expose `POST /api/v1/quiz/{quiz_id}/submit` accepting an array of user answers and returning a score with per-question feedback.  | Must-Have   | A POST request with valid answers returns HTTP 200 with `score`, `total`, `percentage`, and a `results[]` array with `correct` (boolean) and `explanation` per question. Invalid quiz ID returns HTTP 404. |
| BRD-FR-007  | The system shall expose `GET /api/v1/progress/{user_id}` returning the user's progress across all courses.                                       | Must-Have   | A GET request returns HTTP 200 with per-course progress including `completed_lessons`, `total_lessons`, `quiz_scores[]`, and `completion_percentage`.      |
| BRD-FR-008  | The system shall expose `POST /api/v1/progress/{user_id}/complete` to mark a specific lesson as completed for a user.                             | Must-Have   | A POST request with `lesson_id` in the body returns HTTP 200 and persists the completion. Subsequent GET progress reflects the update. Duplicate completions are idempotent. |
| BRD-FR-009  | The system shall expose `GET /api/v1/health` returning the operational status of the API and its dependencies.                                    | Must-Have   | A GET request returns HTTP 200 with `{"status": "healthy", "version": "1.0.0", "database": "connected"}`. If the database is unreachable, status is `"degraded"`. |
| BRD-FR-010  | The system shall seed the database with course and lesson metadata for all three training topics at startup.                                      | Must-Have   | On application startup, the `courses` and `lessons` tables contain pre-populated records for GitHub Actions, GitHub Copilot, and GitHub Advanced Security with correct levels and ordering. |
| BRD-FR-011  | The system shall persist quiz scores in SQLite, associated with the user ID and lesson ID.                                                        | Must-Have   | After a quiz submission, the score is retrievable via the progress endpoint. Scores persist across application restarts.                                   |
| BRD-FR-012  | The system shall validate all request inputs (path parameters, request bodies) and return HTTP 422 with descriptive error messages for invalid input. | Must-Have   | Sending a non-integer course ID returns HTTP 422. Sending a quiz submission with missing fields returns HTTP 422 with field-level error details.           |
| BRD-FR-013  | The system shall support simple API key authentication via an `X-API-Key` header on all endpoints except `/api/v1/health`.                        | Should-Have | Requests without a valid `X-API-Key` header return HTTP 401. The health endpoint is accessible without authentication.                                    |
| BRD-FR-014  | The system shall include pagination support on list endpoints (`courses`, `lessons`) via `limit` and `offset` query parameters.                   | Should-Have | Passing `?limit=2&offset=0` returns the first 2 results. Default limit is 20. Response includes `total` count.                                            |
| BRD-FR-015  | The system shall return lesson content as Markdown with properly formatted code blocks using language-specific syntax highlighting hints.          | Must-Have   | Generated lesson content for GitHub Actions includes YAML code blocks. Content for Copilot includes Python/JS code blocks. Content for Security includes YAML and code blocks. |

---

## 7. Non-Functional Requirements

| Req ID       | Category       | Description                                                                                                      | Target                                       |
|--------------|----------------|------------------------------------------------------------------------------------------------------------------|----------------------------------------------|
| BRD-NFR-001  | Performance    | Non-AI API endpoints (catalog, progress, health) shall respond within 2 seconds under normal load.               | < 2 seconds (p95 latency)                   |
| BRD-NFR-002  | Performance    | AI content and quiz generation endpoints shall respond within 10 seconds, including GitHub Models API round-trip. | < 10 seconds (p95 latency)                  |
| BRD-NFR-003  | Security       | The GitHub Models API key shall be read exclusively from the `GITHUB_MODELS_API_KEY` environment variable and never logged, echoed, or included in API responses. | Zero occurrences of API key in logs/responses |
| BRD-NFR-004  | Security       | All API endpoints (except health) shall require a valid API key in the `X-API-Key` header.                        | 100% of protected endpoints enforce auth     |
| BRD-NFR-005  | Reliability    | The system shall handle GitHub Models API failures gracefully, returning an HTTP 503 with a descriptive error message and retry guidance. | Zero unhandled exceptions from API failures  |
| BRD-NFR-006  | Reliability    | SQLite database operations shall use WAL mode and proper transaction management to prevent data corruption.        | Zero data corruption incidents               |
| BRD-NFR-007  | Logging        | The system shall log all API requests with method, path, status code, and response time at INFO level.            | 100% of requests logged                     |
| BRD-NFR-008  | Logging        | The system shall log AI API call details (model, token count, latency) at DEBUG level for troubleshooting.        | All AI calls logged at DEBUG                 |
| BRD-NFR-009  | Validation     | All user-facing input shall be validated using Pydantic models with type checking and constraint enforcement.      | 100% of endpoints use Pydantic validation    |
| BRD-NFR-010  | Maintainability| The codebase shall follow a modular structure with separate modules for routes, services, models, and AI integration. | Clear separation of concerns verified by review |
| BRD-NFR-011  | Testability    | Every functional requirement shall have at least one corresponding automated test (unit or integration).           | >= 1 test per BRD-FR requirement             |
| BRD-NFR-012  | Data Integrity | Quiz scores and progress records shall be persisted atomically; partial writes shall be rolled back.               | Zero partial-write scenarios in tests        |

---

## 8. GitHub Models Integration Requirements

This section captures requirements specific to the platform's use of the GitHub Models API for AI-driven learning features.

| Req ID       | Description                                                                                                             | Priority    | Notes                                                                                        |
|--------------|-------------------------------------------------------------------------------------------------------------------------|-------------|----------------------------------------------------------------------------------------------|
| BRD-AI-001   | The system shall generate lesson content by sending a structured prompt containing the topic, level, and learning objectives to GPT-4o via the GitHub Models API. | Must-Have   | Model: GPT-4o. Prompt includes topic name, skill level, and 2-3 learning objectives. Max tokens: 2000. |
| BRD-AI-002   | The system shall generate quiz questions by sending topic context and difficulty level to GPT-4o, receiving a JSON array of `{question, options[], correct_answer, explanation}`. | Must-Have   | Response must be parseable JSON. Each quiz contains 3-5 questions. Max tokens: 1500.          |
| BRD-AI-003   | The system shall validate all AI-generated quiz responses against a JSON schema before returning them to the client.      | Must-Have   | Malformed responses trigger a retry (up to 2 retries) before returning an error.              |
| BRD-AI-004   | The system shall implement exponential backoff with jitter for HTTP 429 (rate limit) responses from the GitHub Models API. | Must-Have   | Initial delay: 1s. Max retries: 3. Max delay: 30s. Jitter: +/-500ms.                        |
| BRD-AI-005   | The system shall store prompt templates as separate, version-controlled text files (not inline strings) in a `prompts/` directory. | Must-Have   | Templates use Python string formatting placeholders for topic, level, and objectives.          |
| BRD-AI-006   | The system shall return a structured error response (HTTP 503) with a user-friendly message when the GitHub Models API is unreachable or returns 5xx errors. | Must-Have   | Error response includes `error_code`, `message`, and `retry_after` fields.                    |
| BRD-AI-007   | Generated lesson content shall contain topic-appropriate code examples: YAML for Actions, Python/JS for Copilot, and YAML/CodeQL for Security. | Must-Have   | Verified by content inspection: each generated lesson includes at least one code block.       |
| BRD-AI-008   | Each AI-generated quiz question shall have exactly 4 answer options with exactly 1 correct answer.                        | Must-Have   | Schema validation enforces `options` array length = 4 and `correct_answer` is in `options`.   |
| BRD-AI-009   | The system shall set a request timeout of 30 seconds for all GitHub Models API calls to prevent hung connections.          | Should-Have | Timeout triggers the same error path as a 5xx response.                                       |
| BRD-AI-010   | The system shall include the lesson's topic and level in every AI prompt to ensure content is appropriately scoped.        | Must-Have   | Prompt templates are parameterised with `{topic}`, `{level}`, and `{objectives}` variables.   |

### Integration Considerations

- **Model Selection**: GPT-4o via the GitHub Models API is selected for its strong instruction-following capability, code generation quality, and JSON output reliability. It provides the best balance of quality and speed for educational content generation.
- **Rate Limits & Quotas**: Development usage is expected to be low-volume (< 100 requests/hour). The exponential backoff strategy (BRD-AI-004) handles transient rate limits. For demo scenarios, content can be pre-generated and cached manually.
- **Prompt Management**: All prompts are stored as template files in the `prompts/` directory (BRD-AI-005), version-controlled alongside application code. This enables prompt iteration without code changes and supports future A/B testing of prompt variants.
- **Fallback Strategy**: When the GitHub Models API is unavailable (network error, 5xx, timeout), the system returns HTTP 503 with a structured error (BRD-AI-006). The MVP does not implement content caching; future iterations may add a local cache of previously generated content as a fallback.

---

## 9. Risks & Mitigations

| Risk ID | Description                                                                                 | Likelihood | Impact | Mitigation Strategy                                                                                              |
|---------|---------------------------------------------------------------------------------------------|------------|--------|------------------------------------------------------------------------------------------------------------------|
| R-001   | GitHub Models API rate limits may throttle content generation during demos or heavy usage.   | Medium     | High   | Implement exponential backoff (BRD-AI-004). Pre-generate demo content. Monitor rate limit headers in responses.   |
| R-002   | AI-generated content may contain inaccuracies or outdated information about GitHub features. | Medium     | High   | Include disclaimers in generated content. Use specific, constrained prompts with version references. Plan for human review in post-MVP. |
| R-003   | AI-generated quiz JSON may be malformed or fail schema validation.                           | Medium     | Medium | Validate all AI responses against JSON schema (BRD-AI-003). Implement retry logic (up to 2 retries). Return clear error on persistent failure. |
| R-004   | GitHub Models API may experience downtime, blocking all content generation.                  | Low        | High   | Return HTTP 503 with informative error (BRD-AI-006). Document that MVP has no offline fallback; plan caching for v2. |
| R-005   | SQLite may not handle concurrent access if multiple users access the local instance.         | Low        | Medium | Use WAL mode (BRD-NFR-006). Document single-user/small-team limitation. Plan migration to PostgreSQL for production. |
| R-006   | API key exposure through logs, error messages, or source code.                               | Low        | High   | Enforce env-var-only key access (BRD-NFR-003). Add log sanitisation. Include API key leak checks in code review. |
| R-007   | Prompt injection via user-controlled input fields passed to the AI model.                    | Medium     | Medium | Sanitise all user inputs before prompt construction. Use structured prompt templates with clear system/user message boundaries. |
| R-008   | Scope creep delays MVP delivery due to feature additions beyond the defined scope.           | Medium     | Medium | Strictly enforce In-Scope / Out-of-Scope boundaries. Defer all non-MVP features to a backlog for future sprints. |

---

## 10. Appendix

### 10.1 Glossary

| Term                     | Definition                                                                                                                                       |
|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| GitHub Models API        | A GitHub-hosted inference endpoint that provides access to large language models (e.g., GPT-4o) for generating text, code, and structured outputs. |
| GitHub Actions           | GitHub's built-in CI/CD platform that enables automated workflows triggered by repository events, defined in YAML configuration files.            |
| GitHub Copilot           | An AI-powered coding assistant that provides code suggestions, completions, and chat-based help directly within supported IDEs.                   |
| GitHub Advanced Security | A suite of security features including CodeQL code scanning, secret scanning, Dependabot alerts, and push protection for vulnerability management.|
| FastAPI                  | A modern, high-performance Python web framework for building REST APIs, based on standard Python type hints and asynchronous request handling.    |
| SQLite                   | A lightweight, file-based relational database engine that requires no separate server process, suitable for local and embedded applications.      |
| GPT-4o                   | A multimodal large language model by OpenAI, accessed via the GitHub Models API, capable of generating text, code, and structured JSON outputs.   |
| Pydantic                 | A Python data validation library that uses type annotations to enforce data schemas, used extensively in FastAPI for request/response validation.  |
| Exponential Backoff      | A retry strategy where the wait time between retries increases exponentially, often with random jitter, to reduce load on rate-limited services.  |
| WAL Mode                 | Write-Ahead Logging mode in SQLite, which improves concurrency by allowing readers to operate concurrently with a single writer.                  |

### 10.2 References

- GitHub Models API Documentation: https://docs.github.com/en/github-models
- GitHub Actions Documentation: https://docs.github.com/en/actions
- GitHub Copilot Documentation: https://docs.github.com/en/copilot
- GitHub Advanced Security Documentation: https://docs.github.com/en/code-security
- FastAPI Documentation: https://fastapi.tiangolo.com/
- SQLite Documentation: https://www.sqlite.org/docs.html
- Pydantic Documentation: https://docs.pydantic.dev/

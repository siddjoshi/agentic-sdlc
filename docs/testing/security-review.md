# Security Review — AI-Powered Learning Platform

| Field            | Value                                   |
|------------------|-----------------------------------------|
| **Version**      | 1.0                                     |
| **Date**         | 2026-03-24                              |
| **Reviewer**     | security-agent                          |
| **HLD Ref**      | HLD v1.0 (COMP-001 – COMP-005)         |
| **LLD Ref**      | api-layer.md, content-service.md, data-layer.md |
| **Status**       | Complete                                |

---

## 1. Review Scope

### 1.1 Components Reviewed

| Component                      | Description                                           | Reviewed |
|--------------------------------|-------------------------------------------------------|----------|
| FastAPI application layer      | REST endpoints, middleware, request handling           | [x]      |
| GitHub Models API integration  | Outbound calls, API key usage, response handling      | [x]      |
| Authentication & authorisation | API key validation, path exemptions                   | [x]      |
| Data models & persistence      | ORM models, database queries, data sanitisation       | [x]      |
| Configuration & secrets        | Environment variables, config files, secret storage   | [x]      |
| CI/CD pipeline                 | GitHub Actions workflows, build/deploy security       | [x]      |
| Dependencies                   | Third-party packages and their known vulnerabilities  | [x]      |

### 1.2 Out of Scope

- Frontend/UI (COMP-005) — not yet implemented beyond static file serving
- Infrastructure hardening and cloud deployment
- Penetration testing
- Performance/load testing

---

## 2. Threat Model Summary

### 2.1 Assets

| Asset                            | Sensitivity | Description                                    |
|----------------------------------|-------------|------------------------------------------------|
| GitHub Models API key            | High        | Grants access to AI model; abuse = cost + data exposure |
| Application API key              | High        | Authenticates all non-health API requests      |
| Learning content (AI-generated)  | Medium      | Generated training material for 3 MVP topics   |
| User progress data               | Medium      | Tracks completion across topics, quiz scores   |
| Application source code          | Medium      | Business logic, API contracts                  |
| SQLite database file             | Medium      | Contains all persisted data for the platform   |

### 2.2 Trust Boundaries

```
[User/Browser] ──HTTP──▶ [FastAPI Application] ──HTTPS──▶ [GitHub Models API]
                                    │
                                    ▼
                              [SQLite DB]
```

- **Boundary 1:** User → FastAPI (untrusted input crosses into application)
- **Boundary 2:** FastAPI → GitHub Models API (application secrets cross to external service)
- **Boundary 3:** FastAPI → SQLite (queries constructed from user-influenced data)

### 2.3 Threat Actors

| Actor               | Motivation                          | Capability |
|----------------------|-------------------------------------|------------|
| External attacker    | Data theft, API abuse, disruption   | Medium     |
| Malicious user       | Prompt injection, free-tier abuse   | Low–Medium |
| Supply chain threat  | Compromised dependency              | Low        |

---

## 3. OWASP Top 10 Assessment

| #    | OWASP Category                          | Finding                                                                 | Severity | Status       | Remediation                                                 |
|------|-----------------------------------------|-------------------------------------------------------------------------|----------|--------------|-------------------------------------------------------------|
| A01  | Broken Access Control                   | Any valid API key holder can access/modify any user's progress via `user_id` path parameter (IDOR). No ownership enforcement. | Medium   | Open         | Implement user-scoped tokens or validate API key → user mapping. See SEC-001. |
| A02  | Cryptographic Failures                  | No encryption at rest for SQLite DB. No HTTPS enforcement (expected for MVP local-only). API key comparison not constant-time. | Low      | Accepted     | Use `hmac.compare_digest()` for key comparison. HTTPS out of scope for MVP. See SEC-005. |
| A03  | Injection                               | All SQL queries use parameterized statements. Prompt templates use `str.format()` with DB-sourced values only; no direct user-text injection into prompts. | Info     | Mitigated    | Current approach is sound. Monitor if user-supplied text is ever routed to prompts. |
| A04  | Insecure Design                         | No rate limiting on AI generation endpoints, which are costly operations. Missing global exception handler for unhandled errors. | Medium   | Open         | Add rate limiting middleware (e.g., slowapi). Add catch-all exception handler. See SEC-002, SEC-004. |
| A05  | Security Misconfiguration               | No `.gitignore` file — `.env` files with secrets could be committed. CORS uses wildcard methods/headers with `allow_credentials=True`. | High     | Open         | Create `.gitignore` excluding `.env`, `data/`, `__pycache__/`. Restrict CORS. See SEC-003, SEC-006. |
| A06  | Vulnerable & Outdated Components        | Dependencies use version ranges, not exact pins. No automated vulnerability scanning (pip-audit, Dependabot) configured. | Low      | Open         | Pin exact versions. Add pip-audit to CI. See SEC-008. |
| A07  | Identification & Authentication Failures| Simple API key auth with no expiration, rotation, or per-user identity. Adequate for MVP local use only. | Low      | Accepted     | Sufficient for MVP per DD-005. Plan OAuth2/JWT for production. |
| A08  | Software & Data Integrity Failures      | No CI/CD workflows present; no dependency integrity verification (no lock file or hash checking). | Low      | Open         | Add `pip freeze` lock file and CI workflow. See SEC-009. |
| A09  | Security Logging & Monitoring Failures  | Request logging present. No dedicated security event logging (auth failures, anomalous patterns). No alerting. | Low      | Open         | Add structured security event logging. See SEC-010. |
| A10  | Server-Side Request Forgery (SSRF)      | Outbound calls only go to the configured `GITHUB_MODELS_ENDPOINT`. No user-controlled URL construction. | Info     | Mitigated    | No action needed. Endpoint is set via environment variable at startup. |

---

## 4. API Security Review

### 4.1 Authentication

| Check                                           | Status | Notes                                                        |
|--------------------------------------------------|--------|--------------------------------------------------------------|
| All protected endpoints require valid auth token | ✅ Pass | `APIKeyMiddleware` enforces `X-API-Key` on all non-exempt paths |
| Tokens have appropriate expiration               | ⚠️ N/A | Static API key; no expiration mechanism (acceptable for MVP) |
| Token validation rejects tampered/expired tokens | ✅ Pass | Invalid keys return 401 with structured error response       |
| No sensitive data in JWT payload (if applicable) | ⚠️ N/A | No JWT used; simple API key header only                      |

### 4.2 Authorisation

| Check                                            | Status  | Notes                                                       |
|--------------------------------------------------|---------|-------------------------------------------------------------|
| Endpoint-level access control enforced           | ✅ Pass  | Middleware applies to all routes; health/docs exempt (correct) |
| Users cannot access other users' progress data   | ❌ Fail  | `user_id` is a path parameter with no ownership validation (SEC-001) |
| Admin-only routes are properly guarded           | ⚠️ N/A  | No admin routes in MVP                                      |

### 4.3 Input Validation

| Check                                            | Status  | Notes                                                       |
|--------------------------------------------------|---------|-------------------------------------------------------------|
| All inputs validated via Pydantic models         | ✅ Pass  | All request/response bodies use Pydantic v2 models          |
| Topic parameter restricted to allowed enum values| ✅ Pass  | DB CHECK constraint limits topics to 3 allowed values       |
| Prompt input sanitised before sending to GitHub Models API | ✅ Pass | Prompt parameters (topic, level, objectives) sourced from DB seed data only; no direct user text reaches prompts |
| Request body size limits configured              | ❌ Fail  | No explicit body size limit configured in FastAPI/Uvicorn (SEC-007) |
| Path/query parameters validated and typed        | ✅ Pass  | FastAPI enforces `int` for course_id/lesson_id/quiz_id; `Query` constraints on limit/offset |

### 4.4 Rate Limiting

| Check                                            | Status  | Notes                                                       |
|--------------------------------------------------|---------|-------------------------------------------------------------|
| Rate limiting applied to content generation endpoint | ❌ Fail | No rate limiting middleware configured (SEC-002)            |
| Rate limiting applied to authentication endpoints| ❌ Fail  | No brute-force protection on API key attempts               |
| Appropriate HTTP 429 response returned           | ❌ Fail  | No 429 responses generated by the application itself        |

---

## 5. Secret Management Review

| Check                                                  | Status  | Notes                                                 |
|--------------------------------------------------------|---------|-------------------------------------------------------|
| No API keys or secrets hardcoded in source code        | ✅ Pass  | All secrets use `pydantic-settings` with env vars     |
| `GITHUB_MODELS_API_KEY` loaded from environment only   | ✅ Pass  | Loaded via `Settings` class from env / `.env` file    |
| `.env` files excluded in `.gitignore`                  | ❌ Fail  | No `.gitignore` file exists in the repository (SEC-003) |
| Secrets in CI/CD stored as GitHub Actions secrets       | ⚠️ N/A | No CI/CD workflows present                           |
| No secrets logged or included in error responses       | ✅ Pass  | API keys not present in log statements or error bodies. `Authorization` header value not logged. |
| Secret rotation procedure documented                   | ❌ Fail  | No rotation procedure documented (SEC-011)            |

---

## 6. Dependency Security

| Check                                              | Status  | Notes                                                    |
|----------------------------------------------------|---------|----------------------------------------------------------|
| `pip audit` or equivalent run against requirements | ⚠️ Manual | No automated scanning; manual review performed           |
| No known critical/high CVEs in dependencies        | ✅ Pass  | Current version ranges target recent, well-maintained packages |
| Dependency versions pinned in requirements file    | ⚠️ Partial | Version ranges used (e.g., `>=0.110,<1.0`), not exact pins (SEC-008) |
| Dependabot or similar automated scanning enabled   | ❌ Fail  | No Dependabot config or GitHub Advanced Security alerts  |
| GitHub Advanced Security alerts reviewed           | ⚠️ N/A  | Not configured for this repository                       |

### Known Dependency Issues

| Package      | CVE / Advisory | Severity | Status   | Notes                                              |
|--------------|----------------|----------|----------|----------------------------------------------------|
| —            | —              | —        | —        | No known CVEs in current version ranges as of review date. All 6 dependencies (fastapi, uvicorn, httpx, pydantic, pydantic-settings, aiosqlite) are actively maintained with recent releases. |

---

## 7. Findings Summary

| Finding ID | Description                                                                | Severity | Component              | BRD/NFR Ref          | Remediation                                                                                     | Status |
|------------|----------------------------------------------------------------------------|----------|------------------------|----------------------|-------------------------------------------------------------------------------------------------|--------|
| SEC-001    | IDOR on progress endpoints — any API key holder can read/write any user's progress via `user_id` path parameter | Medium   | COMP-001 (API Gateway), COMP-004 (Progress) | BRD-NFR-004          | Implement user-scoped authentication tokens or validate that the API key maps to the requested `user_id`. For MVP, document the limitation. | Open   |
| SEC-002    | No rate limiting on AI generation endpoints (`POST /lessons/{id}/content`, `POST /lessons/{id}/quiz`) | Medium   | COMP-001 (API Gateway), COMP-002 (Content Service) | BRD-NFR-005          | Add `slowapi` or custom rate-limiting middleware. Apply stricter limits to AI endpoints (e.g., 10 req/min) than catalog endpoints. | Open   |
| SEC-003    | No `.gitignore` file — `.env` files, `data/` directory, and `__pycache__` could be committed to version control, risking secret exposure | High     | Configuration          | BRD-NFR-003          | Create `.gitignore` with entries for `.env`, `data/*.db`, `__pycache__/`, `*.pyc`, `.venv/`, `*.sqlite3`. | Open   |
| SEC-004    | No global catch-all exception handler for unhandled errors — FastAPI's default 500 response may leak stack traces, file paths, and dependency versions | Medium   | COMP-001 (API Gateway) | BRD-NFR-005, BRD-NFR-007 | Register a generic `Exception` handler in `register_exception_handlers()` that returns a safe 500 JSON response without internal details. | Open   |
| SEC-005    | API key comparison uses `!=` operator — susceptible to timing side-channel attacks | Low      | COMP-001 (API Gateway) | BRD-NFR-004          | Replace `key != self._api_key` with `hmac.compare_digest(key, self._api_key)` in `middleware/auth.py`. | Open   |
| SEC-006    | CORS configured with `allow_methods=["*"]`, `allow_headers=["*"]`, and `allow_credentials=True` — overly permissive for any deployment beyond localhost | Medium   | COMP-001 (API Gateway) | BRD-NFR-004          | Restrict `allow_methods` to `["GET", "POST", "OPTIONS"]` and `allow_headers` to `["X-API-Key", "Content-Type"]`. Review `allow_credentials` necessity. | Open   |
| SEC-007    | No request body size limit configured — large payloads could cause memory exhaustion (DoS) | Low      | COMP-001 (API Gateway) | BRD-NFR-001          | Configure `--limit-max-request-size` on Uvicorn or add middleware to reject bodies > 1 MB.      | Open   |
| SEC-008    | Dependencies use version ranges instead of pinned versions — builds are not reproducible and may pull in vulnerable patch releases | Low      | Dependencies           | BRD-NFR-010          | Generate a `requirements.lock` or pin exact versions. Add `pip-audit` check in CI pipeline.     | Open   |
| SEC-009    | No CI/CD pipeline configured — no automated testing, linting, or security scanning before code merges | Low      | CI/CD                  | BRD-NFR-011          | Add a GitHub Actions workflow with `pytest`, `ruff`/`flake8`, and `pip-audit` steps.            | Open   |
| SEC-010    | No dedicated security event logging — authentication failures logged at WARNING but no structured security audit trail | Low      | COMP-001 (API Gateway) | BRD-NFR-007          | Add structured security logging with event types (AUTH_FAILURE, RATE_LIMIT_HIT, INVALID_INPUT) to a dedicated logger or log stream. | Open   |
| SEC-011    | No secret rotation procedure documented for `GITHUB_MODELS_API_KEY` or `API_KEY` | Info     | Configuration          | BRD-NFR-003          | Document rotation steps in a `SECURITY.md` or operations runbook.                               | Open   |
| SEC-012    | `.env.example` contains placeholder secret values — ensure copy instructions emphasize never committing the populated `.env` file | Info     | Configuration          | BRD-NFR-003          | Add a comment to `.env.example` header: "⚠️ NEVER commit the .env file". Ensure `.gitignore` excludes it. | Open   |

### Severity Definitions

| Severity     | Definition                                                              |
|--------------|-------------------------------------------------------------------------|
| **Critical** | Exploitable vulnerability with immediate risk of data breach or system compromise |
| **High**     | Significant vulnerability; exploitation likely without remediation      |
| **Medium**   | Vulnerability with limited impact or requiring specific conditions      |
| **Low**      | Minor issue or hardening recommendation                                 |
| **Info**     | Observation or best-practice suggestion                                 |

---

## 8. Recommendations

### Immediate (before MVP launch)

1. **SEC-003** — Create a `.gitignore` file excluding `.env`, `data/*.db`, `__pycache__/`, `.venv/`, and other build artifacts. This is the highest-priority fix to prevent accidental secret commits.
2. **SEC-004** — Add a catch-all `Exception` handler in `register_exception_handlers()` to prevent stack trace leakage in error responses.
3. **SEC-006** — Tighten CORS configuration to allow only required HTTP methods (`GET`, `POST`, `OPTIONS`) and headers (`X-API-Key`, `Content-Type`).

### Short-Term (post-MVP)

1. **SEC-001** — Implement user-scoped authentication (JWT or session tokens) to enforce ownership on progress endpoints.
2. **SEC-002** — Add rate limiting via `slowapi` or a custom middleware. Apply aggressive limits to AI generation endpoints to prevent cost abuse.
3. **SEC-005** — Switch to constant-time comparison for API key validation using `hmac.compare_digest()`.
4. **SEC-009** — Set up a GitHub Actions CI/CD workflow with automated tests, linting, and `pip-audit` dependency scanning.
5. **SEC-010** — Implement structured security event logging for authentication failures and anomalous request patterns.

### Long-Term

1. Adopt OAuth2/JWT authentication with proper user identity, token expiration, and refresh flows.
2. Implement a secrets management solution (e.g., Azure Key Vault, HashiCorp Vault) with automated rotation.
3. Deploy a Web Application Firewall (WAF) in front of the API when moving to cloud hosting.
4. Enable Dependabot alerts and automated dependency update PRs.
5. Conduct a focused penetration test on the API endpoints before production deployment.

---

## 9. Traceability

### 9.1 Mapping to HLD / LLD Components

| HLD/LLD Component                 | Findings                                | Review Section           |
|-----------------------------------|-----------------------------------------|--------------------------|
| COMP-001 — API Gateway (FastAPI)  | SEC-001, SEC-002, SEC-004, SEC-005, SEC-006, SEC-007 | §4 API Security          |
| COMP-002 — Content Service (AI)   | SEC-002                                 | §3 OWASP A04, §4.4 Rate Limiting |
| COMP-003 — Course Catalog Service | (No findings)                           | §4.3 Input Validation    |
| COMP-004 — Progress Tracking      | SEC-001                                 | §4.2 Authorisation       |
| Configuration & Secrets           | SEC-003, SEC-011, SEC-012               | §5 Secret Management     |
| Dependencies                      | SEC-008                                 | §6 Dependency Security   |
| CI/CD Pipeline                    | SEC-009                                 | §3 OWASP A08             |

### 9.2 Mapping to BRD Non-Functional Requirements

| BRD NFR                                               | Findings         | Status                                |
|-------------------------------------------------------|------------------|---------------------------------------|
| BRD-NFR-001 — Non-AI endpoints < 2s response          | SEC-007          | Met (no perf issues observed); body size limit recommended |
| BRD-NFR-002 — AI endpoints < 10s response             | (None)           | Addressed — 30s timeout configured    |
| BRD-NFR-003 — API key never logged/exposed            | SEC-003, SEC-011, SEC-012 | Partially met — key not logged, but no `.gitignore` protection |
| BRD-NFR-004 — All endpoints enforce auth              | SEC-001, SEC-005, SEC-006 | Met for API key check; IDOR and timing gaps noted |
| BRD-NFR-005 — Graceful AI failure handling            | SEC-002, SEC-004 | Partially met — AI errors handled; rate limiting and catch-all missing |
| BRD-NFR-006 — WAL mode and transactions               | (None)           | Fully met — WAL enabled, transactions via commit() |
| BRD-NFR-007 — Request logging                         | SEC-010          | Met for basic logging; security events not structured |
| BRD-NFR-008 — AI call debug logging                   | (None)           | Fully met — model, token count, latency logged at DEBUG |
| BRD-NFR-009 — Pydantic validation on all inputs       | (None)           | Fully met — all endpoints use Pydantic models |
| BRD-NFR-010 — Modular codebase structure              | SEC-008          | Fully met — clean separation of concerns |
| BRD-NFR-011 — Automated tests per requirement         | SEC-009          | Not yet met — no CI pipeline or test suite observed |
| BRD-NFR-012 — Atomic persistence for scores/progress  | (None)           | Met — `INSERT OR IGNORE` for idempotent writes, commit() after writes |

---

*Security review completed by `security-agent` on 2026-03-24. All source code under `src/`, design documents (HLD v1.0, LLD api-layer/content-service/data-layer), BRD v1.0 requirements, `requirements.txt`, and `.env.example` were reviewed. 12 findings identified (0 Critical, 1 High, 4 Medium, 5 Low, 2 Info).*

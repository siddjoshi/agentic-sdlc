# Task: Implement Seed Data for All 6 Courses

| Field        | Value                |
|--------------|----------------------|
| **Task ID**  | TASK-009             |
| **Story**    | STORY-006            |
| **Status**   | To Do                |
| **Assignee** | develop-agent        |
| **Estimate** | 3h                   |

## Description

Create the `seed_database()` function that inserts initial course and lesson records for all 3 training topics (GitHub Actions, GitHub Copilot, GitHub Advanced Security) at 2 skill levels each (beginner, intermediate), totaling 6 courses and 30+ lessons.

## Implementation Details

**Files to create/modify:**
- `src/database/seed.py` — SEED_COURSES, SEED_LESSONS data and seed_database() function

**Approach:**
```python
import aiosqlite

SEED_COURSES = [
    {"title": "GitHub Actions — Beginner", "description": "Learn the fundamentals of CI/CD with GitHub Actions.", "topic": "github-actions", "level": "beginner"},
    {"title": "GitHub Actions — Intermediate", "description": "Advanced workflows, matrix builds, and custom actions.", "topic": "github-actions", "level": "intermediate"},
    {"title": "GitHub Copilot — Beginner", "description": "Get started with AI-assisted coding using GitHub Copilot.", "topic": "github-copilot", "level": "beginner"},
    {"title": "GitHub Copilot — Intermediate", "description": "Advanced Copilot techniques, prompt engineering, and chat.", "topic": "github-copilot", "level": "intermediate"},
    {"title": "GitHub Advanced Security — Beginner", "description": "Introduction to code scanning, secret scanning, and Dependabot.", "topic": "github-advanced-security", "level": "beginner"},
    {"title": "GitHub Advanced Security — Intermediate", "description": "Custom CodeQL queries, push protection, and security policies.", "topic": "github-advanced-security", "level": "intermediate"},
]
```

Each course should have 5-6 lessons with:
- Meaningful titles related to the topic
- Correct ordering (1, 2, 3, ...)
- JSON array of 2-3 learning objectives per lesson

Use `INSERT OR IGNORE` for idempotency. The function takes an `aiosqlite.Connection` and is called from `DatabaseManager.initialize()`.

**Lessons per course (minimum 5 each):**
- GitHub Actions Beginner: Intro, Workflow Syntax, Actions Marketplace, Env Vars & Secrets, Building & Testing
- GitHub Actions Intermediate: Matrix Builds, Custom Actions, Reusable Workflows, Artifacts & Caching, Security Best Practices
- GitHub Copilot Beginner: Intro, Code Completions, Chat, Prompt Patterns, IDE Integration
- GitHub Copilot Intermediate: Advanced Prompting, Test Generation, Refactoring with Copilot, Custom Instructions, Workspace Agent
- GitHub Advanced Security Beginner: Intro, Secret Scanning, Dependabot, Code Scanning Basics, Security Advisories
- GitHub Advanced Security Intermediate: Custom CodeQL Queries, Push Protection, Security Policies, SARIF & Integrations, Supply Chain Security

## API Changes

N/A

## Data Model Changes

N/A — uses existing tables created by TASK-008.

## Acceptance Criteria

- [ ] 6 courses are seeded (2 per topic × 3 topics)
- [ ] At least 30 lessons total across all courses
- [ ] Each lesson has a title, correct order, and objectives JSON array
- [ ] INSERT OR IGNORE prevents duplicates on re-seed
- [ ] Seed runs automatically during DatabaseManager.initialize()

## Test Requirements

- **Unit tests:** Test seed_database() populates correct record counts; test idempotency by running twice
- **Integration tests:** After app startup, verify course and lesson counts via DB queries
- **Edge cases:** Re-seeding an existing database doesn't create duplicates

## Parent References

| Ref Type | ID               |
|----------|------------------|
| Story    | STORY-006        |
| Epic     | EPIC-001         |
| BRD      | BRD-FR-010       |

## Definition of Done

- [ ] Code written and follows project conventions
- [ ] All tests passing (`pytest`)
- [ ] No linting errors
- [ ] PR opened and reviewed
- [ ] Acceptance criteria verified

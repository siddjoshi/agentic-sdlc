# Agent Operating Handbook — Agentic SDLC

## Mission

Build an AI-powered learning platform MVP through a chain of 6 specialized Copilot agents. Each agent owns a phase of the SDLC and produces artifacts consumed by subsequent agents.

## Guardrails

- Use templates from `templates/` directory for all SDLC documents
- Maintain requirement ID traceability (BRD-xxx) across all artifacts
- Update `docs/change-log.md` for key decisions and scope changes
- Follow Python + FastAPI conventions defined in `.github/copilot-instructions.md`
- Keep artifacts focused — one document per template purpose

## Agent Pipeline & Execution Order

| Order | Agent | Phase | Depends On |
|-------|-------|-------|------------|
| 1 | `@requirement-agent` | Requirements | User input (product vision) |
| 2 | `@plan-and-design-agent` | Architecture & Design | Completed BRD |
| 3 | `@epic-and-tasks-agent` | Backlog Decomposition | BRD + HLD + LLD |
| 4 | `@develop-agent` | Implementation | Tasks + Design docs |
| 5 | `@automation-test-agent` | Testing | Source code + Tasks |
| 6 | `@security-agent` | Security Review | Source code + Design docs |

## Traceability Rules

- Every requirement in BRD gets an ID: `BRD-001`, `BRD-002`, etc.
- HLD/LLD components reference BRD IDs they satisfy
- EPICs/Stories/Tasks reference parent BRD + design component IDs
- Test cases reference the Task/Story they validate
- Security findings reference the component and requirement affected

## Operating Playbook

1. **Read context** — Before generating, read all upstream artifacts to understand scope
2. **Use templates** — Clone the relevant template from `templates/` and populate all sections
3. **Trace back** — Every output must reference at least one upstream requirement ID
4. **Log decisions** — Record key decisions, assumptions, and open questions in `docs/change-log.md`
5. **Stay MVP** — Focus on the 3 use cases (GitHub Actions, Copilot, Advanced Security training)

## MVP Scope Boundaries

### In Scope
- AI-generated training content (lessons, quizzes) for 3 GitHub topics
- REST API for content delivery (FastAPI)
- GitHub Models integration for content generation
- Basic progress tracking
- Simple web frontend

### Out of Scope (for MVP)
- User authentication/authorization (use simple API keys)
- Multi-tenant support
- Content versioning/approval workflows
- Analytics dashboards
- Mobile app

# Agentic SDLC — AI-Powered Learning Platform

An AI-powered learning platform designed to help organizations create, deliver, and track training content. Built entirely through an agentic SDLC pipeline using GitHub Copilot custom agents.

## MVP Use Cases

| # | Use Case | Description |
|---|----------|-------------|
| 1 | **GitHub Actions Training** | AI-generated lessons, quizzes, and hands-on exercises for CI/CD workflows |
| 2 | **GitHub Copilot Training** | AI-generated content for prompt engineering, code suggestions, and Copilot features |
| 3 | **GitHub Advanced Security Training** | AI-generated content for code scanning, secret scanning, and Dependabot |

## Tech Stack

- **Backend**: Python + FastAPI
- **AI Platform**: GitHub Models (direct API)
- **Frontend**: Simple HTML/JS (MVP)
- **Testing**: pytest

## Agent Pipeline

The SDLC is driven by 6 chained Copilot agents. Each agent's output feeds the next:

```
requirement-agent → plan-and-design-agent → epic-and-tasks-agent → develop-agent → automation-test-agent → security-agent
```

| Agent | SDLC Phase | Input | Output |
|-------|-----------|-------|--------|
| `@requirement-agent` | Requirements | User vision | `docs/requirements/BRD.md` |
| `@plan-and-design-agent` | Design | BRD | `docs/design/HLD.md`, `docs/design/LLD/*.md` |
| `@epic-and-tasks-agent` | Planning | BRD + HLD + LLD | `backlog/epics/`, `backlog/stories/`, `backlog/tasks/` |
| `@develop-agent` | Development | Tasks + LLD | `src/` (Python + FastAPI) |
| `@automation-test-agent` | Testing | src/ + Tasks | `tests/` (pytest) |
| `@security-agent` | Security | src/ + Design docs | `docs/testing/security-review.md` |

## Repository Structure

```
├── .github/
│   ├── copilot-instructions.md     # Project-level Copilot guidance
│   └── agents/                      # 6 custom Copilot agents
├── templates/                       # SDLC document templates
├── docs/                            # Generated SDLC artifacts
│   ├── requirements/
│   ├── design/
│   └── testing/
├── backlog/                         # EPICs, Stories, Tasks
├── src/                             # Application source code
├── tests/                           # Test suites
└── AGENTS.md                        # Agent operating handbook
```

## Getting Started

### Using the Agent Pipeline

1. **Generate Requirements**: `@requirement-agent` — describe your product vision and training use cases
2. **Create Design**: `@plan-and-design-agent` — point to `docs/requirements/BRD.md`
3. **Build Backlog**: `@epic-and-tasks-agent` — point to BRD + design docs
4. **Implement Code**: `@develop-agent` — point to specific tasks from backlog
5. **Write Tests**: `@automation-test-agent` — point to implemented code + tasks
6. **Security Review**: `@security-agent` — point to codebase + design

### Running the Application (after develop-agent)

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

### Running Tests (after automation-test-agent)

```bash
pytest tests/ -v
```

## References

- Agent patterns inspired by [AI-SDLC](https://github.com/siddjoshi/AI-SDLC)

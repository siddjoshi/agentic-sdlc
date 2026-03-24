# The Agentic SDLC: An Opinionated Guide

**Author**: Research compiled from industry sources and hands-on implementation  
**Date**: 2026-03-24  
**Status**: Living Document

---

## TL;DR

The Software Development Life Cycle is being rebuilt around AI agents. Not "AI-assisted"—**AI-native**. Specialized agents now own entire SDLC phases, chaining their outputs together like a compiler pipeline for software projects. This is not a minor productivity boost; it is a structural change in how software gets made.

This document takes a strong position on what the Agentic SDLC is, why it matters, what works, what doesn't, and where the industry is heading.

---

## 1. What Is the Agentic SDLC?

The traditional SDLC—Planning, Design, Implementation, Testing, Deployment, Maintenance—assumes humans perform every phase. AI tooling has historically been bolted on as "copilots" that autocomplete code or suggest fixes, but the human remains the orchestrator.

**The Agentic SDLC inverts this model.** AI agents become first-class participants that own entire phases of the lifecycle. Humans shift from doers to reviewers, approvers, and course-correctors.

An Agentic SDLC pipeline looks like this:

```
User Vision
    ↓
┌─────────────────────┐
│  Requirement Agent   │  → BRD (Business Requirements Document)
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│  Design Agent        │  → HLD (High-Level Design) + LLD (Low-Level Design)
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│  Backlog Agent       │  → EPICs → Stories → Tasks
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│  Development Agent   │  → Source Code
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│  Testing Agent       │  → Test Suites + Test Plans
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│  Security Agent      │  → Security Review + Findings
└─────────────────────┘
```

Each agent reads upstream artifacts, uses templates, and produces traceable outputs. The chain is deterministic in structure, even if the content generation is probabilistic.

---

## 2. Strong Opinions, Loosely Held

### Opinion 1: Agents MUST Be Specialized, Not General-Purpose

**A single "do-everything" agent is an anti-pattern.** The moment you ask one agent to write requirements AND design AND code AND test, you get:

- Context window pollution (the agent forgets earlier decisions)
- Role confusion (it optimizes for one phase at the expense of others)
- Unauditability (you can't tell which "hat" it was wearing when it made a choice)

**The correct pattern is a pipeline of narrow specialists.** A requirement agent should know nothing about pytest. A testing agent should know nothing about stakeholder analysis. Specialization enables:

- **Focused context windows**: Each agent loads only the upstream artifacts and templates it needs.
- **Independent evaluation**: You can swap, upgrade, or retrain one agent without touching the others.
- **Clear accountability**: When a test fails, you trace it back through the chain—was the requirement wrong, the design incomplete, or the implementation buggy?

### Opinion 2: Traceability Is Non-Negotiable

Every artifact in an Agentic SDLC must trace back to a requirement ID. This isn't bureaucratic overhead—it's the **only way to maintain coherence** when AI is generating at machine speed.

Without traceability:
- A design document references a feature nobody asked for.
- A test validates behavior that was descoped three iterations ago.
- A security review flags a component that doesn't exist in the final architecture.

The rule is simple: **`BRD-xxx` IDs flow through every artifact.** HLD components reference BRD IDs. EPICs reference HLD components. Stories reference EPICs. Tasks reference Stories. Tests reference Tasks. Security findings reference components and requirements. No ID, no artifact.

### Opinion 3: Templates Are the Contract Between Agents

Agents need structure. Freeform "generate a design document" prompts produce inconsistent, incomparable outputs. Templates solve this:

- They define **what sections are required** (not optional—required).
- They establish **naming conventions** for IDs, statuses, and cross-references.
- They ensure **downstream agents can parse upstream outputs** reliably.

A template is not a suggestion. It is the API contract between agents. Treat it like a schema definition.

### Opinion 4: Human-in-the-Loop Is a Feature, Not a Limitation

The most dangerous version of the Agentic SDLC is the fully autonomous one. Agents should **never** merge their own PRs, deploy their own code, or close their own issues without human review.

The correct model is **Continuous AI** (a term coined by GitHub Next): agents work continuously in the background—triaging, documenting, testing, reviewing—but humans approve every forward-moving decision. This is analogous to CI/CD, where machines build and test but humans gate releases.

> "Pull requests are never merged automatically, and humans must always review and approve." — GitHub Agentic Workflows documentation

### Opinion 5: Repository-Native Memory Beats External State

Where should agents store their decisions, context, and history? Not in a vector database. Not in a separate service. **In the repository itself.**

This is the "drop-box" pattern pioneered by multi-agent frameworks like Squad:

- Architectural decisions go in `decisions.md` or `docs/change-log.md`.
- Agent configuration lives in `.github/` or project root files like `AGENTS.md`.
- Prompt templates live in a `templates/` directory, versioned alongside code.

Benefits:
- **Persistence**: Agent memory survives session boundaries and tool restarts.
- **Auditability**: Every decision is in the git history.
- **Portability**: Clone the repo and you clone the agent's knowledge.
- **No infrastructure**: No vector DB, no external state service, no synchronization headaches.

### Opinion 6: Start with Read-Only Agents, Graduate to Write Agents

The safest adoption path:

1. **Phase 1 — Reporting agents**: Generate status reports, summarize issues, flag stale PRs. Read-only. Zero risk.
2. **Phase 2 — Suggestion agents**: Propose code changes, draft documentation updates, recommend test cases. Agents create PRs but never merge them.
3. **Phase 3 — Execution agents**: Implement features, write tests, perform refactors. Still human-gated at the PR level.
4. **Phase 4 — Autonomous maintenance agents**: Auto-fix CI failures, update dependencies, clean up dead code. Narrowly scoped, well-tested, monitored.

Jumping straight to Phase 4 is how you get a bot that "helpfully" deletes your production database migration.

---

## 3. The Six-Agent Pipeline (In Practice)

Based on real-world implementation, here is what a functioning Agentic SDLC pipeline looks like:

### Agent 1: Requirement Agent
**Input**: User's product vision (plain language)  
**Output**: Business Requirements Document (BRD)  
**Key behaviors**:
- Interviews/extracts from the user's description
- Produces numbered requirements (`BRD-001`, `BRD-002`, ...)
- Defines functional requirements, non-functional requirements, and AI-specific requirements
- Establishes success metrics and KPIs
- Identifies stakeholders and scope boundaries

### Agent 2: Design Agent
**Input**: Completed BRD  
**Output**: High-Level Design (HLD) + Low-Level Design (LLD)  
**Key behaviors**:
- Maps every BRD requirement to a system component
- Produces architecture diagrams (Mermaid, PlantUML)
- Documents key design decisions with rationale
- Defines API contracts, data models, and component interfaces
- Identifies constraints and technology choices

### Agent 3: Backlog Agent
**Input**: BRD + HLD + LLD  
**Output**: EPICs, User Stories, and Tasks  
**Key behaviors**:
- Decomposes design into implementable work items
- Maintains full traceability (Task → Story → EPIC → BRD)
- Includes acceptance criteria for every story
- Specifies implementation details (file paths, code patterns, dependencies)
- Orders tasks by dependency for the development agent

### Agent 4: Development Agent
**Input**: Tasks + Design documents  
**Output**: Source code  
**Key behaviors**:
- Implements one task at a time, following the specified design
- Uses project conventions (type hints, Pydantic models, async patterns)
- Follows the Low-Level Design for file structure and API contracts
- Produces working, runnable code—not scaffolds or stubs

### Agent 5: Testing Agent
**Input**: Source code + Tasks + BRD  
**Output**: Test suites + Test Plan  
**Key behaviors**:
- Generates tests from acceptance criteria, not from reading the implementation
- Covers unit, integration, and contract testing layers
- Mocks external dependencies (AI APIs, databases)
- Maps every test case to a BRD requirement and Task ID
- Targets meaningful coverage, not vanity metrics

### Agent 6: Security Agent
**Input**: Source code + Design documents  
**Output**: Security Review with findings  
**Key behaviors**:
- Reviews against OWASP Top 10
- Examines authentication, authorization, input validation, secrets management
- Rates findings by severity (Critical, High, Medium, Low, Info)
- Provides specific remediation guidance with code examples
- References affected components and BRD requirements

---

## 4. Architectural Patterns That Work

### Pattern: Context Replication, Not Context Splitting

When running multiple agents, don't try to share one context window. Give each agent its own full context loaded with the specific upstream artifacts it needs. A testing agent loading the BRD + source code in its own 200K-token window will outperform a shared agent trying to juggle requirements, design, implementation, and tests in one session.

### Pattern: Structured Outputs Over Freeform Generation

Agents should produce Pydantic-validated JSON, Markdown with required sections, or structured files with known schemas. Freeform text generation between agents creates parsing nightmares. If Agent 2 needs to read Agent 1's output, that output better be predictable.

### Pattern: Decisions as Data

Every key decision should be logged in a structured format:

```markdown
| Date | Phase | Change | Impact | Owner |
|------|-------|--------|--------|-------|
| 2026-03-24 | Requirements | BRD v1.0 created | Baseline established | requirement-agent |
| 2026-03-24 | Design | HLD v1.0 — 5 components defined | Design baseline | design-agent |
```

This isn't documentation theater. This is the audit trail that lets you debug the pipeline when something goes wrong three agents downstream.

### Pattern: Fail-Fast With Graceful Degradation

If the AI API is down, agents should not hallucinate alternatives. They should fail explicitly and tell the human what's blocked. The worst-case scenario in an Agentic SDLC is a confident-sounding agent that silently produced garbage because it couldn't reach its inference endpoint.

---

## 5. What Doesn't Work

### Anti-Pattern: The "One Prompt to Rule Them All"

"Generate a full application from this description" inevitably produces:
- Missing edge cases
- Inconsistent architecture
- No test coverage
- Security vulnerabilities baked into every layer

Decomposition is the entire point. Small, focused prompts with clear scope produce better results than ambitious mega-prompts.

### Anti-Pattern: Agents Reviewing Their Own Work

If one agent writes code and the same agent reviews it, you get confirmation bias at machine scale. The testing agent must be a *different* agent with a *separate* context window. Squad's reviewer protocol explicitly prevents the original author from revising rejected work—a different agent must step in.

### Anti-Pattern: Implicit Memory

"The model just knows our conventions" is a prayer, not a strategy. Conventions, decisions, and context must be explicit in repository files. Models change, context windows reset, and sessions expire. What lives in the repo survives; what lives in the chat dies.

### Anti-Pattern: Skipping the Security Agent

"We'll add security later" is how you ship an MVP with hardcoded API keys, SQL injection vulnerabilities, and overly permissive CORS. The security agent is not optional. It runs on every pipeline execution, and its findings block release.

---

## 6. Continuous AI: The Agentic SDLC in Steady State

The pipeline described above covers greenfield development. But what about ongoing maintenance? This is where **Continuous AI** enters—the integration of AI agents into the ongoing SDLC, analogous to CI/CD:

| Traditional CI/CD | Continuous AI Equivalent |
|---|---|
| Run tests on every commit | Run security review on every PR |
| Lint code automatically | Auto-triage and label new issues |
| Deploy on merge to main | Auto-generate documentation when code changes |
| Monitor uptime | Auto-investigate CI failures and propose fixes |
| Report build status | Generate daily repository health reports |

GitHub Agentic Workflows make this concrete: you describe desired outcomes in Markdown, commit them as `.md` files in `.github/workflows/`, and they execute as GitHub Actions using coding agents (Copilot CLI, Claude Code, OpenAI Codex).

Key design principles for Continuous AI:
- **Read-only by default**: Agents get write permissions only through explicit "safe outputs."
- **Sandboxed execution**: Network isolation, tool allowlisting, permission boundaries.
- **Human gates**: Agents propose; humans approve. Always.

---

## 7. Where This Is Going

### Near-term (2026)
- Multi-agent orchestration becomes mainstream. Tools like Squad, GitHub Agentic Workflows, and custom Copilot agents make the pipeline accessible without infrastructure overhead.
- Repository-native memory becomes the standard. Agents read from and write to versioned files in the repo.
- Agentic SDLC templates emerge as a new category—starter kits that include not just code scaffolds but agent definitions, prompt templates, and pipeline configurations.

### Medium-term (2027-2028)
- Agents gain long-term project memory across sessions and tool boundaries. GitHub Copilot's cross-agent memory system (coding agent, CLI, code review) is the early version of this.
- Security and compliance agents become continuous, not periodic. They run on every commit, not once before release.
- Agent-to-agent protocols standardize. Just as REST standardized service communication, a protocol will emerge for agents to pass artifacts, declare capabilities, and negotiate scope.

### Long-term (2029+)
- The human role shifts entirely to product vision, ethical judgment, and architectural oversight. The "how" of software development is increasingly delegated.
- Agentic pipelines become self-improving. Testing agents discover gaps and request new tests from the development agent. Security agents flag patterns and the development agent auto-remediates. The pipeline runs forward *and* backward.
- The distinction between "development" and "maintenance" dissolves. Software is continuously generated, tested, secured, and evolved by always-on agent pipelines.

---

## 8. Getting Started: A Pragmatic Playbook

If you're building an Agentic SDLC today, here's the order of operations:

1. **Define your agent pipeline.** Which SDLC phases need agents? Start with 3 (requirements, development, testing) and add more as you gain confidence.

2. **Create templates for every artifact.** BRD template, HLD template, Task template, Test Plan template. These are your agent contracts.

3. **Establish the traceability scheme.** Decide on your ID format (`BRD-xxx`, `TASK-xxx`, etc.) and enforce it in every template.

4. **Write an `AGENTS.md` file.** Document the pipeline order, each agent's inputs/outputs, and the dependencies between them. This is the operating manual for your AI team.

5. **Start with the requirement agent.** Get it to produce consistent, well-structured BRDs from user input. If this agent's output is garbage, everything downstream will be worse.

6. **Add agents incrementally.** Design agent next, then backlog, then development, then testing, then security. Validate each link in the chain before extending it.

7. **Keep humans in the loop.** Review every artifact. Approve every PR. Override every bad decision. The agents work for you, not the other way around.

8. **Log everything.** Maintain a `change-log.md` that records every major decision, every scope change, and every agent output. This is your project's institutional memory.

---

## 9. Recommended Reading & References

- **GitHub Agentic Workflows** — Technical preview for Markdown-defined, Actions-executed agentic automation  
- **Squad** by Brady Gaster — Open source multi-agent orchestration built on GitHub Copilot  
- **GitHub Copilot Agent Mode** — Multi-step, multi-file engineering workflows in the IDE  
- **Continuous AI** by GitHub Next — The concept of integrating AI into the SDLC as a continuous practice  
- **GitHub Copilot Memory System** — Cross-agent memory across coding agent, CLI, and code review  

---

## 10. Final Take

The Agentic SDLC is not about replacing developers. It's about giving every developer a team of tireless, specialized, always-available collaborators that handle the structured, repeatable parts of software engineering while humans focus on the creative, ambiguous, and high-stakes decisions.

The teams that adopt this model will ship faster, with fewer defects, and with better documentation than teams that treat AI as a fancy autocomplete. The teams that resist it will wonder why their competitors are moving so fast.

The future of software development is not one human and one AI. It is **one human and six agents**, each doing what they do best.

---

*This is an opinionated, living document. Opinions will evolve as the tooling matures and the industry learns what works at scale.*

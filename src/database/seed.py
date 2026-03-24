"""Seed data for courses and lessons across all three training topics."""

from __future__ import annotations

import logging

import aiosqlite

logger = logging.getLogger(__name__)

SEED_COURSES = [
    # GitHub Actions
    {
        "title": "GitHub Actions — Beginner",
        "description": "Learn the fundamentals of CI/CD with GitHub Actions.",
        "topic": "github-actions",
        "level": "beginner",
    },
    {
        "title": "GitHub Actions — Intermediate",
        "description": "Advanced workflows, matrix builds, and custom actions.",
        "topic": "github-actions",
        "level": "intermediate",
    },
    # GitHub Copilot
    {
        "title": "GitHub Copilot — Beginner",
        "description": "Get started with AI-assisted coding using GitHub Copilot.",
        "topic": "github-copilot",
        "level": "beginner",
    },
    {
        "title": "GitHub Copilot — Intermediate",
        "description": "Advanced Copilot techniques, prompt engineering, and chat.",
        "topic": "github-copilot",
        "level": "intermediate",
    },
    # GitHub Advanced Security
    {
        "title": "GitHub Advanced Security — Beginner",
        "description": "Introduction to code scanning, secret scanning, and Dependabot.",
        "topic": "github-advanced-security",
        "level": "beginner",
    },
    {
        "title": "GitHub Advanced Security — Intermediate",
        "description": "Custom CodeQL queries, push protection, and security policies.",
        "topic": "github-advanced-security",
        "level": "intermediate",
    },
]

# Lessons grouped by (topic, level) — each list is attached to its course.
_LESSONS: dict[tuple[str, str], list[dict]] = {
    ("github-actions", "beginner"): [
        {"title": "Introduction to GitHub Actions", "order": 1, "objectives": '["Understand what GitHub Actions is", "Identify key use cases for CI/CD automation"]'},
        {"title": "Workflow Syntax and Structure", "order": 2, "objectives": '["Read and write workflow YAML files", "Understand triggers, jobs, and steps"]'},
        {"title": "Working with Actions Marketplace", "order": 3, "objectives": '["Find and use community actions", "Pin actions to specific versions"]'},
        {"title": "Environment Variables and Secrets", "order": 4, "objectives": '["Use environment variables in workflows", "Store and access repository secrets"]'},
        {"title": "Building and Testing Code", "order": 5, "objectives": '["Set up a CI pipeline for a sample project", "Run tests and report results"]'},
    ],
    ("github-actions", "intermediate"): [
        {"title": "Matrix Builds and Strategy", "order": 1, "objectives": '["Configure matrix builds for multiple platforms", "Use fail-fast and max-parallel options"]'},
        {"title": "Reusable Workflows", "order": 2, "objectives": '["Create reusable workflow files", "Call workflows from other repositories"]'},
        {"title": "Creating Custom Actions", "order": 3, "objectives": '["Build a Docker container action", "Build a JavaScript action"]'},
        {"title": "Advanced Caching and Artifacts", "order": 4, "objectives": '["Cache dependencies to speed up builds", "Upload and download artifacts between jobs"]'},
        {"title": "Self-Hosted Runners", "order": 5, "objectives": '["Set up a self-hosted runner", "Configure runner groups and labels"]'},
        {"title": "Security Best Practices for Workflows", "order": 6, "objectives": '["Limit permissions with GITHUB_TOKEN scopes", "Avoid script injection vulnerabilities"]'},
    ],
    ("github-copilot", "beginner"): [
        {"title": "What is GitHub Copilot?", "order": 1, "objectives": '["Understand how GitHub Copilot works", "Learn about the AI models behind Copilot"]'},
        {"title": "Setting Up Copilot in Your IDE", "order": 2, "objectives": '["Install the Copilot extension", "Authenticate and enable Copilot"]'},
        {"title": "Writing Code with Suggestions", "order": 3, "objectives": '["Accept, reject, and cycle through suggestions", "Use inline suggestions effectively"]'},
        {"title": "Using Copilot for Documentation", "order": 4, "objectives": '["Generate docstrings and comments", "Create README content with Copilot"]'},
        {"title": "Copilot for Test Generation", "order": 5, "objectives": '["Generate unit tests from existing code", "Review and refine Copilot test suggestions"]'},
    ],
    ("github-copilot", "intermediate"): [
        {"title": "Prompt Engineering for Copilot", "order": 1, "objectives": '["Write effective prompts to guide suggestions", "Use comments and function signatures as context"]'},
        {"title": "Copilot Chat and Conversations", "order": 2, "objectives": '["Use Copilot Chat for code explanations", "Ask Copilot to refactor or fix code"]'},
        {"title": "Copilot for Complex Patterns", "order": 3, "objectives": '["Generate design patterns with Copilot", "Handle multi-file context"]'},
        {"title": "Copilot in the CLI", "order": 4, "objectives": '["Use Copilot CLI for shell commands", "Generate git commands with natural language"]'},
        {"title": "Best Practices and Limitations", "order": 5, "objectives": '["Understand Copilot limitations", "Review generated code for correctness and security"]'},
    ],
    ("github-advanced-security", "beginner"): [
        {"title": "Introduction to GitHub Advanced Security", "order": 1, "objectives": '["Understand GHAS features overview", "Learn about the security tab in repositories"]'},
        {"title": "Code Scanning with CodeQL", "order": 2, "objectives": '["Enable default CodeQL analysis", "Review and triage code scanning alerts"]'},
        {"title": "Secret Scanning Basics", "order": 3, "objectives": '["Understand how secret scanning works", "Respond to secret scanning alerts"]'},
        {"title": "Dependabot for Dependency Management", "order": 4, "objectives": '["Enable Dependabot alerts and updates", "Review and merge Dependabot pull requests"]'},
        {"title": "Security Policies and SECURITY.md", "order": 5, "objectives": '["Create a SECURITY.md file", "Define a vulnerability disclosure process"]'},
    ],
    ("github-advanced-security", "intermediate"): [
        {"title": "Custom CodeQL Queries", "order": 1, "objectives": '["Write a basic CodeQL query", "Run custom queries in the CodeQL CLI"]'},
        {"title": "CodeQL Query Suites and Packs", "order": 2, "objectives": '["Create reusable query packs", "Publish and share CodeQL packs"]'},
        {"title": "Push Protection for Secrets", "order": 3, "objectives": '["Enable push protection", "Handle push protection bypass requests"]'},
        {"title": "Advanced Dependabot Configuration", "order": 4, "objectives": '["Configure Dependabot.yml for multiple ecosystems", "Group and schedule dependency updates"]'},
        {"title": "Security Overview and Dashboards", "order": 5, "objectives": '["Use the organization security overview", "Track security metrics across repositories"]'},
        {"title": "Integrating GHAS into CI/CD Pipelines", "order": 6, "objectives": '["Run CodeQL analysis in GitHub Actions", "Enforce security gates before merging"]'},
    ],
}


async def seed_database(conn: aiosqlite.Connection) -> None:
    """Insert seed courses and lessons if they do not already exist.

    Uses INSERT OR IGNORE for idempotency — safe to call on every startup.
    """
    courses_inserted = 0
    lessons_inserted = 0

    for course in SEED_COURSES:
        cursor = await conn.execute(
            "INSERT OR IGNORE INTO courses (title, description, topic, level) VALUES (?, ?, ?, ?)",
            (course["title"], course["description"], course["topic"], course["level"]),
        )
        if cursor.rowcount and cursor.rowcount > 0:
            courses_inserted += 1

    await conn.commit()

    # Map (topic, level) → course_id
    course_map: dict[tuple[str, str], int] = {}
    cursor = await conn.execute("SELECT id, topic, level FROM courses")
    rows = await cursor.fetchall()
    for row in rows:
        course_map[(row[0] if isinstance(row, tuple) else row["topic"],
                     row[1] if isinstance(row, tuple) else row["level"])] = (
            row[2] if isinstance(row, tuple) else row["id"]
        )

    # Recalculate mapping correctly for Row objects
    course_map = {}
    cursor = await conn.execute("SELECT id, topic, level FROM courses")
    rows = await cursor.fetchall()
    for row in rows:
        # aiosqlite.Row supports index access
        cid, topic, level = row[0], row[1], row[2]
        course_map[(topic, level)] = cid

    for (topic, level), lesson_list in _LESSONS.items():
        course_id = course_map.get((topic, level))
        if course_id is None:
            continue
        for lesson in lesson_list:
            cursor = await conn.execute(
                'INSERT OR IGNORE INTO lessons (course_id, title, level, "order", objectives) '
                "VALUES (?, ?, ?, ?, ?)",
                (course_id, lesson["title"], level, lesson["order"], lesson["objectives"]),
            )
            if cursor.rowcount and cursor.rowcount > 0:
                lessons_inserted += 1

    await conn.commit()
    logger.info("Seed data: %d courses, %d lessons inserted", courses_inserted, lessons_inserted)

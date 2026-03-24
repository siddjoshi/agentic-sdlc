"""Shared fixtures for the entire test suite.

Provides a fully initialized FastAPI test client with an in-memory SQLite
database seeded with course/lesson data, and mock data factories.
"""

from __future__ import annotations

import json
import os
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

# Set environment variables BEFORE any application imports
os.environ.setdefault("API_KEY", "test-api-key")
os.environ.setdefault("GITHUB_MODELS_API_KEY", "test-gh-key")
os.environ.setdefault("GITHUB_MODELS_ENDPOINT", "https://models.test.ai/inference")
os.environ.setdefault("DATABASE_URL", ":memory:")
os.environ.setdefault("LOG_LEVEL", "WARNING")

# Clear any cached settings so tests pick up overrides
from src.config import get_settings  # noqa: E402

get_settings.cache_clear()

from src.database.connection import DatabaseManager  # noqa: E402
from src.main import create_app  # noqa: E402
from src.services.content_service import ContentService  # noqa: E402

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
API_KEY = "test-api-key"
AUTH_HEADERS = {"X-API-Key": API_KEY}

MOCK_LESSON_CONTENT = "# Mock Lesson\n\nThis is mock lesson content.\n\n```yaml\nname: CI\non: push\n```"

MOCK_QUIZ_JSON = json.dumps([
    {
        "question": "What format are GitHub Actions workflows written in?",
        "options": ["JSON", "YAML", "TOML", "XML"],
        "correct_answer": "YAML",
        "explanation": "GitHub Actions workflows use YAML syntax.",
    },
    {
        "question": "What triggers a workflow?",
        "options": ["on: push", "run: push", "trigger: push", "start: push"],
        "correct_answer": "on: push",
        "explanation": "The 'on' key defines workflow triggers.",
    },
    {
        "question": "Where do workflows live?",
        "options": [
            ".github/workflows/",
            ".actions/",
            "workflows/",
            ".ci/",
        ],
        "correct_answer": ".github/workflows/",
        "explanation": "Workflows are stored in .github/workflows/.",
    },
])


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture()
async def app():
    """Create a FastAPI app with an in-memory database."""
    get_settings.cache_clear()
    application = create_app()

    # Override lifespan manually: init DB and mock AI services
    db_manager = DatabaseManager(":memory:")
    await db_manager.initialize()
    application.state.db_manager = db_manager
    application.state.settings = get_settings()

    # Mock AI components
    mock_ai_client = AsyncMock()
    mock_ai_client.generate = AsyncMock(return_value=MOCK_LESSON_CONTENT)
    mock_ai_client.close = AsyncMock()

    mock_prompt_manager = MagicMock()
    mock_prompt_manager.build_lesson_prompt = MagicMock(return_value=[
        {"role": "system", "content": "You are a test instructor."},
        {"role": "user", "content": "Generate lesson content."},
    ])
    mock_prompt_manager.build_quiz_prompt = MagicMock(return_value=[
        {"role": "system", "content": "You are a test quiz creator."},
        {"role": "user", "content": "Generate quiz."},
    ])

    content_service = ContentService(
        client=mock_ai_client,
        prompt_manager=mock_prompt_manager,
        lesson_max_tokens=2000,
        quiz_max_tokens=1500,
    )
    application.state.content_service = content_service

    yield application

    await db_manager.close()


@pytest_asyncio.fixture()
async def client(app):
    """Async HTTP test client with authentication headers."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", headers=AUTH_HEADERS) as ac:
        yield ac


@pytest_asyncio.fixture()
async def unauth_client(app):
    """Async HTTP test client WITHOUT authentication headers."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture()
async def db_conn(app):
    """Direct database connection for test setup/assertions."""
    return await app.state.db_manager.get_connection()


@pytest_asyncio.fixture()
async def seeded_quiz(db_conn):
    """Insert a quiz directly into the DB and return its metadata."""
    questions = [
        {
            "question": "What format are GitHub Actions workflows written in?",
            "options": ["JSON", "YAML", "TOML", "XML"],
            "correct_answer": "YAML",
            "explanation": "GitHub Actions workflows use YAML syntax.",
        },
        {
            "question": "What triggers a workflow?",
            "options": ["on: push", "run: push", "trigger: push", "start: push"],
            "correct_answer": "on: push",
            "explanation": "The 'on' key defines workflow triggers.",
        },
        {
            "question": "Where do workflows live?",
            "options": [
                ".github/workflows/",
                ".actions/",
                "workflows/",
                ".ci/",
            ],
            "correct_answer": ".github/workflows/",
            "explanation": "Workflows are stored in .github/workflows/.",
        },
    ]
    questions_json = json.dumps(questions)
    cursor = await db_conn.execute(
        "INSERT INTO quizzes (lesson_id, questions_json) VALUES (?, ?)",
        (1, questions_json),
    )
    await db_conn.commit()
    quiz_id = cursor.lastrowid
    return {"quiz_id": quiz_id, "questions": questions, "lesson_id": 1}

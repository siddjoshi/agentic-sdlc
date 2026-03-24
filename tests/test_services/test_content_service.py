"""Tests for ContentService — AI content orchestration.

Covers: BRD-FR-004, BRD-FR-005, BRD-AI-001, BRD-AI-002, BRD-AI-003,
        TASK-014, TASK-017
"""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.ai.client import GitHubModelsClient
from src.ai.prompts import PromptManager
from src.exceptions import AIResponseValidationError
from src.services.content_service import ContentService

pytestmark = pytest.mark.asyncio

MOCK_LESSON_MD = "# Test Lesson\n\nContent here.\n\n```yaml\nname: test\n```"

MOCK_QUIZ_VALID = json.dumps([
    {
        "question": "Q1?",
        "options": ["A", "B", "C", "D"],
        "correct_answer": "A",
        "explanation": "A is correct.",
    },
    {
        "question": "Q2?",
        "options": ["W", "X", "Y", "Z"],
        "correct_answer": "X",
        "explanation": "X is correct.",
    },
    {
        "question": "Q3?",
        "options": ["1", "2", "3", "4"],
        "correct_answer": "3",
        "explanation": "3 is correct.",
    },
])

MOCK_QUIZ_INVALID = "not valid json at all"


def _make_service(ai_return=MOCK_LESSON_MD):
    """Create a ContentService with mocked dependencies."""
    mock_client = AsyncMock(spec=GitHubModelsClient)
    mock_client.generate = AsyncMock(return_value=ai_return)

    mock_prompts = MagicMock(spec=PromptManager)
    mock_prompts.build_lesson_prompt = MagicMock(return_value=[
        {"role": "system", "content": "sys"},
        {"role": "user", "content": "usr"},
    ])
    mock_prompts.build_quiz_prompt = MagicMock(return_value=[
        {"role": "system", "content": "sys"},
        {"role": "user", "content": "usr"},
    ])

    service = ContentService(
        client=mock_client,
        prompt_manager=mock_prompts,
        lesson_max_tokens=2000,
        quiz_max_tokens=1500,
    )
    return service, mock_client, mock_prompts


class TestGenerateLessonContent:
    """ContentService.generate_lesson_content() tests."""

    async def test_returns_expected_dict(self):
        """Verify returned dict matches LessonContentResponse schema. [TASK-014] [BRD-FR-004]"""
        service, mock_client, _ = _make_service(MOCK_LESSON_MD)
        result = await service.generate_lesson_content(
            lesson_id=1,
            topic="GitHub Actions",
            level="beginner",
            objectives=["Learn basics"],
        )
        assert result["lesson_id"] == 1
        assert result["topic"] == "GitHub Actions"
        assert result["level"] == "beginner"
        assert result["content_markdown"] == MOCK_LESSON_MD
        assert "generated_at" in result

    async def test_calls_ai_client_with_correct_tokens(self):
        """Verify AI client called with lesson_max_tokens. [TASK-014] [BRD-AI-001]"""
        service, mock_client, _ = _make_service()
        await service.generate_lesson_content(
            lesson_id=1,
            topic="GitHub Actions",
            level="beginner",
            objectives=["Learn basics"],
        )
        mock_client.generate.assert_awaited_once()
        call_kwargs = mock_client.generate.call_args
        assert call_kwargs.kwargs.get("max_tokens") == 2000

    async def test_builds_prompt_with_correct_args(self):
        """Verify prompt manager called with correct arguments. [TASK-014] [BRD-AI-010]"""
        service, _, mock_prompts = _make_service()
        await service.generate_lesson_content(
            lesson_id=5,
            topic="GitHub Copilot",
            level="intermediate",
            objectives=["Prompt engineering", "Chat features"],
        )
        mock_prompts.build_lesson_prompt.assert_called_once_with(
            "GitHub Copilot", "intermediate", ["Prompt engineering", "Chat features"]
        )

    async def test_propagates_ai_error(self):
        """Verify AI errors propagate to caller. [TASK-014] [BRD-AI-006]"""
        from src.exceptions import AIServiceUnavailableError

        service, mock_client, _ = _make_service()
        mock_client.generate = AsyncMock(
            side_effect=AIServiceUnavailableError(details="timeout")
        )
        with pytest.raises(AIServiceUnavailableError):
            await service.generate_lesson_content(
                lesson_id=1,
                topic="Test",
                level="beginner",
                objectives=[],
            )


class TestGenerateQuiz:
    """ContentService.generate_quiz() tests."""

    async def test_generates_and_persists_quiz(self, db_conn):
        """Verify quiz is generated, validated, and persisted. [TASK-017] [BRD-FR-005]"""
        service, mock_client, _ = _make_service(MOCK_QUIZ_VALID)
        result = await service.generate_quiz(
            lesson_id=1,
            topic="GitHub Actions",
            level="beginner",
            db=db_conn,
        )
        assert "quiz_id" in result
        assert result["lesson_id"] == 1
        assert len(result["questions"]) == 3
        assert "generated_at" in result

    async def test_retries_on_validation_failure(self, db_conn):
        """Verify retry on validation failure (up to 3 attempts). [TASK-017] [BRD-AI-003]"""
        service, mock_client, _ = _make_service()
        # First two calls return invalid JSON, third returns valid
        mock_client.generate = AsyncMock(
            side_effect=[MOCK_QUIZ_INVALID, MOCK_QUIZ_INVALID, MOCK_QUIZ_VALID]
        )
        result = await service.generate_quiz(
            lesson_id=1,
            topic="GitHub Actions",
            level="beginner",
            db=db_conn,
        )
        assert "quiz_id" in result
        assert mock_client.generate.await_count == 3

    async def test_raises_after_all_retries_fail(self, db_conn):
        """Verify AIResponseValidationError after 3 failed attempts. [TASK-017] [BRD-AI-003]"""
        service, mock_client, _ = _make_service()
        mock_client.generate = AsyncMock(return_value=MOCK_QUIZ_INVALID)
        with pytest.raises(AIResponseValidationError):
            await service.generate_quiz(
                lesson_id=1,
                topic="Test",
                level="beginner",
                db=db_conn,
            )
        assert mock_client.generate.await_count == 3

    async def test_quiz_persisted_in_database(self, db_conn):
        """Verify quiz record exists in database after generation. [TASK-017] [BRD-FR-011]"""
        service, _, _ = _make_service(MOCK_QUIZ_VALID)
        result = await service.generate_quiz(
            lesson_id=1,
            topic="Test",
            level="beginner",
            db=db_conn,
        )
        cursor = await db_conn.execute(
            "SELECT id FROM quizzes WHERE id = ?", (result["quiz_id"],)
        )
        row = await cursor.fetchone()
        assert row is not None

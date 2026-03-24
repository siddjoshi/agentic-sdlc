"""Tests for lesson content and quiz generation endpoints.

Covers: BRD-FR-004, BRD-FR-005, BRD-FR-015, BRD-AI-001, BRD-AI-002,
        TASK-015, TASK-018
"""

from __future__ import annotations

import json
from unittest.mock import AsyncMock

import pytest

from tests.conftest import AUTH_HEADERS, MOCK_LESSON_CONTENT, MOCK_QUIZ_JSON

pytestmark = pytest.mark.asyncio


class TestGenerateLessonContent:
    """POST /api/v1/lessons/{lesson_id}/content tests."""

    async def test_generate_lesson_content_returns_200(self, client, app):
        """Verify lesson content generation returns 200. [TASK-015] [BRD-FR-004]"""
        app.state.content_service._client.generate = AsyncMock(
            return_value=MOCK_LESSON_CONTENT
        )
        resp = await client.post("/api/v1/lessons/1/content", headers=AUTH_HEADERS)
        assert resp.status_code == 200
        data = resp.json()
        assert data["lesson_id"] == 1
        assert "content_markdown" in data
        assert "topic" in data
        assert "level" in data
        assert "generated_at" in data

    async def test_generate_lesson_content_returns_markdown(self, client, app):
        """Verify response contains Markdown content. [TASK-015] [BRD-FR-015]"""
        app.state.content_service._client.generate = AsyncMock(
            return_value=MOCK_LESSON_CONTENT
        )
        resp = await client.post("/api/v1/lessons/1/content", headers=AUTH_HEADERS)
        data = resp.json()
        assert "# Mock Lesson" in data["content_markdown"]

    async def test_generate_lesson_nonexistent_returns_404(self, client):
        """Verify 404 for non-existent lesson. [TASK-015] [BRD-FR-004]"""
        resp = await client.post(
            "/api/v1/lessons/9999/content", headers=AUTH_HEADERS
        )
        assert resp.status_code == 404
        data = resp.json()
        assert data["error"]["code"] == "LESSON_NOT_FOUND"

    async def test_generate_lesson_ai_error_returns_503(self, client, app):
        """Verify AI service errors propagate as 503. [TASK-015] [BRD-AI-006]"""
        from src.exceptions import AIServiceUnavailableError

        app.state.content_service._client.generate = AsyncMock(
            side_effect=AIServiceUnavailableError(details="timeout")
        )
        resp = await client.post("/api/v1/lessons/1/content", headers=AUTH_HEADERS)
        assert resp.status_code == 503


class TestGenerateQuiz:
    """POST /api/v1/lessons/{lesson_id}/quiz tests."""

    async def test_generate_quiz_returns_200(self, client, app):
        """Verify quiz generation returns 200 with quiz data. [TASK-018] [BRD-FR-005]"""
        app.state.content_service._client.generate = AsyncMock(
            return_value=MOCK_QUIZ_JSON
        )
        resp = await client.post("/api/v1/lessons/1/quiz", headers=AUTH_HEADERS)
        assert resp.status_code == 200
        data = resp.json()
        assert "quiz_id" in data
        assert data["lesson_id"] == 1
        assert "questions" in data
        assert len(data["questions"]) >= 3
        assert "generated_at" in data

    async def test_generate_quiz_question_schema(self, client, app):
        """Verify each quiz question has correct schema. [TASK-018] [BRD-AI-008]"""
        app.state.content_service._client.generate = AsyncMock(
            return_value=MOCK_QUIZ_JSON
        )
        resp = await client.post("/api/v1/lessons/1/quiz", headers=AUTH_HEADERS)
        data = resp.json()
        for q in data["questions"]:
            assert "question" in q
            assert "options" in q
            assert len(q["options"]) == 4
            assert "correct_answer" in q
            assert q["correct_answer"] in q["options"]
            assert "explanation" in q

    async def test_generate_quiz_nonexistent_lesson_returns_404(self, client):
        """Verify 404 for non-existent lesson. [TASK-018] [BRD-FR-005]"""
        resp = await client.post(
            "/api/v1/lessons/9999/quiz", headers=AUTH_HEADERS
        )
        assert resp.status_code == 404

    async def test_generate_quiz_ai_error_returns_503(self, client, app):
        """Verify AI service errors propagate as 503. [TASK-018] [BRD-AI-006]"""
        from src.exceptions import AIServiceUnavailableError

        app.state.content_service._client.generate = AsyncMock(
            side_effect=AIServiceUnavailableError(details="timeout")
        )
        resp = await client.post("/api/v1/lessons/1/quiz", headers=AUTH_HEADERS)
        assert resp.status_code == 503

"""Tests for progress tracking endpoints.

Covers: BRD-FR-007, BRD-FR-008, TASK-021, TASK-022
"""

from __future__ import annotations

import pytest

from tests.conftest import AUTH_HEADERS

pytestmark = pytest.mark.asyncio


class TestGetProgress:
    """GET /api/v1/progress/{user_id} tests."""

    async def test_get_progress_new_user(self, client):
        """Verify new user gets all courses with zero progress. [TASK-022] [BRD-FR-007]"""
        resp = await client.get(
            "/api/v1/progress/brand-new-user", headers=AUTH_HEADERS
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["user_id"] == "brand-new-user"
        assert "courses" in data
        assert len(data["courses"]) == 6
        for course in data["courses"]:
            assert course["completed_lessons"] == 0
            assert course["completion_percentage"] == 0.0
            assert "quiz_scores" in course

    async def test_get_progress_response_schema(self, client):
        """Verify progress response has all required fields. [TASK-022] [BRD-FR-007]"""
        resp = await client.get(
            "/api/v1/progress/schema-user", headers=AUTH_HEADERS
        )
        data = resp.json()
        for course in data["courses"]:
            assert "course_id" in course
            assert "course_title" in course
            assert "completed_lessons" in course
            assert "total_lessons" in course
            assert "quiz_scores" in course
            assert "completion_percentage" in course

    async def test_get_progress_after_completion(self, client):
        """Verify progress reflects lesson completion. [TASK-022] [BRD-FR-007]"""
        # Mark lesson 1 complete
        await client.post(
            "/api/v1/progress/progress-user/complete",
            headers=AUTH_HEADERS,
            json={"lesson_id": 1},
        )
        resp = await client.get(
            "/api/v1/progress/progress-user", headers=AUTH_HEADERS
        )
        data = resp.json()
        # Find the course that lesson 1 belongs to (course 1)
        course_1 = next(c for c in data["courses"] if c["course_id"] == 1)
        assert course_1["completed_lessons"] >= 1
        assert course_1["completion_percentage"] > 0.0


class TestMarkLessonComplete:
    """POST /api/v1/progress/{user_id}/complete tests."""

    async def test_mark_lesson_complete_returns_200(self, client):
        """Verify marking lesson complete returns 200. [TASK-021] [BRD-FR-008]"""
        resp = await client.post(
            "/api/v1/progress/complete-user/complete",
            headers=AUTH_HEADERS,
            json={"lesson_id": 1},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["user_id"] == "complete-user"
        assert data["lesson_id"] == 1
        assert data["status"] == "completed"
        assert "updated_at" in data

    async def test_mark_lesson_complete_idempotent(self, client):
        """Verify duplicate completions are idempotent. [TASK-021] [BRD-FR-008]"""
        body = {"lesson_id": 2}
        resp1 = await client.post(
            "/api/v1/progress/idem-user/complete",
            headers=AUTH_HEADERS,
            json=body,
        )
        resp2 = await client.post(
            "/api/v1/progress/idem-user/complete",
            headers=AUTH_HEADERS,
            json=body,
        )
        assert resp1.status_code == 200
        assert resp2.status_code == 200

        # Check progress shows only 1 completion
        progress = await client.get(
            "/api/v1/progress/idem-user", headers=AUTH_HEADERS
        )
        data = progress.json()
        total_completed = sum(c["completed_lessons"] for c in data["courses"])
        assert total_completed == 1

    async def test_mark_nonexistent_lesson_returns_404(self, client):
        """Verify 404 for non-existent lesson. [TASK-021] [BRD-FR-008]"""
        resp = await client.post(
            "/api/v1/progress/error-user/complete",
            headers=AUTH_HEADERS,
            json={"lesson_id": 99999},
        )
        assert resp.status_code == 404

    async def test_mark_lesson_invalid_id_returns_422(self, client):
        """Verify 422 for invalid lesson_id (<=0). [TASK-021] [BRD-FR-012]"""
        resp = await client.post(
            "/api/v1/progress/invalid-user/complete",
            headers=AUTH_HEADERS,
            json={"lesson_id": 0},
        )
        assert resp.status_code == 422

    async def test_mark_lesson_missing_body_returns_422(self, client):
        """Verify 422 when request body is missing. [TASK-021] [BRD-FR-012]"""
        resp = await client.post(
            "/api/v1/progress/nobody-user/complete",
            headers=AUTH_HEADERS,
            json={},
        )
        assert resp.status_code == 422

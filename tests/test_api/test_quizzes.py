"""Tests for quiz submission and scoring endpoint.

Covers: BRD-FR-006, BRD-FR-011, BRD-NFR-012, TASK-020
"""

from __future__ import annotations

import json

import pytest

from tests.conftest import AUTH_HEADERS

pytestmark = pytest.mark.asyncio


class TestSubmitQuiz:
    """POST /api/v1/quiz/{quiz_id}/submit tests."""

    async def test_submit_quiz_all_correct(self, client, seeded_quiz):
        """Verify scoring when all answers are correct. [TASK-020] [BRD-FR-006]"""
        quiz_id = seeded_quiz["quiz_id"]
        correct_answers = [q["correct_answer"] for q in seeded_quiz["questions"]]
        resp = await client.post(
            f"/api/v1/quiz/{quiz_id}/submit",
            headers=AUTH_HEADERS,
            json={"user_id": "test-user-1", "answers": correct_answers},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["quiz_id"] == quiz_id
        assert data["user_id"] == "test-user-1"
        assert data["score"] == 3
        assert data["total"] == 3
        assert data["percentage"] == 100.0
        assert all(r["correct"] for r in data["results"])

    async def test_submit_quiz_some_wrong(self, client, seeded_quiz):
        """Verify scoring with mixed correct/wrong answers. [TASK-020] [BRD-FR-006]"""
        quiz_id = seeded_quiz["quiz_id"]
        answers = ["YAML", "wrong-answer", ".github/workflows/"]
        resp = await client.post(
            f"/api/v1/quiz/{quiz_id}/submit",
            headers=AUTH_HEADERS,
            json={"user_id": "test-user-2", "answers": answers},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["score"] == 2
        assert data["total"] == 3
        assert data["percentage"] == 66.7
        assert data["results"][0]["correct"] is True
        assert data["results"][1]["correct"] is False
        assert data["results"][2]["correct"] is True

    async def test_submit_quiz_all_wrong(self, client, seeded_quiz):
        """Verify scoring when all answers are wrong. [TASK-020] [BRD-FR-006]"""
        quiz_id = seeded_quiz["quiz_id"]
        answers = ["JSON", "run: push", ".actions/"]
        resp = await client.post(
            f"/api/v1/quiz/{quiz_id}/submit",
            headers=AUTH_HEADERS,
            json={"user_id": "test-user-3", "answers": answers},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["score"] == 0
        assert data["percentage"] == 0.0
        assert all(not r["correct"] for r in data["results"])

    async def test_submit_quiz_includes_explanations(self, client, seeded_quiz):
        """Verify each result includes an explanation. [TASK-020] [BRD-FR-006]"""
        quiz_id = seeded_quiz["quiz_id"]
        answers = ["YAML", "on: push", ".github/workflows/"]
        resp = await client.post(
            f"/api/v1/quiz/{quiz_id}/submit",
            headers=AUTH_HEADERS,
            json={"user_id": "test-user-4", "answers": answers},
        )
        data = resp.json()
        for result in data["results"]:
            assert "explanation" in result
            assert len(result["explanation"]) > 0

    async def test_submit_quiz_wrong_answer_count_returns_422(
        self, client, seeded_quiz
    ):
        """Verify 422 when answer count doesn't match questions. [TASK-020] [BRD-FR-006]"""
        quiz_id = seeded_quiz["quiz_id"]
        resp = await client.post(
            f"/api/v1/quiz/{quiz_id}/submit",
            headers=AUTH_HEADERS,
            json={"user_id": "test-user-5", "answers": ["YAML"]},
        )
        assert resp.status_code == 422

    async def test_submit_quiz_nonexistent_returns_404(self, client):
        """Verify 404 for non-existent quiz. [TASK-020] [BRD-FR-006]"""
        resp = await client.post(
            "/api/v1/quiz/99999/submit",
            headers=AUTH_HEADERS,
            json={"user_id": "test-user-6", "answers": ["A", "B", "C"]},
        )
        assert resp.status_code == 404
        data = resp.json()
        assert data["error"]["code"] == "QUIZ_NOT_FOUND"

    async def test_submit_quiz_persists_attempt(self, client, seeded_quiz, db_conn):
        """Verify quiz attempt is persisted in the database. [TASK-020] [BRD-FR-011]"""
        quiz_id = seeded_quiz["quiz_id"]
        answers = ["YAML", "on: push", ".github/workflows/"]
        await client.post(
            f"/api/v1/quiz/{quiz_id}/submit",
            headers=AUTH_HEADERS,
            json={"user_id": "persist-user", "answers": answers},
        )
        cursor = await db_conn.execute(
            "SELECT user_id, score, total FROM quiz_attempts WHERE quiz_id = ? AND user_id = ?",
            (quiz_id, "persist-user"),
        )
        row = await cursor.fetchone()
        assert row is not None
        assert row[0] == "persist-user"
        assert row[1] == 3
        assert row[2] == 3

    async def test_submit_quiz_missing_user_id_returns_422(self, client, seeded_quiz):
        """Verify 422 when user_id is missing. [TASK-020] [BRD-FR-012]"""
        quiz_id = seeded_quiz["quiz_id"]
        resp = await client.post(
            f"/api/v1/quiz/{quiz_id}/submit",
            headers=AUTH_HEADERS,
            json={"answers": ["A", "B", "C"]},
        )
        assert resp.status_code == 422

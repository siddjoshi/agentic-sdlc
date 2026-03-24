"""Repository for quiz and quiz attempt CRUD operations."""

from __future__ import annotations

import json

import aiosqlite

from src.exceptions import QuizNotFoundError


class QuizRepository:
    """Provides CRUD methods for quizzes and quiz attempts."""

    def __init__(self, conn: aiosqlite.Connection) -> None:
        self._conn = conn

    async def create_quiz(self, lesson_id: int, questions_json: str) -> int:
        """Insert a new quiz record and return its ID."""
        cursor = await self._conn.execute(
            "INSERT INTO quizzes (lesson_id, questions_json) VALUES (?, ?)",
            (lesson_id, questions_json),
        )
        await self._conn.commit()
        return cursor.lastrowid  # type: ignore[return-value]

    async def get_quiz(self, quiz_id: int) -> dict | None:
        """Retrieve a quiz by ID, or return None if not found."""
        cursor = await self._conn.execute(
            "SELECT id, lesson_id, questions_json, generated_at FROM quizzes WHERE id = ?",
            (quiz_id,),
        )
        row = await cursor.fetchone()
        if row is None:
            return None
        return {
            "id": row[0],
            "lesson_id": row[1],
            "questions_json": row[2],
            "generated_at": row[3],
        }

    async def create_attempt(
        self,
        quiz_id: int,
        user_id: str,
        score: int,
        total: int,
        percentage: float,
        answers_json: str,
    ) -> int:
        """Store a quiz attempt and return its ID."""
        cursor = await self._conn.execute(
            "INSERT INTO quiz_attempts (quiz_id, user_id, score, total, percentage, answers_json) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (quiz_id, user_id, score, total, percentage, answers_json),
        )
        await self._conn.commit()
        return cursor.lastrowid  # type: ignore[return-value]

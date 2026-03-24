"""Repository for user progress CRUD operations."""

from __future__ import annotations

from datetime import datetime

import aiosqlite


class ProgressRepository:
    """Provides CRUD methods for user progress tracking."""

    def __init__(self, conn: aiosqlite.Connection) -> None:
        self._conn = conn

    async def mark_complete(self, user_id: str, lesson_id: int) -> datetime:
        """Mark a lesson as completed for a user (idempotent).

        Uses ``INSERT OR IGNORE`` so duplicate completions are safe.
        Returns the ``completed_at`` timestamp.
        """
        await self._conn.execute(
            "INSERT OR IGNORE INTO user_progress (user_id, lesson_id) VALUES (?, ?)",
            (user_id, lesson_id),
        )
        await self._conn.commit()

        cursor = await self._conn.execute(
            "SELECT completed_at FROM user_progress WHERE user_id = ? AND lesson_id = ?",
            (user_id, lesson_id),
        )
        row = await cursor.fetchone()
        return datetime.fromisoformat(row[0]) if row else datetime.utcnow()

    async def get_progress(self, user_id: str) -> list[dict]:
        """Return per-course progress aggregation for a user."""
        cursor = await self._conn.execute(
            """
            SELECT
                c.id AS course_id,
                c.title AS course_title,
                COUNT(DISTINCT up.lesson_id) AS completed_lessons,
                COUNT(DISTINCT l.id) AS total_lessons,
                ROUND(
                    CASE WHEN COUNT(DISTINCT l.id) = 0 THEN 0
                    ELSE COUNT(DISTINCT up.lesson_id) * 100.0 / COUNT(DISTINCT l.id)
                    END, 1
                ) AS completion_percentage
            FROM courses c
            JOIN lessons l ON l.course_id = c.id
            LEFT JOIN user_progress up ON up.lesson_id = l.id AND up.user_id = ?
            GROUP BY c.id, c.title
            ORDER BY c.id
            """,
            (user_id,),
        )
        rows = await cursor.fetchall()
        return [
            {
                "course_id": r[0],
                "course_title": r[1],
                "completed_lessons": r[2],
                "total_lessons": r[3],
                "completion_percentage": r[4],
            }
            for r in rows
        ]

    async def get_quiz_scores(self, user_id: str, course_id: int) -> list[float]:
        """Return quiz attempt percentages for a user in a specific course."""
        cursor = await self._conn.execute(
            """
            SELECT qa.percentage
            FROM quiz_attempts qa
            JOIN quizzes q ON qa.quiz_id = q.id
            JOIN lessons l ON q.lesson_id = l.id
            WHERE qa.user_id = ? AND l.course_id = ?
            ORDER BY qa.attempted_at
            """,
            (user_id, course_id),
        )
        rows = await cursor.fetchall()
        return [r[0] for r in rows]

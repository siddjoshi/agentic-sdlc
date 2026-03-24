"""Repository for course and lesson CRUD operations."""

from __future__ import annotations

import aiosqlite

from src.exceptions import CourseNotFoundError, LessonNotFoundError


class CourseRepository:
    """Provides CRUD methods for courses and lessons."""

    def __init__(self, conn: aiosqlite.Connection) -> None:
        self._conn = conn

    async def list_courses(
        self, limit: int = 20, offset: int = 0
    ) -> tuple[list[dict], int]:
        """Return paginated courses with total count.

        Each course dict includes a ``total_lessons`` field.
        """
        cursor = await self._conn.execute(
            """
            SELECT c.id, c.title, c.description, c.topic, c.level, c.created_at,
                   COUNT(l.id) AS total_lessons
            FROM courses c
            LEFT JOIN lessons l ON l.course_id = c.id
            GROUP BY c.id
            ORDER BY c.id
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        )
        rows = await cursor.fetchall()
        courses = [
            {
                "id": r[0],
                "title": r[1],
                "description": r[2],
                "topic": r[3],
                "level": r[4],
                "created_at": r[5],
                "total_lessons": r[6],
            }
            for r in rows
        ]

        count_cursor = await self._conn.execute("SELECT COUNT(*) FROM courses")
        total_row = await count_cursor.fetchone()
        total = total_row[0] if total_row else 0

        return courses, total

    async def get_course(self, course_id: int) -> dict:
        """Return a single course with its lessons.

        Raises ``CourseNotFoundError`` if the course does not exist.
        """
        cursor = await self._conn.execute(
            "SELECT id, title, description, topic, level, created_at FROM courses WHERE id = ?",
            (course_id,),
        )
        row = await cursor.fetchone()
        if row is None:
            raise CourseNotFoundError(course_id)

        course = {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "topic": row[3],
            "level": row[4],
            "created_at": row[5],
        }

        lesson_cursor = await self._conn.execute(
            'SELECT id, title, level, "order" FROM lessons WHERE course_id = ? ORDER BY "order"',
            (course_id,),
        )
        lesson_rows = await lesson_cursor.fetchall()
        course["lessons"] = [
            {"id": lr[0], "title": lr[1], "level": lr[2], "order": lr[3]}
            for lr in lesson_rows
        ]
        return course

    async def list_lessons(
        self, course_id: int, limit: int = 20, offset: int = 0
    ) -> tuple[list[dict], int]:
        """Return paginated lessons for a course.

        Raises ``CourseNotFoundError`` if the course does not exist.
        """
        # Verify course exists
        check = await self._conn.execute(
            "SELECT id FROM courses WHERE id = ?", (course_id,)
        )
        if await check.fetchone() is None:
            raise CourseNotFoundError(course_id)

        cursor = await self._conn.execute(
            'SELECT id, title, level, "order" FROM lessons WHERE course_id = ? ORDER BY "order" LIMIT ? OFFSET ?',
            (course_id, limit, offset),
        )
        rows = await cursor.fetchall()
        lessons = [
            {"id": r[0], "title": r[1], "level": r[2], "order": r[3]}
            for r in rows
        ]

        count_cursor = await self._conn.execute(
            "SELECT COUNT(*) FROM lessons WHERE course_id = ?", (course_id,)
        )
        total_row = await count_cursor.fetchone()
        total = total_row[0] if total_row else 0

        return lessons, total

    async def get_lesson(self, lesson_id: int) -> dict:
        """Return a single lesson by ID.

        Raises ``LessonNotFoundError`` if the lesson does not exist.
        """
        cursor = await self._conn.execute(
            'SELECT id, course_id, title, level, "order", objectives, created_at '
            "FROM lessons WHERE id = ?",
            (lesson_id,),
        )
        row = await cursor.fetchone()
        if row is None:
            raise LessonNotFoundError(lesson_id)

        return {
            "id": row[0],
            "course_id": row[1],
            "title": row[2],
            "level": row[3],
            "order": row[4],
            "objectives": row[5],
            "created_at": row[6],
        }

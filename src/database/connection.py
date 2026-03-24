"""Database connection manager and schema initialization."""

from __future__ import annotations

import logging
from pathlib import Path

import aiosqlite

from src.database.seed import seed_database

logger = logging.getLogger(__name__)

# SQL for creating all tables and indexes
_SCHEMA_SQL = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    topic TEXT NOT NULL CHECK (topic IN ('github-actions', 'github-copilot', 'github-advanced-security')),
    level TEXT NOT NULL CHECK (level IN ('beginner', 'intermediate')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    level TEXT NOT NULL CHECK (level IN ('beginner', 'intermediate')),
    "order" INTEGER NOT NULL CHECK ("order" >= 1),
    objectives TEXT NOT NULL DEFAULT '[]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    UNIQUE (course_id, "order")
);

CREATE TABLE IF NOT EXISTS quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lesson_id INTEGER NOT NULL,
    questions_json TEXT NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id)
);

CREATE TABLE IF NOT EXISTS quiz_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER NOT NULL,
    user_id TEXT NOT NULL,
    score INTEGER NOT NULL CHECK (score >= 0),
    total INTEGER NOT NULL CHECK (total >= 1),
    percentage REAL NOT NULL CHECK (percentage >= 0 AND percentage <= 100),
    answers_json TEXT NOT NULL,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
);

CREATE TABLE IF NOT EXISTS user_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    lesson_id INTEGER NOT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id),
    UNIQUE (user_id, lesson_id)
);

CREATE INDEX IF NOT EXISTS idx_lessons_course_id ON lessons(course_id);
CREATE INDEX IF NOT EXISTS idx_quizzes_lesson_id ON quizzes(lesson_id);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_user_id ON quiz_attempts(user_id);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_quiz_id ON quiz_attempts(quiz_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_lesson_id ON user_progress(lesson_id);
"""


class DatabaseManager:
    """Manages the async SQLite connection lifecycle, schema creation, and seeding."""

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._connection: aiosqlite.Connection | None = None

    async def initialize(self) -> None:
        """Create tables, enable WAL mode, seed data, and keep a connection open."""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)

        conn = await aiosqlite.connect(self.db_path)
        conn.row_factory = aiosqlite.Row
        # Execute schema statements one by one (PRAGMA cannot be in executescript)
        for statement in _SCHEMA_SQL.strip().split(";"):
            statement = statement.strip()
            if statement:
                await conn.execute(statement)
        await conn.commit()

        await seed_database(conn)

        self._connection = conn
        logger.info("Database initialized at %s", self.db_path)

    async def get_connection(self) -> aiosqlite.Connection:
        """Return the active database connection."""
        if self._connection is None:
            raise RuntimeError("DatabaseManager has not been initialized")
        return self._connection

    async def close(self) -> None:
        """Close the database connection."""
        if self._connection is not None:
            await self._connection.close()
            self._connection = None
            logger.info("Database connection closed")

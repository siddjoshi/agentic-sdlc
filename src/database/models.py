"""Pydantic models mirroring database rows."""

from datetime import datetime

from pydantic import BaseModel, Field


class CourseRow(BaseModel):
    """Mirrors the courses table."""

    id: int
    title: str
    description: str
    topic: str = Field(
        ...,
        description="One of: 'github-actions', 'github-copilot', 'github-advanced-security'",
    )
    level: str = Field(..., description="'beginner' or 'intermediate'")
    created_at: datetime


class LessonRow(BaseModel):
    """Mirrors the lessons table."""

    id: int
    course_id: int
    title: str
    level: str
    order: int = Field(..., ge=1, description="Sequence order within the course")
    objectives: str = Field(..., description="JSON array of learning objectives")
    created_at: datetime


class QuizRow(BaseModel):
    """Mirrors the quizzes table."""

    id: int
    lesson_id: int
    questions_json: str = Field(
        ..., description="JSON serialization of quiz questions"
    )
    generated_at: datetime


class QuizAttemptRow(BaseModel):
    """Mirrors the quiz_attempts table."""

    id: int
    quiz_id: int
    user_id: str
    score: int
    total: int
    percentage: float
    answers_json: str = Field(
        ..., description="JSON serialization of user's answers"
    )
    attempted_at: datetime


class UserProgressRow(BaseModel):
    """Mirrors the user_progress table."""

    id: int
    user_id: str
    lesson_id: int
    completed_at: datetime


class CourseProgressRow(BaseModel):
    """Computed model for per-course progress."""

    course_id: int
    course_title: str
    completed_lessons: int
    total_lessons: int
    completion_percentage: float

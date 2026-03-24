"""Response body Pydantic models."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Course catalog
# ---------------------------------------------------------------------------

class CourseResponse(BaseModel):
    """Single course in the catalog."""

    id: int
    title: str
    description: str
    level: str
    total_lessons: int


class CourseListResponse(BaseModel):
    """Paginated list of courses."""

    courses: list[CourseResponse]
    total: int
    limit: int
    offset: int


class LessonSummary(BaseModel):
    """Lesson metadata in a list context."""

    id: int
    title: str
    level: str
    order: int


class CourseDetailResponse(BaseModel):
    """Course details with lesson outline."""

    id: int
    title: str
    description: str
    level: str
    lessons: list[LessonSummary]


class LessonListResponse(BaseModel):
    """Paginated list of lessons for a course."""

    lessons: list[LessonSummary]
    total: int
    limit: int
    offset: int


# ---------------------------------------------------------------------------
# AI-generated content
# ---------------------------------------------------------------------------

class LessonContentResponse(BaseModel):
    """AI-generated lesson content."""

    lesson_id: int
    topic: str
    level: str
    content_markdown: str
    generated_at: datetime


class QuizQuestionResponse(BaseModel):
    """A single quiz question."""

    question: str
    options: list[str] = Field(..., min_length=4, max_length=4)
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    """Generated quiz."""

    quiz_id: int
    lesson_id: int
    topic: str
    level: str
    questions: list[QuizQuestionResponse]
    generated_at: datetime


# ---------------------------------------------------------------------------
# Quiz scoring
# ---------------------------------------------------------------------------

class QuestionResult(BaseModel):
    """Per-question result in a scored quiz."""

    correct: bool
    explanation: str


class QuizResult(BaseModel):
    """Scored quiz result."""

    quiz_id: int
    user_id: str
    score: int
    total: int
    percentage: float
    results: list[QuestionResult]


# ---------------------------------------------------------------------------
# Progress tracking
# ---------------------------------------------------------------------------

class CourseProgress(BaseModel):
    """Progress for a single course."""

    course_id: int
    course_title: str
    completed_lessons: int
    total_lessons: int
    quiz_scores: list[float]
    completion_percentage: float


class ProgressResponse(BaseModel):
    """User's progress across all courses."""

    user_id: str
    courses: list[CourseProgress]


class ProgressUpdateResponse(BaseModel):
    """Confirmation of a lesson completion."""

    user_id: str
    lesson_id: int
    status: str = "completed"
    updated_at: datetime


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="'healthy' or 'degraded'")
    version: str
    database: str = Field(..., description="'connected' or 'disconnected'")

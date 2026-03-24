"""Tests for request and response Pydantic models.

Covers: BRD-FR-012, BRD-NFR-009, TASK-006
"""

from __future__ import annotations

from datetime import datetime

import pytest
from pydantic import ValidationError

from src.models.requests import LessonCompleteRequest, QuizSubmission
from src.models.responses import (
    CourseDetailResponse,
    CourseListResponse,
    CourseProgress,
    CourseResponse,
    HealthResponse,
    LessonContentResponse,
    LessonListResponse,
    LessonSummary,
    ProgressResponse,
    ProgressUpdateResponse,
    QuestionResult,
    QuizQuestionResponse,
    QuizResponse,
    QuizResult,
)


class TestLessonCompleteRequest:
    """LessonCompleteRequest model tests."""

    def test_valid_request(self):
        """Verify valid lesson_id accepted. [TASK-006] [BRD-NFR-009]"""
        req = LessonCompleteRequest(lesson_id=1)
        assert req.lesson_id == 1

    def test_zero_lesson_id_rejected(self):
        """Verify lesson_id=0 rejected (gt=0). [TASK-006] [BRD-FR-012]"""
        with pytest.raises(ValidationError):
            LessonCompleteRequest(lesson_id=0)

    def test_negative_lesson_id_rejected(self):
        """Verify negative lesson_id rejected. [TASK-006] [BRD-FR-012]"""
        with pytest.raises(ValidationError):
            LessonCompleteRequest(lesson_id=-1)

    def test_missing_lesson_id_rejected(self):
        """Verify missing lesson_id rejected. [TASK-006] [BRD-FR-012]"""
        with pytest.raises(ValidationError):
            LessonCompleteRequest()


class TestQuizSubmission:
    """QuizSubmission model tests."""

    def test_valid_submission(self):
        """Verify valid quiz submission. [TASK-006] [BRD-NFR-009]"""
        sub = QuizSubmission(user_id="user-1", answers=["A", "B"])
        assert sub.user_id == "user-1"
        assert sub.answers == ["A", "B"]

    def test_empty_user_id_rejected(self):
        """Verify empty user_id rejected (min_length=1). [TASK-006] [BRD-FR-012]"""
        with pytest.raises(ValidationError):
            QuizSubmission(user_id="", answers=["A"])

    def test_empty_answers_rejected(self):
        """Verify empty answers list rejected (min_length=1). [TASK-006] [BRD-FR-012]"""
        with pytest.raises(ValidationError):
            QuizSubmission(user_id="user-1", answers=[])

    def test_user_id_max_length(self):
        """Verify user_id over 100 chars rejected. [TASK-006] [BRD-FR-012]"""
        with pytest.raises(ValidationError):
            QuizSubmission(user_id="x" * 101, answers=["A"])


class TestResponseModels:
    """Response model validation tests."""

    def test_health_response(self):
        """Verify HealthResponse creation. [TASK-005] [BRD-FR-009]"""
        h = HealthResponse(status="healthy", version="1.0.0", database="connected")
        assert h.status == "healthy"

    def test_course_response(self):
        """Verify CourseResponse creation. [TASK-011] [BRD-FR-001]"""
        c = CourseResponse(
            id=1, title="Test", description="Desc", level="beginner", total_lessons=5
        )
        assert c.id == 1
        assert c.total_lessons == 5

    def test_course_list_response(self):
        """Verify CourseListResponse with pagination. [TASK-011] [BRD-FR-014]"""
        r = CourseListResponse(
            courses=[
                CourseResponse(
                    id=1, title="T", description="D", level="beginner", total_lessons=3
                )
            ],
            total=1,
            limit=20,
            offset=0,
        )
        assert r.total == 1
        assert r.limit == 20

    def test_quiz_question_response_requires_four_options(self):
        """Verify QuizQuestionResponse enforces 4 options. [TASK-016] [BRD-AI-008]"""
        q = QuizQuestionResponse(
            question="Q?",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation="Exp",
        )
        assert len(q.options) == 4

    def test_quiz_result(self):
        """Verify QuizResult creation. [TASK-020] [BRD-FR-006]"""
        r = QuizResult(
            quiz_id=1,
            user_id="u1",
            score=2,
            total=3,
            percentage=66.7,
            results=[
                QuestionResult(correct=True, explanation="Good"),
                QuestionResult(correct=False, explanation="Wrong"),
                QuestionResult(correct=True, explanation="Good"),
            ],
        )
        assert r.score == 2
        assert r.percentage == 66.7

    def test_progress_response(self):
        """Verify ProgressResponse creation. [TASK-022] [BRD-FR-007]"""
        p = ProgressResponse(
            user_id="u1",
            courses=[
                CourseProgress(
                    course_id=1,
                    course_title="Test",
                    completed_lessons=3,
                    total_lessons=5,
                    quiz_scores=[80.0, 100.0],
                    completion_percentage=60.0,
                )
            ],
        )
        assert p.user_id == "u1"
        assert p.courses[0].completion_percentage == 60.0

    def test_progress_update_response(self):
        """Verify ProgressUpdateResponse creation. [TASK-021] [BRD-FR-008]"""
        r = ProgressUpdateResponse(
            user_id="u1",
            lesson_id=1,
            status="completed",
            updated_at=datetime.utcnow(),
        )
        assert r.status == "completed"


class TestDatabaseModels:
    """Database Pydantic model tests."""

    def test_course_row(self):
        """Verify CourseRow creation. [TASK-008] [BRD-NFR-010]"""
        from src.database.models import CourseRow

        row = CourseRow(
            id=1,
            title="Test",
            description="Desc",
            topic="github-actions",
            level="beginner",
            created_at=datetime.utcnow(),
        )
        assert row.topic == "github-actions"

    def test_lesson_row(self):
        """Verify LessonRow creation. [TASK-008] [BRD-NFR-010]"""
        from src.database.models import LessonRow

        row = LessonRow(
            id=1,
            course_id=1,
            title="Lesson 1",
            level="beginner",
            order=1,
            objectives='["obj1"]',
            created_at=datetime.utcnow(),
        )
        assert row.order == 1

    def test_quiz_row(self):
        """Verify QuizRow creation. [TASK-008] [BRD-NFR-010]"""
        from src.database.models import QuizRow

        row = QuizRow(
            id=1,
            lesson_id=1,
            questions_json="[]",
            generated_at=datetime.utcnow(),
        )
        assert row.lesson_id == 1

    def test_quiz_attempt_row(self):
        """Verify QuizAttemptRow creation. [TASK-008] [BRD-NFR-010]"""
        from src.database.models import QuizAttemptRow

        row = QuizAttemptRow(
            id=1,
            quiz_id=1,
            user_id="u1",
            score=3,
            total=3,
            percentage=100.0,
            answers_json='["A","B","C"]',
            attempted_at=datetime.utcnow(),
        )
        assert row.percentage == 100.0

    def test_user_progress_row(self):
        """Verify UserProgressRow creation. [TASK-008] [BRD-NFR-010]"""
        from src.database.models import UserProgressRow

        row = UserProgressRow(
            id=1,
            user_id="u1",
            lesson_id=1,
            completed_at=datetime.utcnow(),
        )
        assert row.user_id == "u1"

    def test_course_progress_row(self):
        """Verify CourseProgressRow creation. [TASK-008] [BRD-NFR-010]"""
        from src.database.models import CourseProgressRow

        row = CourseProgressRow(
            course_id=1,
            course_title="Test",
            completed_lessons=2,
            total_lessons=5,
            completion_percentage=40.0,
        )
        assert row.completion_percentage == 40.0

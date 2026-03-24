"""Tests for custom exception classes and exception handlers.

Covers: BRD-FR-012, TASK-006
"""

from __future__ import annotations

import pytest

from src.exceptions import (
    AIRateLimitError,
    AIResponseValidationError,
    AIServiceUnavailableError,
    AppError,
    CourseNotFoundError,
    DatabaseError,
    LessonNotFoundError,
    QuizNotFoundError,
)


class TestExceptionHierarchy:
    """Exception class tests."""

    def test_app_error_base(self):
        """Verify AppError base class. [TASK-006] [BRD-FR-012]"""
        err = AppError(code="TEST", message="test error", status_code=400)
        assert err.code == "TEST"
        assert err.message == "test error"
        assert err.status_code == 400
        assert err.details is None
        assert err.retry_after is None

    def test_course_not_found_error(self):
        """Verify CourseNotFoundError. [TASK-006] [BRD-FR-012]"""
        err = CourseNotFoundError(42)
        assert err.status_code == 404
        assert err.code == "COURSE_NOT_FOUND"
        assert "42" in err.message

    def test_lesson_not_found_error(self):
        """Verify LessonNotFoundError. [TASK-006] [BRD-FR-012]"""
        err = LessonNotFoundError(7)
        assert err.status_code == 404
        assert err.code == "LESSON_NOT_FOUND"
        assert "7" in err.message

    def test_quiz_not_found_error(self):
        """Verify QuizNotFoundError. [TASK-006] [BRD-FR-012]"""
        err = QuizNotFoundError(99)
        assert err.status_code == 404
        assert err.code == "QUIZ_NOT_FOUND"
        assert "99" in err.message

    def test_ai_service_unavailable_error(self):
        """Verify AIServiceUnavailableError. [TASK-006] [BRD-AI-006]"""
        err = AIServiceUnavailableError(details="connection refused")
        assert err.status_code == 503
        assert err.code == "AI_SERVICE_UNAVAILABLE"
        assert err.retry_after == 30
        assert err.details == "connection refused"

    def test_ai_rate_limit_error(self):
        """Verify AIRateLimitError. [TASK-006] [BRD-AI-004]"""
        err = AIRateLimitError(details="429 too many requests")
        assert err.status_code == 503
        assert err.code == "AI_RATE_LIMITED"
        assert err.retry_after == 60

    def test_ai_response_validation_error(self):
        """Verify AIResponseValidationError. [TASK-006] [BRD-AI-003]"""
        err = AIResponseValidationError(details="invalid JSON")
        assert err.status_code == 502
        assert err.code == "AI_RESPONSE_INVALID"
        assert err.retry_after == 15

    def test_database_error(self):
        """Verify DatabaseError. [TASK-006]"""
        err = DatabaseError(details="disk full")
        assert err.status_code == 500
        assert err.code == "DATABASE_ERROR"

    def test_all_exceptions_inherit_app_error(self):
        """Verify all custom exceptions inherit from AppError. [TASK-006]"""
        for exc_class in [
            CourseNotFoundError,
            LessonNotFoundError,
            QuizNotFoundError,
            AIServiceUnavailableError,
            AIRateLimitError,
            AIResponseValidationError,
            DatabaseError,
        ]:
            assert issubclass(exc_class, AppError)

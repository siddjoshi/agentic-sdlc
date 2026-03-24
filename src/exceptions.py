"""Custom exception hierarchy and FastAPI exception handlers."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


# ---------------------------------------------------------------------------
# Base exception
# ---------------------------------------------------------------------------

class AppError(Exception):
    """Base exception for all application errors."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 500,
        details: str | None = None,
        retry_after: int | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        self.retry_after = retry_after


# ---------------------------------------------------------------------------
# 404 errors
# ---------------------------------------------------------------------------

class CourseNotFoundError(AppError):
    """Raised when a course ID does not exist."""

    def __init__(self, course_id: int) -> None:
        super().__init__(
            code="COURSE_NOT_FOUND",
            message=f"Course with ID {course_id} was not found.",
            status_code=404,
        )


class LessonNotFoundError(AppError):
    """Raised when a lesson ID does not exist."""

    def __init__(self, lesson_id: int) -> None:
        super().__init__(
            code="LESSON_NOT_FOUND",
            message=f"Lesson with ID {lesson_id} was not found.",
            status_code=404,
        )


class QuizNotFoundError(AppError):
    """Raised when a quiz ID does not exist."""

    def __init__(self, quiz_id: int) -> None:
        super().__init__(
            code="QUIZ_NOT_FOUND",
            message=f"Quiz with ID {quiz_id} was not found.",
            status_code=404,
        )


# ---------------------------------------------------------------------------
# AI / external service errors
# ---------------------------------------------------------------------------

class AIServiceUnavailableError(AppError):
    """Raised when the GitHub Models API is unreachable or returned 5xx."""

    def __init__(self, details: str | None = None) -> None:
        super().__init__(
            code="AI_SERVICE_UNAVAILABLE",
            message="The AI content generation service is temporarily unavailable. Please try again later.",
            status_code=503,
            details=details,
            retry_after=30,
        )


class AIRateLimitError(AppError):
    """Raised when the GitHub Models API returns 429 after all retries."""

    def __init__(self, details: str | None = None) -> None:
        super().__init__(
            code="AI_RATE_LIMITED",
            message="The AI service is rate-limited. Please try again later.",
            status_code=503,
            details=details,
            retry_after=60,
        )


class AIResponseValidationError(AppError):
    """Raised when the AI response fails schema validation after retries."""

    def __init__(self, details: str | None = None) -> None:
        super().__init__(
            code="AI_RESPONSE_INVALID",
            message="The AI service returned an invalid response. Please try again.",
            status_code=502,
            details=details,
            retry_after=15,
        )


# ---------------------------------------------------------------------------
# Database errors
# ---------------------------------------------------------------------------

class DatabaseError(AppError):
    """Raised on unexpected SQLite errors."""

    def __init__(self, details: str | None = None) -> None:
        super().__init__(
            code="DATABASE_ERROR",
            message="An internal database error occurred. Please try again.",
            status_code=500,
            details=details,
        )


# ---------------------------------------------------------------------------
# Handler registration
# ---------------------------------------------------------------------------

def register_exception_handlers(app: FastAPI) -> None:
    """Register custom exception handlers on the FastAPI app."""

    @app.exception_handler(AppError)
    async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
        """Convert any AppError into a structured JSON error response."""
        body: dict = {
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        }
        if exc.retry_after is not None:
            body["error"]["retry_after"] = exc.retry_after
        return JSONResponse(status_code=exc.status_code, content=body)

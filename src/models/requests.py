"""Request body Pydantic models."""

from pydantic import BaseModel, Field


class LessonCompleteRequest(BaseModel):
    """Request body to mark a lesson as completed."""

    lesson_id: int = Field(..., gt=0, description="ID of the lesson to mark complete")


class QuizSubmission(BaseModel):
    """Request body for submitting quiz answers."""

    user_id: str = Field(
        ..., min_length=1, max_length=100, description="Opaque user identifier"
    )
    answers: list[str] = Field(
        ..., min_length=1, description="User's selected answers in question order"
    )

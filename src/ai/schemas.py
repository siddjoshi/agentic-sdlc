"""AI response validation schemas for quiz generation."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from src.exceptions import AIResponseValidationError

logger = logging.getLogger(__name__)


class QuizQuestion(BaseModel):
    """A single multiple-choice quiz question from the AI."""

    question: str = Field(..., description="The question text")
    options: list[str] = Field(
        ..., min_length=4, max_length=4, description="Exactly 4 answer options"
    )
    correct_answer: str = Field(
        ..., description="The correct option (must be in options)"
    )
    explanation: str = Field(..., description="Explanation of the correct answer")

    @field_validator("correct_answer")
    @classmethod
    def correct_answer_in_options(cls, v: str, info) -> str:  # noqa: N805
        """Ensure the correct answer is one of the provided options."""
        options = info.data.get("options", [])
        if options and v not in options:
            raise ValueError(
                f"correct_answer '{v}' is not in options {options}"
            )
        return v


class QuizResponseSchema(BaseModel):
    """Validated quiz response from the AI."""

    quiz_id: Optional[int] = Field(None, description="Assigned after persistence")
    lesson_id: int
    topic: str
    level: str
    questions: list[QuizQuestion] = Field(
        ..., min_length=3, max_length=5, description="3-5 quiz questions"
    )
    generated_at: datetime = Field(default_factory=datetime.utcnow)


def validate_quiz_response(
    raw_json: str,
    lesson_id: int,
    topic: str,
    level: str,
) -> QuizResponseSchema:
    """Parse and validate raw AI JSON into a QuizResponseSchema.

    Handles both a bare JSON array ``[{...}, ...]`` and an object wrapper
    ``{"questions": [{...}, ...]}``.

    Args:
        raw_json: The raw text returned by the AI model.
        lesson_id: The lesson the quiz belongs to.
        topic: Training topic name.
        level: Skill level.

    Returns:
        A validated ``QuizResponseSchema``.

    Raises:
        AIResponseValidationError: If the JSON is invalid or fails validation.
    """
    try:
        # Strip markdown code fences if present
        cleaned = raw_json.strip()
        if cleaned.startswith("```"):
            first_newline = cleaned.index("\n")
            last_fence = cleaned.rfind("```")
            cleaned = cleaned[first_newline + 1 : last_fence].strip()

        data = json.loads(cleaned)

        # Accept both array and {"questions": [...]} formats
        if isinstance(data, list):
            questions_data = data
        elif isinstance(data, dict) and "questions" in data:
            questions_data = data["questions"]
        else:
            raise ValueError("Expected a JSON array or an object with a 'questions' key")

        return QuizResponseSchema(
            lesson_id=lesson_id,
            topic=topic,
            level=level,
            questions=questions_data,
        )

    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Quiz validation failed: %s", exc)
        raise AIResponseValidationError(details=str(exc)) from exc
    except Exception as exc:
        logger.warning("Quiz validation unexpected error: %s", exc)
        raise AIResponseValidationError(details=str(exc)) from exc

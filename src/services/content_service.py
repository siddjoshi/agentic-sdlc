"""Content service — orchestrates AI content generation."""

from __future__ import annotations

import json
import logging
from datetime import datetime

import aiosqlite

from src.ai.client import GitHubModelsClient
from src.ai.prompts import PromptManager
from src.ai.schemas import validate_quiz_response, QuizResponseSchema
from src.exceptions import AIResponseValidationError
from src.repositories.quiz_repository import QuizRepository

logger = logging.getLogger(__name__)


class ContentService:
    """High-level service that orchestrates prompt building, AI API calls,
    response validation, and quiz persistence.

    Follows the Facade pattern — route handlers interact with this class
    rather than calling the AI client directly.
    """

    def __init__(
        self,
        client: GitHubModelsClient,
        prompt_manager: PromptManager,
        lesson_max_tokens: int = 2000,
        quiz_max_tokens: int = 1500,
    ) -> None:
        self._client = client
        self._prompts = prompt_manager
        self._lesson_max_tokens = lesson_max_tokens
        self._quiz_max_tokens = quiz_max_tokens

    async def generate_lesson_content(
        self,
        lesson_id: int,
        topic: str,
        level: str,
        objectives: list[str],
    ) -> dict:
        """Generate Markdown lesson content via the AI API.

        Args:
            lesson_id: Database ID of the lesson.
            topic: Training topic name.
            level: Skill level.
            objectives: Learning objectives for the lesson.

        Returns:
            A dict matching the ``LessonContentResponse`` schema.
        """
        logger.info(
            "Generating lesson content: lesson_id=%d topic=%s level=%s",
            lesson_id, topic, level,
        )
        messages = self._prompts.build_lesson_prompt(topic, level, objectives)
        content = await self._client.generate(
            messages=messages, max_tokens=self._lesson_max_tokens
        )
        return {
            "lesson_id": lesson_id,
            "topic": topic,
            "level": level,
            "content_markdown": content,
            "generated_at": datetime.utcnow().isoformat(),
        }

    async def generate_quiz(
        self,
        lesson_id: int,
        topic: str,
        level: str,
        db: aiosqlite.Connection,
        num_questions: int = 3,
    ) -> dict:
        """Generate a quiz via the AI API, validate it, and persist it.

        Retries up to 2 additional times on validation failure.

        Args:
            lesson_id: Database ID of the lesson.
            topic: Training topic name.
            level: Skill level.
            db: Database connection for quiz persistence.
            num_questions: Number of quiz questions to generate.

        Returns:
            A dict matching the ``QuizResponse`` schema including quiz_id.

        Raises:
            AIResponseValidationError: If validation fails after all attempts.
        """
        logger.info(
            "Generating quiz: lesson_id=%d topic=%s level=%s",
            lesson_id, topic, level,
        )
        messages = self._prompts.build_quiz_prompt(topic, level, num_questions)

        max_validation_attempts = 3
        last_error: AIResponseValidationError | None = None

        for attempt in range(max_validation_attempts):
            raw = await self._client.generate(
                messages=messages, max_tokens=self._quiz_max_tokens
            )
            try:
                quiz = validate_quiz_response(raw, lesson_id, topic, level)
                # Persist the quiz
                repo = QuizRepository(db)
                questions_json = json.dumps(
                    [q.model_dump() for q in quiz.questions]
                )
                quiz_id = await repo.create_quiz(lesson_id, questions_json)

                result = quiz.model_dump()
                result["quiz_id"] = quiz_id
                result["generated_at"] = result["generated_at"].isoformat()
                # Convert questions to plain dicts
                result["questions"] = [q.model_dump() for q in quiz.questions]

                logger.info("Quiz generated and persisted: quiz_id=%d", quiz_id)
                return result

            except AIResponseValidationError as exc:
                last_error = exc
                logger.warning(
                    "Quiz validation failed on attempt %d/%d: %s",
                    attempt + 1, max_validation_attempts, exc.details,
                )

        # All validation attempts exhausted
        raise last_error or AIResponseValidationError(
            details="Quiz validation failed after all attempts"
        )

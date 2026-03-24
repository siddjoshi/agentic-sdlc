"""Prompt template manager for AI content generation."""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class PromptManager:
    """Loads prompt templates from disk and constructs chat messages.

    Templates use Python ``str.format()`` placeholders such as
    ``{topic}``, ``{level}``, ``{objectives}``, and ``{num_questions}``.
    """

    def __init__(self, prompts_dir: str | Path) -> None:
        self._dir = Path(prompts_dir)
        self._lesson_template: str = self._load("lesson_content.txt")
        self._quiz_template: str = self._load("quiz_generation.txt")
        logger.info("Prompt templates loaded from %s", self._dir)

    def _load(self, filename: str) -> str:
        """Load a template file or raise a clear error."""
        path = self._dir / filename
        if not path.exists():
            raise FileNotFoundError(
                f"Prompt template not found: {path}. "
                f"Ensure the '{filename}' file exists in '{self._dir}'."
            )
        return path.read_text(encoding="utf-8")

    def build_lesson_prompt(
        self, topic: str, level: str, objectives: list[str]
    ) -> list[dict]:
        """Construct chat messages for lesson content generation.

        Args:
            topic: Training topic (e.g. 'GitHub Actions').
            level: Skill level ('beginner' or 'intermediate').
            objectives: Learning objectives for the lesson.

        Returns:
            A list of chat message dicts with ``role`` and ``content`` keys.
        """
        objectives_text = "\n".join(f"- {obj}" for obj in objectives)
        user_content = self._lesson_template.format(
            topic=topic, level=level, objectives=objectives_text
        )
        return [
            {
                "role": "system",
                "content": (
                    "You are an expert technical instructor specializing in GitHub tools. "
                    "Generate clear, well-structured lesson content in Markdown format. "
                    "Include practical code examples and explanations."
                ),
            },
            {"role": "user", "content": user_content},
        ]

    def build_quiz_prompt(
        self, topic: str, level: str, num_questions: int = 3
    ) -> list[dict]:
        """Construct chat messages for quiz generation.

        Args:
            topic: Training topic.
            level: Skill level.
            num_questions: Number of questions to generate (3-5).

        Returns:
            A list of chat message dicts requesting JSON quiz output.
        """
        user_content = self._quiz_template.format(
            topic=topic, level=level, num_questions=num_questions
        )
        return [
            {
                "role": "system",
                "content": (
                    "You are an expert quiz creator for GitHub training courses. "
                    "Generate multiple-choice quiz questions. "
                    "Respond ONLY with a valid JSON array of question objects. "
                    "Each object must have: question (string), options (array of exactly 4 strings), "
                    "correct_answer (string matching one of the options), explanation (string)."
                ),
            },
            {"role": "user", "content": user_content},
        ]

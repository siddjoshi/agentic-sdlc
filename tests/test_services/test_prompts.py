"""Tests for PromptManager — prompt template loading and construction.

Covers: BRD-AI-005, BRD-AI-010, TASK-013
"""

from __future__ import annotations

import pytest

from src.ai.prompts import PromptManager


class TestPromptManager:
    """PromptManager tests."""

    def test_loads_templates_from_disk(self):
        """Verify templates load from prompts/ directory. [TASK-013] [BRD-AI-005]"""
        pm = PromptManager("prompts")
        assert pm._lesson_template is not None
        assert pm._quiz_template is not None
        assert len(pm._lesson_template) > 0
        assert len(pm._quiz_template) > 0

    def test_build_lesson_prompt_structure(self):
        """Verify lesson prompt returns correct message structure. [TASK-013] [BRD-AI-010]"""
        pm = PromptManager("prompts")
        messages = pm.build_lesson_prompt(
            topic="GitHub Actions",
            level="beginner",
            objectives=["Learn workflows", "Run tests"],
        )
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"

    def test_build_lesson_prompt_includes_topic(self):
        """Verify lesson prompt includes topic and level. [TASK-013] [BRD-AI-010]"""
        pm = PromptManager("prompts")
        messages = pm.build_lesson_prompt(
            topic="GitHub Copilot",
            level="intermediate",
            objectives=["Prompt engineering"],
        )
        user_content = messages[1]["content"]
        assert "GitHub Copilot" in user_content
        assert "intermediate" in user_content

    def test_build_lesson_prompt_includes_objectives(self):
        """Verify lesson prompt includes objectives. [TASK-013] [BRD-AI-010]"""
        pm = PromptManager("prompts")
        messages = pm.build_lesson_prompt(
            topic="Test",
            level="beginner",
            objectives=["Objective A", "Objective B"],
        )
        user_content = messages[1]["content"]
        assert "Objective A" in user_content
        assert "Objective B" in user_content

    def test_build_quiz_prompt_structure(self):
        """Verify quiz prompt returns correct message structure. [TASK-013] [BRD-AI-005]"""
        pm = PromptManager("prompts")
        messages = pm.build_quiz_prompt(
            topic="GitHub Actions",
            level="beginner",
            num_questions=3,
        )
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"

    def test_build_quiz_prompt_includes_topic(self):
        """Verify quiz prompt includes topic and level. [TASK-013] [BRD-AI-010]"""
        pm = PromptManager("prompts")
        messages = pm.build_quiz_prompt(
            topic="GitHub Advanced Security",
            level="intermediate",
            num_questions=5,
        )
        user_content = messages[1]["content"]
        assert "GitHub Advanced Security" in user_content
        assert "intermediate" in user_content

    def test_build_quiz_prompt_system_mentions_json(self):
        """Verify quiz system message requests JSON output. [TASK-013] [BRD-AI-002]"""
        pm = PromptManager("prompts")
        messages = pm.build_quiz_prompt("Test", "beginner", 3)
        system_content = messages[0]["content"]
        assert "JSON" in system_content

    def test_missing_template_raises_error(self, tmp_path):
        """Verify FileNotFoundError for missing templates. [TASK-013] [BRD-AI-005]"""
        with pytest.raises(FileNotFoundError):
            PromptManager(str(tmp_path))

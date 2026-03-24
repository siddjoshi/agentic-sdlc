"""Tests for AI response validation schemas.

Covers: BRD-AI-003, BRD-AI-008, TASK-016
"""

from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from src.ai.schemas import QuizQuestion, QuizResponseSchema, validate_quiz_response
from src.exceptions import AIResponseValidationError


class TestQuizQuestion:
    """QuizQuestion model validation tests."""

    def test_valid_question(self):
        """Verify valid QuizQuestion creation. [TASK-016] [BRD-AI-008]"""
        q = QuizQuestion(
            question="What is X?",
            options=["A", "B", "C", "D"],
            correct_answer="B",
            explanation="B is correct.",
        )
        assert q.question == "What is X?"
        assert len(q.options) == 4
        assert q.correct_answer == "B"

    def test_exactly_four_options_required(self):
        """Verify exactly 4 options enforced. [TASK-016] [BRD-AI-008]"""
        with pytest.raises(ValidationError):
            QuizQuestion(
                question="Q?",
                options=["A", "B", "C"],
                correct_answer="A",
                explanation="Exp",
            )

    def test_more_than_four_options_rejected(self):
        """Verify more than 4 options rejected. [TASK-016] [BRD-AI-008]"""
        with pytest.raises(ValidationError):
            QuizQuestion(
                question="Q?",
                options=["A", "B", "C", "D", "E"],
                correct_answer="A",
                explanation="Exp",
            )

    def test_correct_answer_must_be_in_options(self):
        """Verify correct_answer must be in options list. [TASK-016] [BRD-AI-008]"""
        with pytest.raises(ValidationError):
            QuizQuestion(
                question="Q?",
                options=["A", "B", "C", "D"],
                correct_answer="Z",
                explanation="Exp",
            )


class TestQuizResponseSchema:
    """QuizResponseSchema validation tests."""

    def test_valid_quiz_response(self):
        """Verify valid QuizResponseSchema creation. [TASK-016] [BRD-AI-003]"""
        questions = [
            QuizQuestion(
                question=f"Q{i}?",
                options=["A", "B", "C", "D"],
                correct_answer="A",
                explanation="Exp",
            )
            for i in range(3)
        ]
        schema = QuizResponseSchema(
            lesson_id=1, topic="Test", level="beginner", questions=questions
        )
        assert len(schema.questions) == 3

    def test_minimum_three_questions(self):
        """Verify minimum 3 questions enforced. [TASK-016] [BRD-AI-003]"""
        questions = [
            QuizQuestion(
                question=f"Q{i}?",
                options=["A", "B", "C", "D"],
                correct_answer="A",
                explanation="Exp",
            )
            for i in range(2)
        ]
        with pytest.raises(ValidationError):
            QuizResponseSchema(
                lesson_id=1, topic="Test", level="beginner", questions=questions
            )

    def test_maximum_five_questions(self):
        """Verify maximum 5 questions enforced. [TASK-016] [BRD-AI-003]"""
        questions = [
            QuizQuestion(
                question=f"Q{i}?",
                options=["A", "B", "C", "D"],
                correct_answer="A",
                explanation="Exp",
            )
            for i in range(6)
        ]
        with pytest.raises(ValidationError):
            QuizResponseSchema(
                lesson_id=1, topic="Test", level="beginner", questions=questions
            )


class TestValidateQuizResponse:
    """validate_quiz_response() function tests."""

    def test_valid_json_array(self):
        """Verify parsing a valid JSON array. [TASK-016] [BRD-AI-003]"""
        raw = json.dumps([
            {
                "question": f"Q{i}?",
                "options": ["A", "B", "C", "D"],
                "correct_answer": "A",
                "explanation": "Exp",
            }
            for i in range(3)
        ])
        result = validate_quiz_response(raw, lesson_id=1, topic="Test", level="beginner")
        assert len(result.questions) == 3
        assert result.lesson_id == 1

    def test_valid_json_object_with_questions_key(self):
        """Verify parsing a JSON object with 'questions' key. [TASK-016] [BRD-AI-003]"""
        raw = json.dumps({
            "questions": [
                {
                    "question": f"Q{i}?",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "A",
                    "explanation": "Exp",
                }
                for i in range(3)
            ]
        })
        result = validate_quiz_response(raw, lesson_id=2, topic="Test", level="intermediate")
        assert len(result.questions) == 3

    def test_handles_markdown_code_fences(self):
        """Verify stripping of markdown code fences. [TASK-016] [BRD-AI-003]"""
        inner = json.dumps([
            {
                "question": f"Q{i}?",
                "options": ["A", "B", "C", "D"],
                "correct_answer": "A",
                "explanation": "Exp",
            }
            for i in range(3)
        ])
        raw = f"```json\n{inner}\n```"
        result = validate_quiz_response(raw, lesson_id=1, topic="T", level="beginner")
        assert len(result.questions) == 3

    def test_invalid_json_raises_error(self):
        """Verify AIResponseValidationError for malformed JSON. [TASK-016] [BRD-AI-003]"""
        with pytest.raises(AIResponseValidationError):
            validate_quiz_response("not json", lesson_id=1, topic="T", level="beginner")

    def test_wrong_structure_raises_error(self):
        """Verify AIResponseValidationError for wrong JSON structure. [TASK-016] [BRD-AI-003]"""
        with pytest.raises(AIResponseValidationError):
            validate_quiz_response(
                json.dumps({"wrong": "structure"}),
                lesson_id=1,
                topic="T",
                level="beginner",
            )

    def test_too_few_questions_raises_error(self):
        """Verify error when quiz has fewer than 3 questions. [TASK-016] [BRD-AI-003]"""
        raw = json.dumps([
            {
                "question": "Q1?",
                "options": ["A", "B", "C", "D"],
                "correct_answer": "A",
                "explanation": "Exp",
            }
        ])
        with pytest.raises(AIResponseValidationError):
            validate_quiz_response(raw, lesson_id=1, topic="T", level="beginner")

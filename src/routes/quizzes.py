"""Quiz submission and scoring route handler."""

from __future__ import annotations

import json

from fastapi import APIRouter, Depends

from src.dependencies import get_db
from src.exceptions import QuizNotFoundError
from src.models.requests import QuizSubmission
from src.models.responses import QuestionResult, QuizResult
from src.repositories.quiz_repository import QuizRepository

router = APIRouter(prefix="/quiz", tags=["quizzes"])


@router.post("/{quiz_id}/submit", response_model=QuizResult)
async def submit_quiz(
    quiz_id: int,
    submission: QuizSubmission,
    db=Depends(get_db),
) -> QuizResult:
    """Score a quiz submission and persist the attempt.

    Returns 404 if the quiz does not exist.
    Returns 422 if the number of answers does not match the number of questions.
    """
    repo = QuizRepository(db)
    quiz = await repo.get_quiz(quiz_id)
    if quiz is None:
        raise QuizNotFoundError(quiz_id)

    questions = json.loads(quiz["questions_json"])

    # Validate answer count
    if len(submission.answers) != len(questions):
        from fastapi import HTTPException

        raise HTTPException(
            status_code=422,
            detail={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": (
                        f"Expected {len(questions)} answers but received "
                        f"{len(submission.answers)}."
                    ),
                    "details": None,
                }
            },
        )

    # Score
    score = 0
    results: list[QuestionResult] = []
    for q, user_answer in zip(questions, submission.answers):
        correct = user_answer == q["correct_answer"]
        if correct:
            score += 1
        results.append(
            QuestionResult(correct=correct, explanation=q["explanation"])
        )

    total = len(questions)
    percentage = round(score * 100.0 / total, 1) if total > 0 else 0.0

    # Persist attempt
    await repo.create_attempt(
        quiz_id=quiz_id,
        user_id=submission.user_id,
        score=score,
        total=total,
        percentage=percentage,
        answers_json=json.dumps(submission.answers),
    )

    return QuizResult(
        quiz_id=quiz_id,
        user_id=submission.user_id,
        score=score,
        total=total,
        percentage=percentage,
        results=results,
    )

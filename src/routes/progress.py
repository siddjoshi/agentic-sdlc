"""User progress tracking route handlers."""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends

from src.dependencies import get_db
from src.exceptions import LessonNotFoundError
from src.models.requests import LessonCompleteRequest
from src.models.responses import (
    CourseProgress,
    ProgressResponse,
    ProgressUpdateResponse,
)
from src.repositories.course_repository import CourseRepository
from src.repositories.progress_repository import ProgressRepository

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/{user_id}", response_model=ProgressResponse)
async def get_progress(
    user_id: str,
    db=Depends(get_db),
) -> ProgressResponse:
    """Get a user's progress across all courses.

    Returns all courses with completion stats and quiz scores.
    """
    progress_repo = ProgressRepository(db)
    course_progress = await progress_repo.get_progress(user_id)

    courses = []
    for cp in course_progress:
        quiz_scores = await progress_repo.get_quiz_scores(user_id, cp["course_id"])
        courses.append(
            CourseProgress(
                course_id=cp["course_id"],
                course_title=cp["course_title"],
                completed_lessons=cp["completed_lessons"],
                total_lessons=cp["total_lessons"],
                quiz_scores=quiz_scores,
                completion_percentage=cp["completion_percentage"],
            )
        )

    return ProgressResponse(user_id=user_id, courses=courses)


@router.post("/{user_id}/complete", response_model=ProgressUpdateResponse)
async def mark_lesson_complete(
    user_id: str,
    body: LessonCompleteRequest,
    db=Depends(get_db),
) -> ProgressUpdateResponse:
    """Mark a lesson as completed for a user.

    Returns 404 if the lesson does not exist.
    Duplicate completions are idempotent.
    """
    # Verify the lesson exists
    course_repo = CourseRepository(db)
    await course_repo.get_lesson(body.lesson_id)  # raises LessonNotFoundError

    progress_repo = ProgressRepository(db)
    completed_at = await progress_repo.mark_complete(user_id, body.lesson_id)

    return ProgressUpdateResponse(
        user_id=user_id,
        lesson_id=body.lesson_id,
        status="completed",
        updated_at=completed_at,
    )

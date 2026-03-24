"""Lesson content and quiz generation route handlers."""

from __future__ import annotations

import json

from fastapi import APIRouter, Depends, Request

from src.dependencies import get_content_service, get_db
from src.models.responses import LessonContentResponse, QuizQuestionResponse, QuizResponse
from src.repositories.course_repository import CourseRepository
from src.services.content_service import ContentService

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.post("/{lesson_id}/content", response_model=LessonContentResponse)
async def generate_lesson_content(
    lesson_id: int,
    db=Depends(get_db),
    content_service: ContentService = Depends(get_content_service),
) -> LessonContentResponse:
    """Generate AI-powered lesson content for a specific lesson.

    Returns 404 if the lesson does not exist.
    AI errors propagate as HTTP 503.
    """
    repo = CourseRepository(db)
    lesson = await repo.get_lesson(lesson_id)
    course = await repo.get_course(lesson["course_id"])

    objectives = json.loads(lesson["objectives"]) if isinstance(lesson["objectives"], str) else lesson["objectives"]

    result = await content_service.generate_lesson_content(
        lesson_id=lesson_id,
        topic=course["title"],
        level=lesson["level"],
        objectives=objectives,
    )
    return LessonContentResponse(**result)


@router.post("/{lesson_id}/quiz", response_model=QuizResponse)
async def generate_quiz(
    lesson_id: int,
    db=Depends(get_db),
    content_service: ContentService = Depends(get_content_service),
) -> QuizResponse:
    """Generate a multiple-choice quiz for a specific lesson.

    Returns 404 if the lesson does not exist.
    AI errors propagate as HTTP 502/503.
    """
    repo = CourseRepository(db)
    lesson = await repo.get_lesson(lesson_id)
    course = await repo.get_course(lesson["course_id"])

    result = await content_service.generate_quiz(
        lesson_id=lesson_id,
        topic=course["title"],
        level=lesson["level"],
        db=db,
    )
    return QuizResponse(
        quiz_id=result["quiz_id"],
        lesson_id=result["lesson_id"],
        topic=result["topic"],
        level=result["level"],
        questions=[QuizQuestionResponse(**q) for q in result["questions"]],
        generated_at=result["generated_at"],
    )

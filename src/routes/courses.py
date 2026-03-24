"""Course catalog route handlers."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from src.dependencies import get_db
from src.models.responses import (
    CourseDetailResponse,
    CourseListResponse,
    CourseResponse,
    LessonListResponse,
    LessonSummary,
)
from src.repositories.course_repository import CourseRepository

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=CourseListResponse)
async def list_courses(
    limit: int = Query(default=20, ge=1, le=100, description="Max results to return"),
    offset: int = Query(default=0, ge=0, description="Number of results to skip"),
    db=Depends(get_db),
) -> CourseListResponse:
    """List all courses with pagination."""
    repo = CourseRepository(db)
    courses, total = await repo.list_courses(limit=limit, offset=offset)
    return CourseListResponse(
        courses=[
            CourseResponse(
                id=c["id"],
                title=c["title"],
                description=c["description"],
                level=c["level"],
                total_lessons=c["total_lessons"],
            )
            for c in courses
        ],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{course_id}", response_model=CourseDetailResponse)
async def get_course(
    course_id: int,
    db=Depends(get_db),
) -> CourseDetailResponse:
    """Get course details including lesson outline.

    Returns 404 if the course does not exist.
    """
    repo = CourseRepository(db)
    course = await repo.get_course(course_id)
    return CourseDetailResponse(
        id=course["id"],
        title=course["title"],
        description=course["description"],
        level=course["level"],
        lessons=[
            LessonSummary(
                id=l["id"], title=l["title"], level=l["level"], order=l["order"]
            )
            for l in course["lessons"]
        ],
    )


@router.get("/{course_id}/lessons", response_model=LessonListResponse)
async def list_lessons(
    course_id: int,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db=Depends(get_db),
) -> LessonListResponse:
    """List lessons for a course with pagination.

    Returns 404 if the course does not exist.
    """
    repo = CourseRepository(db)
    lessons, total = await repo.list_lessons(course_id, limit=limit, offset=offset)
    return LessonListResponse(
        lessons=[
            LessonSummary(
                id=l["id"], title=l["title"], level=l["level"], order=l["order"]
            )
            for l in lessons
        ],
        total=total,
        limit=limit,
        offset=offset,
    )

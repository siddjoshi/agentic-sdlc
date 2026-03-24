"""Tests for course catalog endpoints.

Covers: BRD-FR-001, BRD-FR-002, BRD-FR-003, BRD-FR-014, TASK-010, TASK-011
"""

from __future__ import annotations

import pytest

from tests.conftest import AUTH_HEADERS

pytestmark = pytest.mark.asyncio


class TestListCourses:
    """GET /api/v1/courses tests."""

    async def test_list_courses_returns_200(self, client):
        """Verify listing courses returns 200 with course data. [TASK-011] [BRD-FR-001]"""
        resp = await client.get("/api/v1/courses", headers=AUTH_HEADERS)
        assert resp.status_code == 200
        data = resp.json()
        assert "courses" in data
        assert "total" in data
        assert data["total"] == 6  # 3 topics × 2 levels

    async def test_list_courses_default_pagination(self, client):
        """Verify default pagination: limit=20, offset=0. [TASK-011] [BRD-FR-014]"""
        resp = await client.get("/api/v1/courses", headers=AUTH_HEADERS)
        data = resp.json()
        assert data["limit"] == 20
        assert data["offset"] == 0
        assert len(data["courses"]) == 6

    async def test_list_courses_custom_pagination(self, client):
        """Verify pagination with limit=2&offset=0. [TASK-011] [BRD-FR-014]"""
        resp = await client.get(
            "/api/v1/courses?limit=2&offset=0", headers=AUTH_HEADERS
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["courses"]) == 2
        assert data["total"] == 6
        assert data["limit"] == 2
        assert data["offset"] == 0

    async def test_list_courses_offset_pagination(self, client):
        """Verify offset skips results. [TASK-011] [BRD-FR-014]"""
        resp = await client.get(
            "/api/v1/courses?limit=2&offset=4", headers=AUTH_HEADERS
        )
        data = resp.json()
        assert len(data["courses"]) == 2
        assert data["offset"] == 4

    async def test_list_courses_response_schema(self, client):
        """Verify each course has required fields. [TASK-011] [BRD-FR-001]"""
        resp = await client.get("/api/v1/courses", headers=AUTH_HEADERS)
        data = resp.json()
        for course in data["courses"]:
            assert "id" in course
            assert "title" in course
            assert "description" in course
            assert "level" in course
            assert "total_lessons" in course

    async def test_list_courses_invalid_limit_returns_422(self, client):
        """Verify limit=0 returns 422. [TASK-011] [BRD-FR-012]"""
        resp = await client.get(
            "/api/v1/courses?limit=0", headers=AUTH_HEADERS
        )
        assert resp.status_code == 422


class TestGetCourse:
    """GET /api/v1/courses/{course_id} tests."""

    async def test_get_course_valid_id(self, client):
        """Verify getting a course by valid ID. [TASK-011] [BRD-FR-002]"""
        resp = await client.get("/api/v1/courses/1", headers=AUTH_HEADERS)
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == 1
        assert "title" in data
        assert "description" in data
        assert "level" in data
        assert "lessons" in data
        assert isinstance(data["lessons"], list)

    async def test_get_course_includes_lessons(self, client):
        """Verify course detail includes lesson list. [TASK-011] [BRD-FR-002]"""
        resp = await client.get("/api/v1/courses/1", headers=AUTH_HEADERS)
        data = resp.json()
        assert len(data["lessons"]) > 0
        for lesson in data["lessons"]:
            assert "id" in lesson
            assert "title" in lesson
            assert "level" in lesson
            assert "order" in lesson

    async def test_get_course_not_found_returns_404(self, client):
        """Verify 404 for non-existent course. [TASK-011] [BRD-FR-002]"""
        resp = await client.get("/api/v1/courses/999", headers=AUTH_HEADERS)
        assert resp.status_code == 404
        data = resp.json()
        assert data["error"]["code"] == "COURSE_NOT_FOUND"


class TestListLessons:
    """GET /api/v1/courses/{course_id}/lessons tests."""

    async def test_list_lessons_returns_200(self, client):
        """Verify listing lessons for a valid course. [TASK-011] [BRD-FR-003]"""
        resp = await client.get(
            "/api/v1/courses/1/lessons", headers=AUTH_HEADERS
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "lessons" in data
        assert "total" in data
        assert len(data["lessons"]) > 0

    async def test_list_lessons_ordered(self, client):
        """Verify lessons are returned in order. [TASK-011] [BRD-FR-003]"""
        resp = await client.get(
            "/api/v1/courses/1/lessons", headers=AUTH_HEADERS
        )
        data = resp.json()
        orders = [l["order"] for l in data["lessons"]]
        assert orders == sorted(orders)

    async def test_list_lessons_nonexistent_course_returns_404(self, client):
        """Verify 404 for lessons of non-existent course. [TASK-011] [BRD-FR-003]"""
        resp = await client.get(
            "/api/v1/courses/999/lessons", headers=AUTH_HEADERS
        )
        assert resp.status_code == 404

    async def test_list_lessons_pagination(self, client):
        """Verify lesson pagination works. [TASK-011] [BRD-FR-014]"""
        resp = await client.get(
            "/api/v1/courses/1/lessons?limit=2&offset=0", headers=AUTH_HEADERS
        )
        data = resp.json()
        assert len(data["lessons"]) == 2
        assert data["limit"] == 2
        assert data["offset"] == 0

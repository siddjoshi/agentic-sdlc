"""Tests for API key authentication middleware.

Covers: BRD-FR-013, BRD-NFR-004, TASK-004
"""

from __future__ import annotations

import pytest

from tests.conftest import AUTH_HEADERS

pytestmark = pytest.mark.asyncio


class TestAuthentication:
    """API key authentication tests."""

    async def test_missing_api_key_returns_401(self, unauth_client):
        """Verify 401 when X-API-Key header is missing. [TASK-004] [BRD-FR-013]"""
        resp = await unauth_client.get("/api/v1/courses")
        assert resp.status_code == 401
        data = resp.json()
        assert data["error"]["code"] == "UNAUTHORIZED"

    async def test_invalid_api_key_returns_401(self, unauth_client):
        """Verify 401 when X-API-Key value is wrong. [TASK-004] [BRD-FR-013]"""
        resp = await unauth_client.get(
            "/api/v1/courses", headers={"X-API-Key": "wrong-key"}
        )
        assert resp.status_code == 401
        data = resp.json()
        assert data["error"]["code"] == "UNAUTHORIZED"

    async def test_valid_api_key_passes(self, client):
        """Verify valid key grants access. [TASK-004] [BRD-FR-013]"""
        resp = await client.get("/api/v1/courses", headers=AUTH_HEADERS)
        assert resp.status_code == 200

    async def test_health_exempt_from_auth(self, unauth_client):
        """Verify /api/v1/health is exempt from auth. [TASK-004] [BRD-FR-013]"""
        resp = await unauth_client.get("/api/v1/health")
        assert resp.status_code == 200

    async def test_401_error_response_format(self, unauth_client):
        """Verify 401 response follows ErrorResponse format. [TASK-004] [BRD-FR-013]"""
        resp = await unauth_client.get("/api/v1/courses")
        assert resp.status_code == 401
        data = resp.json()
        assert "error" in data
        assert "code" in data["error"]
        assert "message" in data["error"]

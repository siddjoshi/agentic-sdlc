"""Tests for the health check endpoint.

Covers: BRD-FR-009, TASK-005, BRD-FR-013
"""

from __future__ import annotations

import pytest

from tests.conftest import AUTH_HEADERS

pytestmark = pytest.mark.asyncio


class TestHealthCheck:
    """Health check endpoint tests."""

    async def test_health_check_returns_healthy(self, client):
        """Verify health returns 200 with healthy status. [TASK-005] [BRD-FR-009]"""
        resp = await client.get("/api/v1/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"
        assert "version" in data

    async def test_health_check_without_auth(self, unauth_client):
        """Verify health endpoint is exempt from authentication. [TASK-004] [BRD-FR-013]"""
        resp = await unauth_client.get("/api/v1/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"

    async def test_health_check_includes_version(self, client):
        """Verify health response includes app version. [TASK-005] [BRD-FR-009]"""
        resp = await client.get("/api/v1/health")
        data = resp.json()
        assert data["version"] == "1.0.0"

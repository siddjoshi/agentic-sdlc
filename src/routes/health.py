"""Health check route handler."""

from __future__ import annotations

import logging

from fastapi import APIRouter, Request

from src.models.responses import HealthResponse

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check(request: Request) -> HealthResponse:
    """Return the system health status.

    Checks database connectivity and reports overall application health.
    No authentication required.
    """
    db_status = "connected"
    status = "healthy"

    try:
        db_manager = request.app.state.db_manager
        conn = await db_manager.get_connection()
        cursor = await conn.execute("SELECT 1")
        await cursor.fetchone()
    except Exception:
        db_status = "disconnected"
        status = "degraded"
        logger.warning("Health check: database unreachable")

    version = request.app.state.settings.app_version

    return HealthResponse(status=status, version=version, database=db_status)

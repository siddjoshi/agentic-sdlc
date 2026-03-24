"""FastAPI dependency injection providers."""

from __future__ import annotations

from fastapi import Request

import aiosqlite

from src.services.content_service import ContentService


async def get_db(request: Request) -> aiosqlite.Connection:
    """Yield the active database connection from the app state."""
    db_manager = request.app.state.db_manager
    return await db_manager.get_connection()


async def get_content_service(request: Request) -> ContentService:
    """Return the ContentService instance from the app state."""
    return request.app.state.content_service

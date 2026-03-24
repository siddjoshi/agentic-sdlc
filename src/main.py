"""FastAPI application entry point."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.ai.client import GitHubModelsClient
from src.ai.prompts import PromptManager
from src.config import get_settings
from src.database.connection import DatabaseManager
from src.exceptions import register_exception_handlers
from src.middleware.auth import APIKeyMiddleware
from src.middleware.logging import RequestLoggingMiddleware
from src.routes import courses, health, lessons, progress, quizzes
from src.services.content_service import ContentService

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Async lifespan context: initialise DB and AI client on startup, clean up on shutdown."""
    settings = get_settings()
    app.state.settings = settings

    # Database
    db_manager = DatabaseManager(settings.database_url)
    await db_manager.initialize()
    app.state.db_manager = db_manager

    # AI client and services
    ai_client = GitHubModelsClient(
        endpoint=settings.github_models_endpoint,
        api_key=settings.github_models_api_key,
        model=settings.github_models_model,
        timeout=settings.ai_request_timeout,
        max_retries=settings.ai_max_retries,
        initial_backoff=settings.ai_initial_backoff,
        max_backoff=settings.ai_max_backoff,
        jitter_ms=settings.ai_backoff_jitter,
    )
    prompt_manager = PromptManager(settings.prompts_dir)
    content_service = ContentService(
        client=ai_client,
        prompt_manager=prompt_manager,
        lesson_max_tokens=settings.lesson_max_tokens,
        quiz_max_tokens=settings.quiz_max_tokens,
    )
    app.state.content_service = content_service

    logger.info("Application started — version %s", settings.app_version)
    yield

    # Shutdown
    await ai_client.close()
    await db_manager.close()
    logger.info("Application shutdown complete")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    )

    app = FastAPI(
        title="AI-Powered Learning Platform",
        description="GitHub training platform with AI-generated lessons and quizzes.",
        version=settings.app_version,
        lifespan=lifespan,
    )

    # Middleware (order matters — outermost first)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(APIKeyMiddleware, api_key=settings.api_key)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception handlers
    register_exception_handlers(app)

    # Routers
    app.include_router(health.router, prefix="/api/v1")
    app.include_router(courses.router, prefix="/api/v1")
    app.include_router(lessons.router, prefix="/api/v1")
    app.include_router(quizzes.router, prefix="/api/v1")
    app.include_router(progress.router, prefix="/api/v1")

    return app


app = create_app()

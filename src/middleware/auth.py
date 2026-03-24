"""API key authentication middleware."""

from __future__ import annotations

import logging

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

logger = logging.getLogger(__name__)

# Paths exempt from API key authentication
_EXEMPT_PATHS = frozenset({"/api/v1/health", "/docs", "/openapi.json", "/redoc"})


class APIKeyMiddleware(BaseHTTPMiddleware):
    """Validates the ``X-API-Key`` header on all routes except health and docs.

    If the key is missing or does not match the configured value, a 401
    JSON error response is returned.
    """

    def __init__(self, app, api_key: str) -> None:  # noqa: ANN001
        super().__init__(app)
        self._api_key = api_key

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Check the API key header."""
        path = request.url.path

        # Allow exempt paths
        if path in _EXEMPT_PATHS or path.startswith("/static"):
            return await call_next(request)

        key = request.headers.get("X-API-Key")
        if not key or key != self._api_key:
            logger.warning("Unauthorized request: %s %s", request.method, path)
            return JSONResponse(
                status_code=401,
                content={
                    "error": {
                        "code": "UNAUTHORIZED",
                        "message": "Missing or invalid API key. Provide a valid key in the X-API-Key header.",
                        "details": None,
                    }
                },
            )

        return await call_next(request)

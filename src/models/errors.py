"""Error response Pydantic models."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Structured error detail."""

    code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[str] = None
    retry_after: Optional[int] = None


class ErrorResponse(BaseModel):
    """Standard error response wrapper."""

    error: ErrorDetail
